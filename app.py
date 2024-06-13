# from flask import Flask

# app = Flask(__name__)

# @app.route('/')
# def hello():
#     return 'Hello, World!'

# if __name__ == '__main__':
#     app.run(debug=True)

from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# OpenWeatherMap API key
API_KEY = '0508d2db089889c03892c245e506b540'  # takes 45 mins to activate key

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/weather', methods=['POST'])
def weather():
    # Get the location typed into the search bar
    location = request.form['location']
    
    # Call the OpenWeatherMap API to get the weather data for the location
    url = f'http://api.openweathermap.org/data/2.5/weather?q={location}&appid={API_KEY}'
    response = requests.get(url)
    data = response.json()

    print("data",data)
    
    # Extract relevant weather information
    if data['cod'] == 200:
        weather_data = {
            'city': data['name'],
            'temperature': round(data['main']['temp'] - 273.15, 2),  # Convert temperature from Kelvin to Celsius
            'description': data['weather'][0]['description'].capitalize(),
            'icon': data['weather'][0]['icon']
        }
        return render_template('weather.html', weather_data=weather_data)
    else:
        error_message = f'Error: {data["message"]}'
        return render_template('error.html', error_message=error_message)

if __name__ == '__main__':
    app.run(debug=True)
