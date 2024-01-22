import tensorflow as tf
from tensorflow.keras.utils import load_img
from tensorflow.keras.preprocessing import image
import numpy as np

model = tf.keras.models.load_model('static/fruits360-original-size_model.h5')
classes = np.array(['apple_6', 'apple_braeburn_1', 'apple_crimson_snow_1', 'apple_golden_1', 'apple_golden_2', 'apple_golden_3', 'apple_granny_smith_1', 'apple_hit_1', 'apple_pink_lady_1', 'apple_red_1', 'apple_red_2', 'apple_red_3', 'apple_red_delicios_1', 'apple_red_yellow_1', 'apple_rotten_1', 'cabbage_white_1', 'carrot_1', 'cucumber_1', 'cucumber_3', 'eggplant_violet_1', 'pear_1', 'pear_3', 'zucchini_1', 'zucchini_dark_1'])  # Your complete class list

def get_model():
    return model

def get_classes():
    return classes

def predict_image(img_path):
    img_width, img_height = (100, 100)
    img_path = img_path

    # Load and preprocess the image
    img = load_img(img_path, target_size=(img_width, img_height))
    img_array = image.img_to_array(img)
    img_array = tf.expand_dims(img_array, axis=0)
    img_array = img_array / 255.0  # Make sure this matches the training normalization

    # Make predictions
    predictions = model.predict(img_array)
    predicted_class_index = np.argmax(predictions, axis=1)

    # Map predicted index to class label
    predicted_class_label = classes[predicted_class_index]
    print(predicted_class_label)

    # Confidence
    predicted_confidence = predictions[0][predicted_class_index]
    print(predicted_confidence)

    return [predicted_class_label, predicted_confidence]
