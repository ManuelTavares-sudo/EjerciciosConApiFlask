from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

GITHUB_API = 'https://api.github.com'
HEADERS = {
    'Accept': 'application/vnd.github.v3+json',
    'User-Agent': 'FlaskApp/1.0'
}

@app.route('/')
def index():
    return render_template('github.html')

@app.route('/api/github/usuario/<username>')
def obtener_usuario_github(username):
    try:
        # Información del usuario
        user_response = requests.get(f'{GITHUB_API}/users/{username}', headers=HEADERS, timeout=10)
        if user_response.status_code == 404:
            return jsonify({'error': f'Usuario "{username}" no encontrado'}), 404
        if user_response.status_code == 403:
            return jsonify({'error': 'Rate limit de GitHub alcanzado. Espera unos minutos.'}), 403

        usuario = user_response.json()

        # Repositorios
        repos_response = requests.get(
            f'{GITHUB_API}/users/{username}/repos',
            headers=HEADERS,
            params={'per_page': 100, 'sort': 'updated'},
            timeout=10
        )
        repos = repos_response.json() if repos_response.status_code == 200 else []

        # Estadísticas
        total_stars = sum(repo.get('stargazers_count', 0) for repo in repos)
        total_forks = sum(repo.get('forks_count', 0) for repo in repos)
        total_watchers = sum(repo.get('watchers_count', 0) for repo in repos)

        # Lenguajes
        lenguajes = {}
        for repo in repos:
            lang = repo.get('language')
            if lang:
                lenguajes[lang] = lenguajes.get(lang, 0) + 1

        top_lenguajes = sorted(lenguajes.items(), key=lambda x: x[1], reverse=True)[:5]

        resultado = {
            'nombre': usuario.get('name') or username,
            'username': usuario['login'],
            'bio': usuario.get('bio'),
            'avatar': usuario['avatar_url'],
            'repositorios': usuario.get('public_repos', 0),
            'seguidores': usuario.get('followers', 0),
            'siguiendo': usuario.get('following', 0),
            'gists': usuario.get('public_gists', 0),
            'ubicacion': usuario.get('location'),
            'empresa': usuario.get('company'),
            'blog': usuario.get('blog'),
            'twitter': usuario.get('twitter_username'),
            'creado': usuario['created_at'][:10],
            'profile_url': usuario['html_url'],
            'total_stars': total_stars,
            'total_forks': total_forks,
            'total_watchers': total_watchers,
            'lenguajes': dict(lenguajes),
            'top_lenguajes': [{'lenguaje': l[0], 'repos': l[1]} for l in top_lenguajes],
            'repos_destacados': [
                {
                    'nombre': repo['name'],
                    'descripcion': repo.get('description') or 'Sin descripción',
                    'stars': repo.get('stargazers_count', 0),
                    'forks': repo.get('forks_count', 0),
                    'lenguaje': repo.get('language'),
                    'url': repo['html_url'],
                    'actualizado': repo.get('updated_at', '')[:10],
                    'topics': repo.get('topics', [])[:3]
                }
                for repo in sorted(repos, key=lambda x: x.get('stargazers_count', 0), reverse=True)[:6]
            ]
        }
        return jsonify(resultado)
    except requests.exceptions.Timeout:
        return jsonify({'error': 'GitHub tardó demasiado en responder.'}), 504
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/github/trending')
def repositorios_trending():
    from datetime import datetime, timedelta
    fecha = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
    lenguaje = request.args.get('lenguaje', '')

    query = f'created:>{fecha}'
    if lenguaje:
        query += f' language:{lenguaje}'

    params = {
        'q': query,
        'sort': 'stars',
        'order': 'desc',
        'per_page': 10
    }
    try:
        response = requests.get(f'{GITHUB_API}/search/repositories', headers=HEADERS, params=params, timeout=10)
        data = response.json()
        repos = [
            {
                'nombre': repo['full_name'],
                'descripcion': repo.get('description') or 'Sin descripción',
                'stars': repo['stargazers_count'],
                'forks': repo['forks_count'],
                'lenguaje': repo.get('language'),
                'url': repo['html_url'],
                'propietario': repo['owner']['login'],
                'avatar': repo['owner']['avatar_url'],
                'topics': repo.get('topics', [])[:3]
            }
            for repo in data.get('items', [])
        ]
        return jsonify(repos)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/github/buscar/repos')
def buscar_repos():
    query = request.args.get('q', '')
    lenguaje = request.args.get('lenguaje', '')
    if not query:
        return jsonify({'error': 'Consulta requerida'}), 400

    search_query = query
    if lenguaje:
        search_query += f' language:{lenguaje}'

    params = {'q': search_query, 'sort': 'stars', 'order': 'desc', 'per_page': 12}
    try:
        response = requests.get(f'{GITHUB_API}/search/repositories', headers=HEADERS, params=params, timeout=10)
        data = response.json()
        repos = [
            {
                'nombre': repo['full_name'],
                'descripcion': repo.get('description') or 'Sin descripción',
                'stars': repo['stargazers_count'],
                'forks': repo['forks_count'],
                'lenguaje': repo.get('language'),
                'url': repo['html_url'],
                'avatar': repo['owner']['avatar_url']
            }
            for repo in data.get('items', [])
        ]
        return jsonify(repos)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("🐙 GitHub Dashboard - http://127.0.0.1:5000")
    print("💡 Prueba con: torvalds, gaearon, sindresorhus")
    app.run(debug=True)
