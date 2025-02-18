import os

from firebase_admin import credentials, firestore, initialize_app, get_app

class FirebaseConfig:
    def __init__(self):
        self.db = self._initialize_firebase()
        self.user_collection = self.db.collection(u'users')
        self.products_collection = self.db.collection(u'products')

    def _initialize_firebase(self)-> firestore.client:
        url = os.path.join("./keys/credentials_firestore.json")

        cred = credentials.Certificate(url)
        initialize_app(cred)

        return firestore.client()
    
    def get_collection(self, collection_name:str)->firestore.CollectionReference:
        return self.db.collection(collection_name)

firebase = FirebaseConfig() 
user_collection = firebase.user_collection
products_collection = firebase.products_collection

    
    
    

        
        