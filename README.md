# 🌱 AI Plant Disease Detection Platform

This project implements a custom Convolutional Neural Network (CNN) model built from scratch for classifying apple plant diseases from leaf images. The model is deployed as a full-stack web application using Flask, featuring JWT authentication and a dynamic frontend. It leverages TensorFlow for inference, PyMongo for user and prediction history management, and is structured for production deployment on cloud platforms like Azure.

## Table of Contents
- [Features](#features)
- [Project Flow](#project-flow)
- [Local Setup](#local-setup)
- [Project Structure](#project-structure)
- [Azure Deployment Guide](#azure-deployment-guide)
  - [Prerequisites](#prerequisites)
  - [1. Set up Azure Cosmos DB (MongoDB API)](#1-set-up-azure-cosmos-db-mongodb-api)
  - [2. Set up Azure Blob Storage for Models](#2-set-up-azure-blob-storage-for-models)
  - [3. Deploy to Azure App Service](#3-deploy-to-azure-app-service)
- [Usage Examples (API & UI)](#usage-examples-api--ui)
- [Requirements](#requirements)

## Features
- **Custom Image Classification**: Utilizes a proprietary CNN built from scratch with TensorFlow/Keras to identify 4 classes: Black rot, Scab, Cedar rust, and Healthy.
- **Secure Authentication**: Provides user registration and login endpoints secured via JSON Web Tokens (JWT).
- **Web API & Dashboard**: A Flask backend serves the RESTful APIs, connected to a Bootstrap 5 frontend featuring asynchronous Javascript (Fetch API) for seamless uploads.
- **Database Integration**: Interacts with MongoDB (via PyMongo) to persistently store user credentials and individual prediction histories.
- **Production-Ready**: Configured with Gunicorn for robust production deployment.
- **Cloud Deployment**: Comprehensive guide for deploying the application to Azure Cloud services.

## Project Flow
1.  **Model Training**: A custom CNN is trained on an augmented dataset of apple leaf images. The trained model (`.keras`) and class mapping (`.json`) are saved as artifacts.
2.  **Authentication**: Users register and log in through the frontend, receiving a JWT access token stored in the browser's `localStorage`.
3.  **Inference API**: The Flask application exposes a `/predict_image` endpoint. It accepts an image, securely verifies the JWT, and saves the file temporarily.
4.  **Prediction & Logging**: The image is preprocessed by the `Image_clf` utility, fed to the CNN, and classified. The result is returned to the user and permanently logged in MongoDB under their profile.
5.  **History Retrieval**: The `/saved_data` API fetches the user's past predictions to populate the dashboard history in real-time.

## Local Setup
To run this project locally, follow these steps:

1.  **Clone the repository**:
    ```bash
    git clone [https://github.com/your-username/Plant_Disease_Detection.git](https://github.com/your-username/Plant_Disease_Detection.git)
    cd Plant_Disease_Detection
    ```

2.  **Create a virtual environment and activate it**:
    ```bash
    python -m venv .venv
    # On Windows
    .venv\Scripts\activate
    # On macOS/Linux
    source .venv/bin/activate
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Prepare your trained model**:
    Ensure your trained model (`Apple_Plant_clf_model.keras`) and class names (`Apple_plnt_class.json`) are placed in the `artifacts/` directory. 

5.  **Set up MongoDB**:
    Ensure you have a MongoDB instance running. Update the MongoDB connection string and JWT Secret Key in your `config.py` or `.env` file.

6.  **Run the Flask application locally**:
    ```bash
    # Set environment variables
    export FLASK_APP=main.py
    export MONGODB_URI="mongodb://localhost:27017/plant_disease_db"
    export JWT_SECRET_KEY="your_super_secret_key"
    
    flask run
    ```
    Alternatively, for a production-like local environment:
    ```bash
    gunicorn -w 4 -b 0.0.0.0:8000 main:app
    ```
    The application will be accessible at `http://localhost:5000` (Flask default) or `http://localhost:8000` (Gunicorn). Navigate to `/login_page` to start.

## Project Structure
Plant_Disease_Detection/
├── .venv/                            # Python virtual environment
├── artifacts/                        # Directory for ML artifacts
│   ├── Apple_Plant_clf_model.keras   # Trained custom CNN model
│   └── Apple_plnt_class.json         # JSON mapping of class names
├── data/                             # Temporary storage for uploaded images during inference
├── src/
│   └── utils.py                      # Contains Image_clf class for preprocessing and prediction
├── static/
│   └── style.css                     # Custom frontend styling (frosted glass, gradients)
├── templates/
│   ├── login.html                    # Authentication UI
│   └── dashboard.html                # Main interface for predictions and history
├── config.py                         # Application configuration and DB initialization
├── main.py                           # Main Flask application and API routing
├── Plant_Dieases_Detection.ipynb     # Original model training and EDA notebook
└── requirements.txt                  # Python dependencies


## Azure Deployment Guide
This guide outlines the steps to deploy the application to Azure using Azure App Service, Azure Cosmos DB (MongoDB API), and Azure Blob Storage.

### Prerequisites
-   An active Azure subscription.
-   Azure CLI installed and configured.
-   Git installed.

### 1. Set up Azure Cosmos DB (MongoDB API)
This will host your MongoDB database for user data and history.

1.  **Create a Cosmos DB account**:
    ```bash
    az cosmosdb create --name <your-cosmosdb-account-name> --resource-group <your-resource-group> --kind MongoDB --locations "East US"=0
    ```

2.  **Retrieve the connection string**:
    ```bash
    az cosmosdb keys list --name <your-cosmosdb-account-name> --resource-group <your-resource-group> --type connection-strings --query connectionStrings[0].connectionString --output tsv
    ```
    Save this string; you will map it to `MONGODB_URI` in your App Service environment variables.

### 2. Set up Azure Blob Storage for Models (Optional but Recommended)
For production, storing heavy `.keras` models in Blob Storage rather than the Git repository is best practice.

1.  **Create a Storage Account & Container**:
    ```bash
    az storage account create --name <your-storage-account-name> --resource-group <your-resource-group> --location "East US" --sku Standard_LRS
    az storage container create --name models --account-name <your-storage-account-name> --public-access off
    ```

2.  **Upload your trained model**:
    ```bash
    az storage blob upload --container-name models --file artifacts/Apple_Plant_clf_model.keras --name Apple_Plant_clf_model.keras --account-name <your-storage-account-name>
    ```

### 3. Deploy to Azure App Service
This will host your Flask backend and serve your HTML templates.

1.  **Create an Azure Web App**:
    ```bash
    az webapp create --resource-group <your-resource-group> --plan <your-app-service-plan> --name <your-webapp-name> --runtime "PYTHON|3.11"
    ```

2.  **Configure environment variables**:
    ```bash
    az webapp config appsettings set --resource-group <your-resource-group> --name <your-webapp-name> --settings MONGODB_URI="<your-cosmosdb-connection-string>" JWT_SECRET_KEY="<generate_a_secure_random_string>"
    ```

3.  **Configure Gunicorn startup command**:
    ```bash
    az webapp config set --resource-group <your-resource-group> --name <your-webapp-name> --startup-file "gunicorn --bind 0.0.0.0 --timeout 600 main:app"
    ```

4.  **Deploy your code via Local Git**:
    ```bash
    az webapp deployment user set --username <your-git-username> --password <your-git-password>
    az webapp deployment source config-local-git --name <your-webapp-name> --resource-group <your-resource-group> --query scmUri --output tsv
    
    # Add remote and push
    git remote add azure <scmUri>
    git push azure master
    ```

## Usage Examples (API & UI)
**Via the Web Interface:**
Navigate to the root URL, log in (or register), and use the UI to upload a leaf image. The Javascript `fetch` API handles the token authorization and DOM updates automatically.

**Via API (cURL Example):**
Assuming you have successfully authenticated and received a JWT token:

```bash
# Export your token
export TOKEN="your_jwt_access_token_here"

# Make a prediction request
curl -X POST https://<your-webapp-name>.azurewebsites.net/predict_image \
  -H "Authorization: Bearer $TOKEN" \
  -F "username=testuser" \
  -F "image=@/path/to/local/apple_scab_leaf.jpg"
Expected Response:

JSON
{
  "status": "success",
  "predicted_class_name": "Scab Plant",
  "message": "Prediction saved successfully"
}
Requirements
Ensure these are in your requirements.txt:

Plaintext
# --- Core Machine Learning ---
tensorflow>=2.10.0
numpy>=1.23.5
Pillow>=10.0.0

# --- Web Framework & API ---
Flask==3.0.0
Werkzeug==3.0.0
PyJWT==2.8.0

# --- Database ---
pymongo==4.6.1

# --- Production Deployment ---
gunicorn==21.2.0