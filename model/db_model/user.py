from model.db_model.base_model import BaseDbModel
from model.db_model.mongodb import get_client


class UserDbModel(BaseDbModel):
    DB = 'klx_migrate'
    TBL = 'user'

    @classmethod
    def find_by_username(cls, username):
        col = get_client()[cls.DB][cls.TBL]
        ret = col.find_one({'username': username})
        return ret

    @classmethod
    def update_user_by_username(cls, username, updata, upsert=False):
        col = get_client()[cls.DB][cls.TBL]
        col.update_one({'username': username}, {'$set': updata}, upsert=upsert)
        return True

    @classmethod
    def get_user_list(cls):
        col = get_client()[cls.DB][cls.TBL]
        ret = col.find()
        ret = list(ret)
        return ret
