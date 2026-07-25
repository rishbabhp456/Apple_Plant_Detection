import config
import keras, json
import numpy as np  # Don't forget to import numpy for argmax!
from keras.preprocessing import image

class Image_clf:
    def __init__(self):
        # 1. Load the model ONCE when the app starts
        self.load_model()

    def load_model(self):
        """---Load model file----"""
        self.model = keras.models.load_model(config.MODEL_PATH)
        
        """ ---- Load model Class----"""
        with open(config.MODEL_CONFIG, 'r') as f:
            self.class_names = json.load(f)

    def preprocess_image(self, input_img): 
        """Load and preprocess image"""
        img = image.load_img(input_img, target_size=(224, 224))
        img_array = image.img_to_array(img)
        img_array = img_array / 255.0
        
        self.test_array = img_array.reshape(1, 224, 224, 3)
        return self.test_array

    def predict_image(self, input_img):
        """Preprocess image"""
        self.preprocessed_image = self.preprocess_image(input_img)

        """Predict image"""
        self.prediction = self.model.predict(self.preprocessed_image)

        # Get the index of the highest probability
        predicted_class_index = np.argmax(self.prediction)
        
        # 2. JSON keys are strings! We must convert the integer index to a string to avoid a KeyError
        self.predicted_class_name = self.class_names[predicted_class_index]
        
        # 3. Convert Numpy array to a standard Python list so Flask can return it as JSON
        prediction_list = self.prediction.tolist()
        
        return self.predicted_class_name, prediction_list