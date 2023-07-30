# utils.py
import requests
from sklearn.linear_model import LinearRegression
from joblib import load
from weather_forecast.models import UserQuery


    


'''
def save_user_query(location, question, ai_response):
    # Implement the logic to save the user's query and AI response
    # You can use Django models or any other storage mechanism to save this data
    # For example, if you have a Django model named "UserQuery", you can do something like this:
    
    user_query = UserQuery(location=location, question=question, ai_response=ai_response)
    user_query.save()
'''


def load_trained_model():
    # Assuming you've saved the trained model using joblib or another serialization method
    # Modify the file path based on the actual location and format of your trained model file
    model_file_path = "/path/to/your/trained/model.pkl"
    loaded_model = load(model_file_path)
    return loaded_model


def make_weather_prediction(features):
  
    model = load_trained_model() 
    X = [[features['temperature'], features['humidity']]]

    prediction = model.predict(X)

    return prediction[0]  