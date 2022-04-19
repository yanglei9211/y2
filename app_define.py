CODE_2_SUBJECT = {
    'chinese': {2: 101, 3: 201, 4: 301},
    'math': {2: 102, 3: 202, 4: 302},
    'english': {2: 103, 3:203, 4: 303},
    'physics': {3: 204, 4: 304},
    'chemistry': {3: 205, 4: 305},
    'biology': {3: 206, 4: 306},
    'politics': {3: 207, 4: 307},
    'geography': {3: 208, 4: 308},
    'history': {3: 209, 4: 309}
}

USER_ROLE_USER = 1 << 0  # 账号权限
USER_ROLE_FIRST = 1 << 1 # 测试接口权限
USER_ROLE_DATA = 1 << 2 # 内容数据权限
USER_ROLE_MANAGER = USER_ROLE_USER | USER_ROLE_FIRST | USER_ROLE_DATA

VALID_ROLES = [USER_ROLE_MANAGER, USER_ROLE_FIRST, USER_ROLE_USER, USER_ROLE_DATA]
