# app/firebase_admin_init.py
import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate("./yot-firebase-firebase-adminsdk-fbsvc-5adc144e23.json")
firebase_admin.initialize_app(cred)
