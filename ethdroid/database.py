from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError, ConnectionFailure

from ethdroid.config import MONGO_DB_NAME, MONGO_DB_COLLECTION


class MongoDatabase:

    connectionOK = False

    def __init__(self):

        self.client = MongoClient(serverSelectionTimeoutMS=10000)

        try:
            self.client.admin.command('ismaster')
            self.db = self.client[MONGO_DB_NAME]

            if MONGO_DB_COLLECTION in self.db.collection_names():

                self.collection = self.db[MONGO_DB_COLLECTION]
                self.connectionOK = True

        except ServerSelectionTimeoutError or ConnectionFailure:
            print("Server not available")

    def insert_user(self, usr_tg_id, usr_tg_alias='', usr_lang_code='', usr_bot_state=''):

        self.collection.insert({"usr_tg_id": usr_tg_id,
                                "usr_tg_alias": usr_tg_alias,
                                "usr_lang_code": usr_lang_code,
                                "usr_bot_state": usr_bot_state,
                                "usr_wallets": ()
                                })

    def get_user(self, usr_tg_id):

        user = self.collection.find_one({'usr_tg_id': usr_tg_id})
        return user

    def edit_user(self, user):

        self.collection.save(user)

    def get_all_users(self):

        users = self.collection.find()
        return users
