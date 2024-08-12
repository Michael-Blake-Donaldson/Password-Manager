from pymongo import MongoClient

class Database:
    def __init__(self):
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client['password_manager']
        self.passwords_collection = self.db['passwords']
        self.master_collection = self.db['master_password']  # Collection for storing master password and key

    def insert_password(self, data):
        self.passwords_collection.insert_one(data)

    def get_all_passwords(self):
        return list(self.passwords_collection.find({}))

    def find_password(self, query):
        return self.passwords_collection.find_one(query)

    def delete_password(self, query):
        self.passwords_collection.delete_one(query)

    def update_password(self, query, new_data):
        self.passwords_collection.update_one(query, {'$set': new_data})

    def store_master_password(self, encrypted_password, key):
        # Clear any existing master password before storing a new one
        self.master_collection.delete_many({})
        self.master_collection.insert_one({"master_password": encrypted_password, "key": key})

    def get_master_password(self):
        return self.master_collection.find_one({})
