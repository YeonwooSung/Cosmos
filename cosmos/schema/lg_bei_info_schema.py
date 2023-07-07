from pydantic import BaseModel, Field

# custom modules
from cosmos.utils.constants import BEI_INFO_CMD_RESULT_CD, BEI_INFO_CMD_DEFAULT_MSG

class BeiInfoTarget(BaseModel):
    result_cd: int = Field(default=BEI_INFO_CMD_RESULT_CD)
    msg: str = Field(default=BEI_INFO_CMD_DEFAULT_MSG)
    image_url: str
    image_size: str
    image_dir: str
    image_name: str
    image_rev: str
    image_ver: str
    cdn_url: str
