import os

FLASK_HOST = '0.0.0.0'
FLASK_PORT = 8000
MONGO_PASSWORD = 'test123$'
MONGO_URL = f'mongodb+srv://rishabhp:{MONGO_PASSWORD}@docdb-cluster-20260630-0923.global.mongocluster.cosmos.azure.com/?tls=true&authMechanism=SCRAM-SHA-256&retrywrites=false&maxIdleTimeMS=120000'
db_name = 'image_clf'
collection_user = 'clf_users'
collection_data = 'Plant_Data'

MODEL_PATH = os.path.join(os.getcwd(),"artifacts","Apple_Plant_clf_model.keras")
MODEL_CONFIG = os.path.join(os.getcwd(),"artifacts","Apple_plnt_class.json")
