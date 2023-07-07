
# utils/logging.py
LOGGING_DEFAULT_LOG_NAME = "cosmos"
LOGGING_DEFAULT_LOG_LEVEL = "DEBUG"
LOGGING_DEFAULT_CONSOLE_LOG_LEVEL = "INFO"
LOGGING_DEFAULT_MAX_BYTES = 10485760
LOGGING_DEFAULT_BACKUP_COUNT = 10
LOGGING_DEFAULT_LOGGING_WORKERS = 1

# utils/database.py
DB_ISOLATION_LEVELS = ["AUTOCOMMIT", "READ COMMITTED", "READ UNCOMMITTED", "REPEATABLE READ", "SERIALIZABLE"]
FILE_DB_DSN_CONSTANT = "sqlite:///cosmos.db"

# services/lg_bei_info.py
BEI_INFO_CMD_FORMATSTR = '<REQUEST><PRODUCT_ID>{}</PRODUCT_ID><MODEL_NM>{}</MODEL_NM><FW_TYPE>{}</FW_TYPE><IMAGE_VER>{}</IMAGE_VER><IMAGE_REV>{}</IMAGE_REV><KERNEL_VER></KERNEL_VER><ROOTFS_VER></ROOTFS_VER><DEVICE_ID>SENDTESTID</DEVICE_ID><IGNORE_DISABLE>{}</IGNORE_DISABLE><COUNTRY_CODE>KR</COUNTRY_CODE><SCHEME_TYPE>HTTPS</SCHEME_TYPE></REQUEST>'
BEI_INFO_CMD_RESULT_CD = 900
BEI_INFO_CMD_DEFAULT_MSG = "Success"
BEI_INFO_CMD_FAILURE_MSG = "Failure"
BEI_INFO_CMD_DEFAULT_IMAGE_URL_ENDPOINT = '/CdnCheckBEInfoCmd.cbec'
