# views.py
from django.shortcuts import render, redirect
from django.http import JsonResponse
import openai
from weather_forecast.utils.utils import *
import requests
import os
from django.http import JsonResponse
# Initialize OpenAI API
openai.api_key = "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"

def dummy(request):
    return render(request,'dummy.html')

import requests

def fetch_weather_data(location):
    weather_api_key = "e4467eceef2a35e625ad1f069efed92d"
    
    weather_api_base_url = "http://api.weatherstack.com/current?"
    params = {
        "access_key": weather_api_key,
        "query": location,
    }
    
    try:
        response = requests.get(weather_api_base_url, params=params)
        response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
        data = response.json()

        # Check if the response is successful and contains the 'current' key
        if "error" in data:
            print("Error:", data["error"]["info"])
            return None
        elif "current" in data:
            print(data)
            return data
        else:
            print("Error: Invalid response data.")
            return None
    except requests.exceptions.RequestException as e:
        print("Error:", e)
        return None


openai.organization = "org-k6eSOJlxXp6k1velCYNxATGA"
openai.api_key = os.getenv("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")

def list_engines(request):
    try:
        engines_data = openai.Engine.list()
        return JsonResponse(engines_data, safe=False)
    except Exception as e:
        return JsonResponse({"error": str(e)})

def get_gpt_response(prompt):
    try:
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            max_tokens=200,
        )
        return response.choices[0].text.strip()
    except Exception as e:
        # Handle any errors that might occur during the API call
        return "Error: AI response not available"



def weather_forecast(request):
    if request.method == "POST":
        location = request.POST.get("location")
        question = request.POST.get("question")

        # Fetch weather data using the third-party weather API
        weather_data = fetch_weather_data(location)

        if weather_data:
            # Access 'current' key only if it exists in the weather_data dictionary
            current_data = weather_data.get("current")
            if current_data:
                # Access temperature, humidity, and weather description
                current_temp = current_data.get("temp_c")
                humidity = current_data.get("humidity")
                weather_description = current_data.get("condition").get("text")
            else:
                # Handle the case when 'current' key is not present in the weather_data dictionary
                current_temp = "N/A"
                humidity = "N/A"
                weather_description = "N/A"
        else:
            # Handle the case when weather_data is None (i.e., an error occurred with the API response)
            current_temp = "Error"
            humidity = "Error"
            weather_description = "Error"

        # Compose a prompt for ChatGPT
        prompt = f"Today's weather in {location} is {weather_description} with a temperature of {current_temp}°C and humidity at {humidity}%.\n"
        prompt += question

        # Get AI response using ChatGPT API
        ai_response = get_gpt_response(prompt)

        # Save the user query and ChatGPT response
        #save_user_query(location, question, ai_response)
        d={"location": location, "weather_data": weather_data,
            "current_temp": current_temp,
            "humidity": humidity,
            "weather_description": weather_description,
            "ai_response": ai_response}
        
        return render(request, "result.html", d)

    return render(request, "index.html")
