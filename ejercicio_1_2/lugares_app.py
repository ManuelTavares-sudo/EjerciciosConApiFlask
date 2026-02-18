from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('lugares.html')

@app.route('/api/lugares')
def buscar_lugares():
    lat = request.args.get('lat', type=float)
    lon = request.args.get('lon', type=float)
    tipo = request.args.get('tipo', 'restaurant')
    radio = request.args.get('radio', 1000, type=int)

    if not lat or not lon:
        return jsonify({'error': 'Latitud y longitud requeridas'}), 400

    # Mapeo de tipos a queries de OSM
    tipos_osm = {
        'restaurant': 'amenity=restaurant',
        'hospital': 'amenity=hospital',
        'cafe': 'amenity=cafe',
        'farmacia': 'amenity=pharmacy',
        'tienda': 'shop=supermarket',
        'gasolinera': 'amenity=fuel',
        'banco': 'amenity=bank',
        'hotel': 'tourism=hotel'
    }

    query = tipos_osm.get(tipo, 'amenity=restaurant')

    overpass_url = "https://overpass-api.de/api/interpreter"
    overpass_query = f"""
[out:json][timeout:25];
(
  node[{query}](around:{radio},{lat},{lon});
  way[{query}](around:{radio},{lat},{lon});
);
out center;
"""

    try:
        response = requests.get(
            overpass_url,
            params={'data': overpass_query},
            timeout=30
        )
        data = response.json()

        lugares = []
        for elemento in data['elements'][:20]:
            if 'center' in elemento:
                coords = elemento['center']
            elif 'lat' in elemento:
                coords = {'lat': elemento['lat'], 'lon': elemento['lon']}
            else:
                continue

            tags = elemento.get('tags', {})

            # Calcular distancia aproximada (Haversine simplificado)
            import math
            dlat = math.radians(coords['lat'] - lat)
            dlon = math.radians(coords['lon'] - lon)
            a = math.sin(dlat/2)**2 + math.cos(math.radians(lat)) * math.cos(math.radians(coords['lat'])) * math.sin(dlon/2)**2
            distancia = round(6371000 * 2 * math.asin(math.sqrt(a)))

            direccion = ' '.join(filter(None, [
                tags.get('addr:street', ''),
                tags.get('addr:housenumber', '')
            ])).strip()

            lugares.append({
                'nombre': tags.get('name', 'Sin nombre'),
                'direccion': direccion or 'Dirección no disponible',
                'lat': coords['lat'],
                'lon': coords['lon'],
                'tipo': tags.get('amenity') or tags.get('shop') or tags.get('tourism', ''),
                'telefono': tags.get('phone', ''),
                'horario': tags.get('opening_hours', ''),
                'distancia': distancia,
                'website': tags.get('website', '')
            })

        # Ordenar por distancia
        lugares.sort(key=lambda x: x['distancia'])
        return jsonify(lugares)

    except requests.exceptions.Timeout:
        return jsonify({'error': 'La búsqueda tardó demasiado. Intenta con un radio menor.'}), 504
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("📍 Buscador de Lugares - http://127.0.0.1:5000")
    app.run(debug=True)
