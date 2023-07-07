from pydantic import BaseModel

class SQL_Info(BaseModel):
    sql_url: str
    sql_user: str
    sql_password: str

class WorkflowType(BaseModel):
    workflow_id: str
    workflow_type: str # one of ['python', 'sql']
    command_str: str

    sql_info: SQL_Info = None
