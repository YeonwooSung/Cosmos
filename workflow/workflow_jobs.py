# custom modules
from .workflow_type import SQL_Info

def run_sql_work(command: str, sql_info: SQL_Info):
    assert sql_info is not None, 'SQL info is required for SQL workflow type.'

    print('Run SQL Work')
    pass

def run_python_work(command: str):
    print('Run Python Work')
    pass
