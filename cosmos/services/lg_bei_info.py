import base64
from parse import parse

# custom modules
from cosmos.utils.logging import Logger
from cosmos.utils.constants import (
    BEI_INFO_CMD_FORMATSTR,
    BEI_INFO_CMD_RESULT_CD,
    BEI_INFO_CMD_DEFAULT_MSG,
    BEI_INFO_CMD_DEFAULT_IMAGE_URL_ENDPOINT,
    BEI_INFO_CMD_FAILURE_MSG
)
from cosmos.schema.lg_bei_info_schema import BeiInfoTarget

logger = Logger()


def parse_request_and_find_image_data(base64_str: str):
    decoded_str = base64.b64decode(base64_str).decode('utf-8')
    parsed_result = parse(BEI_INFO_CMD_FORMATSTR, decoded_str)
    product_id, model_nm, fw_type, image_ver, image_rev, ignore_disable = parsed_result

    if not product_id or not model_nm or not fw_type or not image_ver or not image_rev or not ignore_disable:
        return BeiInfoTarget(
            result_cd=BEI_INFO_CMD_RESULT_CD,
            msg=BEI_INFO_CMD_FAILURE_MSG,
            image_url='/',
            image_size=1,
            image_dir='/',
            image_name='no_image',
            image_rev='00',
            image_ver='01.02.03',
            cdn_url=BEI_INFO_CMD_DEFAULT_IMAGE_URL_ENDPOINT,
        )
    return BeiInfoTarget(
        result_cd=BEI_INFO_CMD_RESULT_CD,
        msg=BEI_INFO_CMD_DEFAULT_MSG,
        image_url='/',
        image_size=1,
        image_dir='/',
        image_name='no_image',
        image_rev='00',
        image_ver='01.02.03',
        cdn_url=BEI_INFO_CMD_DEFAULT_IMAGE_URL_ENDPOINT,
    )


async def process_cdn_bei_info_cmd(request_id:str, base64_str: str):
    res = parse_request_and_find_image_data(base64_str)
    reponse_formate = f'<?xml version="1.0" encoding="utf-8"?><RESPONSE><REQ_ID>{request_id}</REQ_ID><RESULT_CD>{res.result_cd}</RESULT_CD><MSG>{res.msg}</MSG><IMAGE_URL>{res.image_url}</IMAGE_URL><UPDATE_CNT>1</UPDATE_CNT><IMAGE_SIZE>{res.image_size}</IMAGE_SIZE><IMAGE_DIR>{res.image_dir}</IMAGE_DIR><IMAGE_NAME>{res.image_name}</IMAGE_NAME><IMAGE_REV>{res.image_rev}</IMAGE_REV><IMAGE_VER>{res.image_ver}</IMAGE_VER><CDN_URL>{res.cdn_url}</CDN_URL></RESPONSE>'

    # encode the response with base64
    encoded_str = base64.b64encode(reponse_formate.encode('utf-8'))
    response_str = encoded_str.decode('utf-8')
    return response_str
