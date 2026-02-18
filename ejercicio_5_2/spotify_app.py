from flask import Flask, render_template, request, jsonify, session
import requests
import base64
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = 'clave_secreta_spotify_app_2024'

# Spotify API Credentials - obtener en https://developer.spotify.com/dashboard
CLIENT_ID = 'TU_CLIENT_ID_AQUI'
CLIENT_SECRET = 'TU_CLIENT_SECRET_AQUI'

SPOTIFY_TOKEN_URL = 'https://accounts.spotify.com/api/token'
SPOTIFY_API_URL = 'https://api.spotify.com/v1'

def get_access_token():
    if 'access_token' in session and 'token_expiry' in session:
        if datetime.now() < datetime.fromisoformat(session['token_expiry']):
            return session['access_token']
    auth_string = f"{CLIENT_ID}:{CLIENT_SECRET}"
    auth_base64 = base64.b64encode(auth_string.encode('utf-8')).decode('utf-8')
    headers = {'Authorization': f'Basic {auth_base64}', 'Content-Type': 'application/x-www-form-urlencoded'}
    try:
        response = requests.post(SPOTIFY_TOKEN_URL, headers=headers, data={'grant_type': 'client_credentials'}, timeout=10)
        if response.status_code != 200:
            return None
        token_data = response.json()
        session['access_token'] = token_data['access_token']
        session['token_expiry'] = (datetime.now() + timedelta(seconds=token_data['expires_in'] - 60)).isoformat()
        return token_data['access_token']
    except Exception as e:
        print(f"Error al obtener token: {e}")
        return None

@app.route('/')
def index():
    return render_template('spotify.html')

@app.route('/api/spotify/buscar')
def buscar_spotify():
    query = request.args.get('q', '')
    tipo = request.args.get('tipo', 'track')
    limite = request.args.get('limite', 20, type=int)
    if not query:
        return jsonify({'error': 'Consulta requerida'}), 400
    token = get_access_token()
    if not token:
        return jsonify({'error': 'Error al autenticar con Spotify'}), 500
    try:
        headers = {'Authorization': f'Bearer {token}'}
        params = {'q': query, 'type': tipo, 'limit': limite, 'market': 'MX'}
        response = requests.get(f'{SPOTIFY_API_URL}/search', headers=headers, params=params, timeout=10)
        if response.status_code != 200:
            return jsonify({'error': f'Error Spotify: {response.status_code}'}), 500
        data = response.json()
        resultados = []
        if tipo == 'track':
            for track in data.get('tracks', {}).get('items', []):
                resultados.append({
                    'id': track['id'], 'nombre': track['name'],
                    'artistas': [a['name'] for a in track['artists']],
                    'artista_principal': track['artists'][0]['name'] if track['artists'] else '',
                    'album': track['album']['name'],
                    'imagen': track['album']['images'][0]['url'] if track['album']['images'] else None,
                    'duracion': f"{track['duration_ms']//60000}:{(track['duration_ms']%60000)//1000:02d}",
                    'preview_url': track['preview_url'],
                    'spotify_url': track['external_urls']['spotify'],
                    'popularidad': track['popularity'], 'explicito': track['explicit']
                })
        elif tipo == 'artist':
            for artist in data.get('artists', {}).get('items', []):
                resultados.append({
                    'id': artist['id'], 'nombre': artist['name'],
                    'generos': artist['genres'], 'popularidad': artist['popularity'],
                    'imagen': artist['images'][0]['url'] if artist['images'] else None,
                    'seguidores': artist['followers']['total'],
                    'spotify_url': artist['external_urls']['spotify']
                })
        elif tipo == 'album':
            for album in data.get('albums', {}).get('items', []):
                resultados.append({
                    'id': album['id'], 'nombre': album['name'],
                    'artistas': [a['name'] for a in album['artists']],
                    'fecha_lanzamiento': album['release_date'],
                    'total_tracks': album['total_tracks'],
                    'imagen': album['images'][0]['url'] if album['images'] else None,
                    'spotify_url': album['external_urls']['spotify'], 'tipo': album['album_type']
                })
        elif tipo == 'playlist':
            for playlist in data.get('playlists', {}).get('items', []):
                if playlist:
                    resultados.append({
                        'id': playlist['id'], 'nombre': playlist['name'],
                        'descripcion': playlist.get('description', ''),
                        'owner': playlist['owner']['display_name'],
                        'total_tracks': playlist['tracks']['total'],
                        'imagen': playlist['images'][0]['url'] if playlist.get('images') else None,
                        'spotify_url': playlist['external_urls']['spotify'],
                        'publica': playlist.get('public', True)
                    })
        return jsonify(resultados)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/spotify/artista/<artist_id>')
def info_artista(artist_id):
    token = get_access_token()
    if not token:
        return jsonify({'error': 'Error al autenticar'}), 500
    try:
        headers = {'Authorization': f'Bearer {token}'}
        artist = requests.get(f'{SPOTIFY_API_URL}/artists/{artist_id}', headers=headers, timeout=10).json()
        top_tracks = requests.get(f'{SPOTIFY_API_URL}/artists/{artist_id}/top-tracks', headers=headers, params={'market': 'MX'}, timeout=10).json().get('tracks', [])
        albums = requests.get(f'{SPOTIFY_API_URL}/artists/{artist_id}/albums', headers=headers, params={'limit': 10, 'market': 'MX'}, timeout=10).json().get('items', [])
        related = requests.get(f'{SPOTIFY_API_URL}/artists/{artist_id}/related-artists', headers=headers, timeout=10).json().get('artists', [])
        resultado = {
            'id': artist['id'], 'nombre': artist['name'], 'generos': artist['genres'],
            'popularidad': artist['popularity'], 'seguidores': artist['followers']['total'],
            'imagen': artist['images'][0]['url'] if artist['images'] else None,
            'spotify_url': artist['external_urls']['spotify'],
            'top_canciones': [{'id': t['id'], 'nombre': t['name'], 'album': t['album']['name'],
                'preview': t['preview_url'], 'imagen': t['album']['images'][0]['url'] if t['album']['images'] else None,
                'duracion': f"{t['duration_ms']//60000}:{(t['duration_ms']%60000)//1000:02d}",
                'spotify_url': t['external_urls']['spotify']} for t in top_tracks[:10]],
            'albums': [{'id': a['id'], 'nombre': a['name'], 'fecha': a['release_date'],
                'imagen': a['images'][0]['url'] if a['images'] else None,
                'total_tracks': a['total_tracks'], 'tipo': a['album_type']} for a in albums],
            'artistas_relacionados': [{'id': r['id'], 'nombre': r['name'],
                'imagen': r['images'][0]['url'] if r['images'] else None,
                'popularidad': r['popularity']} for r in related[:6]]
        }
        return jsonify(resultado)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/spotify/album/<album_id>')
def info_album(album_id):
    token = get_access_token()
    if not token:
        return jsonify({'error': 'Error al autenticar'}), 500
    try:
        headers = {'Authorization': f'Bearer {token}'}
        album = requests.get(f'{SPOTIFY_API_URL}/albums/{album_id}', headers=headers, params={'market': 'MX'}, timeout=10).json()
        resultado = {
            'id': album['id'], 'nombre': album['name'],
            'artistas': [a['name'] for a in album['artists']],
            'fecha_lanzamiento': album['release_date'], 'total_tracks': album['total_tracks'],
            'imagen': album['images'][0]['url'] if album['images'] else None,
            'generos': album.get('genres', []), 'sello': album.get('label', ''),
            'popularidad': album['popularity'], 'spotify_url': album['external_urls']['spotify'],
            'tracks': [{'numero': t['track_number'], 'nombre': t['name'],
                'duracion': f"{t['duration_ms']//60000}:{(t['duration_ms']%60000)//1000:02d}",
                'preview': t['preview_url'], 'spotify_url': t['external_urls']['spotify']}
                for t in album['tracks']['items']]
        }
        return jsonify(resultado)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("=" * 60)
    print("🎵 Buscador de Música - Spotify Web API")
    print("=" * 60)
    if CLIENT_ID == 'TU_CLIENT_ID_AQUI':
        print("⚠️  ADVERTENCIA: Reemplaza CLIENT_ID y CLIENT_SECRET")
        print("   Obtén tus credenciales en:")
        print("   https://developer.spotify.com/dashboard")
    else:
        print(f"✅ Client ID configurado: {CLIENT_ID[:20]}...")
    print("🌐 Servidor corriendo en: http://127.0.0.1:5001")
    print("=" * 60)
    app.run(debug=True, port=5001)
