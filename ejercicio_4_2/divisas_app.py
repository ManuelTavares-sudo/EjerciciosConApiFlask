from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# ExchangeRate-API - Obtén tu API key gratis en https://www.exchangerate-api.com/
# Plan gratuito: 1,500 solicitudes/mes
API_KEY = '3d5da222c9aa6c9de92e8801'
BASE_URL = 'https://v6.exchangerate-api.com/v6'

@app.route('/')
def index():
    return render_template('divisas.html')

@app.route('/api/divisas/tasas/<moneda_base>')
def obtener_tasas(moneda_base):
    try:
        url = f'{BASE_URL}/{API_KEY}/latest/{moneda_base.upper()}'
        response = requests.get(url, timeout=10)
        data = response.json()

        if data.get('result') != 'success':
            return jsonify({'error': data.get('error-type', 'Error al obtener tasas')}), 400

        return jsonify({
            'moneda_base': data['base_code'],
            'tasas': data['conversion_rates'],
            'ultima_actualizacion': data['time_last_update_utc']
        })
    except requests.exceptions.Timeout:
        return jsonify({'error': 'El servicio de tasas tardó demasiado.'}), 504
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/divisas/convertir')
def convertir():
    monto = request.args.get('monto', type=float)
    de = request.args.get('de', 'USD').upper()
    a = request.args.get('a', 'MXN').upper()

    if monto is None or monto <= 0:
        return jsonify({'error': 'Monto válido requerido (mayor a 0)'}), 400

    try:
        url = f'{BASE_URL}/{API_KEY}/pair/{de}/{a}/{monto}'
        response = requests.get(url, timeout=10)
        data = response.json()

        if data.get('result') != 'success':
            return jsonify({'error': data.get('error-type', 'Error en conversión')}), 400

        return jsonify({
            'monto_original': monto,
            'moneda_origen': de,
            'moneda_destino': a,
            'monto_convertido': round(data['conversion_result'], 4),
            'tasa_conversion': data['conversion_rate'],
            'ultima_actualizacion': data['time_last_update_utc']
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/divisas/monedas')
def listar_monedas():
    monedas = {
        'USD': {'nombre': 'Dólar Estadounidense', 'simbolo': '$', 'bandera': '🇺🇸'},
        'EUR': {'nombre': 'Euro', 'simbolo': '€', 'bandera': '🇪🇺'},
        'GBP': {'nombre': 'Libra Esterlina', 'simbolo': '£', 'bandera': '🇬🇧'},
        'JPY': {'nombre': 'Yen Japonés', 'simbolo': '¥', 'bandera': '🇯🇵'},
        'MXN': {'nombre': 'Peso Mexicano', 'simbolo': '$', 'bandera': '🇲🇽'},
        'CAD': {'nombre': 'Dólar Canadiense', 'simbolo': '$', 'bandera': '🇨🇦'},
        'AUD': {'nombre': 'Dólar Australiano', 'simbolo': '$', 'bandera': '🇦🇺'},
        'CHF': {'nombre': 'Franco Suizo', 'simbolo': 'Fr', 'bandera': '🇨🇭'},
        'CNY': {'nombre': 'Yuan Chino', 'simbolo': '¥', 'bandera': '🇨🇳'},
        'BRL': {'nombre': 'Real Brasileño', 'simbolo': 'R$', 'bandera': '🇧🇷'},
        'ARS': {'nombre': 'Peso Argentino', 'simbolo': '$', 'bandera': '🇦🇷'},
        'COP': {'nombre': 'Peso Colombiano', 'simbolo': '$', 'bandera': '🇨🇴'},
        'CLP': {'nombre': 'Peso Chileno', 'simbolo': '$', 'bandera': '🇨🇱'},
        'INR': {'nombre': 'Rupia India', 'simbolo': '₹', 'bandera': '🇮🇳'},
        'KRW': {'nombre': 'Won Coreano', 'simbolo': '₩', 'bandera': '🇰🇷'},
        'SGD': {'nombre': 'Dólar de Singapur', 'simbolo': '$', 'bandera': '🇸🇬'},
    }
    return jsonify(monedas)

@app.route('/api/divisas/historico')
def tasas_historicas():
    """Últimas tasas para múltiples pares desde USD"""
    pares = ['MXN', 'EUR', 'GBP', 'JPY', 'BRL', 'ARS', 'CAD', 'AUD']
    try:
        url = f'{BASE_URL}/{API_KEY}/latest/USD'
        response = requests.get(url, timeout=10)
        data = response.json()

        if data.get('result') != 'success':
            return jsonify({'error': 'No se pudieron obtener las tasas'}), 400

        tasas = data['conversion_rates']
        resultado = {
            moneda: tasas.get(moneda, 0)
            for moneda in pares
            if moneda in tasas
        }
        return jsonify(resultado)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("💰 Conversor de Divisas - ExchangeRate-API")
    print("🔑 Configura tu API_KEY de https://www.exchangerate-api.com/")
    print("🌐 App en: http://127.0.0.1:5000")
    app.run(debug=True)
