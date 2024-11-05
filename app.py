from flask import Flask, render_template, request, jsonify
import requests
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

def get_weather(city=None, lat=None, lon=None):
    api_key = os.getenv('WEATHER_API_KEY')
    if city:
        base_url = "http://api.weatherapi.com/v1/current.json?"
        complete_url = f"{base_url}key={api_key}&q={city}"
    else:
        base_url = "http://api.weatherapi.com/v1/current.json?"
        complete_url = f"{base_url}key={api_key}&q={lat},{lon}"
    response = requests.get(complete_url)
    return response.json()

def parse_weather_data(data):
    if "error" not in data:
        current = data["current"]
        location = data["location"]
        condition = current["condition"]

        return {
            "city": location["name"],
            "temperature": current["temp_c"],
            "humidity": current["humidity"],
            "pressure": current["pressure_mb"],
            "wind_speed": current["wind_kph"],
            "description": condition["text"],
            "icon": condition["icon"]
        }
    else:
        return None

@app.route('/', methods=['GET', 'POST'])
def index():
    weather = None
    if request.method == 'POST':
        city = request.form['city']
        data = get_weather(city=city)
        weather = parse_weather_data(data)

    return render_template('index.html', weather=weather)

@app.route('/location', methods=['POST'])
def location():
    data = request.json
    lat = data.get('latitude')
    lon = data.get('longitude')
    weather_data = get_weather(lat=lat, lon=lon)
    weather = parse_weather_data(weather_data)
    return jsonify({
        'city': weather['city'] if weather else 'Unknown'
    })

if __name__ == '__main__':
    app.run(debug=True)
