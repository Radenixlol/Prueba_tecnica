import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("config\prueba-tecnica-89152-firebase-adminsdk-q2r7f-b773959d06.json")
firebase_admin.initialize_app(cred)

db = firestore.client()