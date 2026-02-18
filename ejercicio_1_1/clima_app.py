from flask import Flask, render_template, jsonify
import requests

app = Flask(__name__)

# Reemplaza con tu API key de OpenWeatherMap
WEATHER_API_KEY = '402d8ebf0c899a2fdbb786e4a0c6814d'

@app.route('/')
def index():
    return render_template('clima.html')

@app.route('/api/clima')
def obtener_clima():
    try:
        # 1. Obtener ubicación por IP
        ip_response = requests.get('https://ipapi.co/json/', timeout=10)
        ubicacion = ip_response.json()
        ciudad = ubicacion.get('city', 'Ciudad desconocida')
        lat = ubicacion.get('latitude')
        lon = ubicacion.get('longitude')

        # 2. Obtener clima de esa ubicación
        weather_url = 'https://api.openweathermap.org/data/2.5/weather'
        params = {
            'lat': lat,
            'lon': lon,
            'appid': WEATHER_API_KEY,
            'units': 'metric',
            'lang': 'es'
        }
        clima_response = requests.get(weather_url, params=params, timeout=10)
        clima = clima_response.json()

        if clima_response.status_code != 200:
            return jsonify({'error': clima.get('message', 'Error al obtener clima')}), 400

        resultado = {
            'ciudad': ciudad,
            'pais': ubicacion.get('country_name'),
            'temperatura': round(clima['main']['temp'], 1),
            'sensacion': round(clima['main']['feels_like'], 1),
            'descripcion': clima['weather'][0]['description'].capitalize(),
            'humedad': clima['main']['humidity'],
            'viento': clima['wind']['speed'],
            'icono': clima['weather'][0]['icon'],
            'temp_min': round(clima['main']['temp_min'], 1),
            'temp_max': round(clima['main']['temp_max'], 1),
            'presion': clima['main']['pressure'],
            'lat': lat,
            'lon': lon
        }
        return jsonify(resultado)
    except requests.exceptions.Timeout:
        return jsonify({'error': 'Tiempo de espera agotado. Intenta de nuevo.'}), 504
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("🌍 Clima App - http://127.0.0.1:5000")
    print("⚠️  Recuerda configurar WEATHER_API_KEY con tu API key de OpenWeatherMap")
    app.run(debug=True)
