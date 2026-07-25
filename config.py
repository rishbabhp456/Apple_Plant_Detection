import os

FLASK_HOST = '0.0.0.0'
FLASK_PORT = 8000
MONGO_URL = 'mongodb://localhost:27017/'

db_name = 'image_clf'
collection_user = 'clf_users'
collection_data = 'Plant_Data'

MODEL_PATH = os.path.join(os.getcwd(),"artifacts","Apple_Plant_clf_model.keras")
MODEL_CONFIG = os.path.join(os.getcwd(),"artifacts","Apple_plnt_class.json")
