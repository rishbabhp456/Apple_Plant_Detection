import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # Suppresses unneeded compiled optimization warnings
from flask import Flask, jsonify, request,render_template, redirect, url_for, session
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from src.uitls import Image_clf
from werkzeug.utils import secure_filename
import config
import pymongo
import datetime


client = pymongo.MongoClient(config.MONGO_URL)
db = client[config.db_name]
plant_collection = db[config.collection_data]
user_collection = db[config.collection_user]

obj_image_clf = Image_clf()


app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = 'secret'
app.config["SECRET_KEY"] = "flask-session-secret"
jwt = JWTManager(app)


@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login_page')
def login_page():
    return render_template('login.html')


@app.route('/register_page')
def register_page():
    return render_template('register.html')


@app.route('/forgot_password_page')
def forgot_password_page():
    return render_template('forget_password.html')


@app.route('/dashboard_page')
def dashboard_page():
    return render_template('dashboard.html')


@app.route('/register', methods=['POST'])
def register():
    data = request.form
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    dob = data.get('dob')
    response = user_collection.find_one({"username": username},{"email": email})
    if not response:
        user_collection.insert_one({"username": username, "password": password, "email": email, "dob": dob})
        return jsonify({"message": "User registered successfully!"})
    else:
        return jsonify({"message": "User already exists!"})



@app.route('/login', methods=['POST'])
def login():
    data = request.form
    username = data.get('username') 
    password = data.get('password')
    response = user_collection.find_one({"username": username, "password": password})

    if response:
        access_token = create_access_token(identity=username,
                                            expires_delta= datetime.timedelta(minutes=5))
        return jsonify({"status": "success","message": "Login Successful", 
                        "access_token":access_token})
    else:
        return jsonify({"status": "failure", "message": "Invalid Credentials"})
    


@app.route("/forget_password", methods=["POST"])
def forget_password():
    data = request.form
    username = data.get('username')
    email = data.get('email')
    new_password = data.get('new_password')

    response = user_collection.find_one({"username": username, "email": email})
    if response:
        user_collection.update_one({"username": username, "email": email}, {"$set": {"password": new_password}})
        return jsonify({"status": "success", "message": "Password updated successfully"})
    else:
        return jsonify({"status": "failure", "message": "Invalid username or email"})
    

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    if request.method == 'POST':
        return jsonify({"status": "success", "message": "Logged out successfully"})
    return redirect(url_for('login_page'))


@app.route("/predict_image", methods=["POST"])
def predict_image():

    username = request.form.get('username', 'anonymous')
    """Check input image file"""
    if 'image' not in request.files:
        return jsonify({"status": "failure", "message": "No image file provided"}), 400

    file = request.files['image']

    """check if file exists"""
    if file:
        try:
            """clean and store file in temporary storage"""
            filename = secure_filename(file.filename)
            temp_path = os.path.join("data", filename)
            file.save(temp_path)

            predicted_class_name, prediction_list = obj_image_clf.predict_image(temp_path)

            """Remove temporary file"""
            if os.path.exists(temp_path):
                os.remove(temp_path)

            """Save the Predictions"""
            prediction_record = {
                "username": username,
                "image_name": filename,
                "predicted_disease": predicted_class_name,
                "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            plant_collection.insert_one(prediction_record)

            return jsonify({"status": "success", "predicted_class_name": predicted_class_name, "prediction_list": prediction_list})

        except Exception as e:
            if os.path.exists(temp_path):
                os.remove(temp_path)
            return jsonify({"status": "failure", "message": str(e)}), 500
    else:
        return jsonify({"status": "failure", "message": "An An unexpected error occurred"}), 500


@app.route("/saved_data", methods=["GET"])
def saved_data():
    username = request.args.get('username')
    response = user_collection.find_one({"username": username})
    
    if response:
        # Fetch data and return it using the key "history" so the frontend can read it
        user_history = list(plant_collection.find({"username": username}, {"_id": 0}))
        return jsonify({"status": "success", "history": user_history})
    
    # Return empty history if user is not found
    return jsonify({"status": "success", "message": "No previous predictions found", "history": []})

    
if __name__ == "__main__":
    app.run(host= config.FLASK_HOST, port= config.FLASK_PORT, debug= True)