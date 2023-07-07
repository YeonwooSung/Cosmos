from airflow import DAG, ScheduleArg
from airflow.operators.python import PythonOperator
import os
from typing import Union

# custom modules
from .workflow_jobs import run_python_work, run_sql_work
from .workflow_type import WorkflowType


class AirflowPipelineGenerator:
    '''
    Generate Airflow DAGs from a list of tasks.

    Reference: <https://docs.astronomer.io/learn/dynamically-generating-dags>
    '''

    def __init__(self) -> None:
        pass

    def generate_pipeline_from_task_list(
        self,
        dag_id: str,
        schedule: ScheduleArg,
        default_args: Union[dict, None] = None,
        task_list: list[WorkflowType] = [],
    ) -> tuple[DAG, list[WorkflowType]]:
        '''
        Generate a DAG from a list of tasks.

        Args:
            dag_id (str): DAG ID
            schedule (ScheduleArg): DAG schedule
            default_args (Union[dict, None], optional): DAG default arguments. Defaults to None.
            task_list (list[WorkflowType], optional): List of tasks. Defaults to [].

        Returns:
            tuple[DAG, list[WorkflowType]]: A tuple of DAG and task list.

        Raises:
            ValueError: If task list is empty.
            ValueError: If workflow type is invalid.
            ValueError: If SQL info is required for SQL workflow type.
        '''
        if task_list is None or len(task_list) == 0:
            raise ValueError('Task list is empty.')

        dag = DAG(dag_id, schedule=schedule, default_args=default_args)

        # define tasks in DAG
        with dag:
            for task in task_list:
                workflow_type = task['workflow_type']

                kwargs = { 'command': task['command_str'] }

                if workflow_type == 'python':
                    _ = PythonOperator(
                        task_id=task['task_id'],
                        python_callable=run_python_work,
                        op_kwargs=kwargs,
                    )

                elif workflow_type == 'sql':
                    if task['sql_info'] is None:
                        raise ValueError('SQL info is required for SQL workflow type.')
                    kwargs['sql_info'] = task['sql_info']

                    _ = PythonOperator(
                        task_id=task['task_id'],
                        python_callable=run_sql_work,
                        op_kwargs=kwargs,
                    )

                else:
                    raise ValueError('Invalid workflow type.')
        return dag, task_list


    def save_dag_to_file(self, dag: DAG, dag_file_path: str) -> None:
        '''
        Save a DAG to a file.

        Args:
            task_list (list[WorkflowType]): List of tasks.
            dag (DAG): DAG.
            dag_file_path (str): DAG file path.

        Raises:
            ValueError: If DAG file already exists.
        '''
        if os.path.exists(dag_file_path):
            raise ValueError(f'DAG file {dag_file_path} already exists.')

        # save DAG to file
        with open(dag_file_path, 'w') as f:
            f.write(dag.fileloc)
        print(f'DAG file saved to {dag_file_path}.')


    def load_dag_from_file(self, dag_file_path: str) -> DAG:
        '''
        Load a DAG from a file.

        Args:
            dag_file_path (str): DAG file path.

        Returns:
            DAG: DAG.

        Raises:
            ValueError: If DAG file does not exist.
        '''
        if not os.path.exists(dag_file_path):
            raise ValueError(f'DAG file {dag_file_path} does not exist.')
        dag = DAG.load(dag_file_path)
        return dag
