from flask import Flask, render_template, request, jsonify
import requests
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('reddit.html')

@app.route('/api/reddit/posts')
def obtener_posts_reddit():
    subreddit = request.args.get('subreddit', 'python')
    filtro = request.args.get('filtro', 'hot')  # hot, new, top
    limit = request.args.get('limit', 10, type=int)

    url = f'https://www.reddit.com/r/{subreddit}/{filtro}.json'
    headers = {'User-Agent': 'Mozilla/5.0 (compatible; FlaskApp/1.0)'}

    try:
        response = requests.get(url, headers=headers, params={'limit': limit}, timeout=15)

        if response.status_code == 403:
            return jsonify({'error': 'Acceso bloqueado por Reddit. Intenta de nuevo.'}), 403
        if response.status_code == 404:
            return jsonify({'error': f'El subreddit r/{subreddit} no existe.'}), 404

        data = response.json()
        posts = []
        for post in data['data']['children']:
            post_data = post['data']
            fecha = datetime.fromtimestamp(post_data['created_utc'])

            thumbnail = post_data.get('thumbnail')
            if thumbnail in ['self', 'default', '', 'nsfw', 'spoiler']:
                thumbnail = None

            posts.append({
                'titulo': post_data['title'],
                'autor': post_data['author'],
                'puntos': post_data['score'],
                'comentarios': post_data['num_comments'],
                'url': f"https://reddit.com{post_data['permalink']}",
                'url_completa': post_data.get('url', ''),
                'fecha': fecha.strftime('%d/%m/%Y %H:%M'),
                'thumbnail': thumbnail,
                'selftext': (post_data.get('selftext', '')[:200] + '...') if post_data.get('selftext') else '',
                'upvote_ratio': round(post_data.get('upvote_ratio', 0) * 100),
                'is_video': post_data.get('is_video', False)
            })

        return jsonify({'subreddit': subreddit, 'posts': posts})
    except requests.exceptions.Timeout:
        return jsonify({'error': 'Reddit tardó demasiado en responder.'}), 504
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/reddit/buscar')
def buscar_reddit():
    query = request.args.get('q', '')
    limit = request.args.get('limit', 10, type=int)

    if not query:
        return jsonify({'error': 'Consulta requerida'}), 400

    url = 'https://www.reddit.com/search.json'
    headers = {'User-Agent': 'Mozilla/5.0 (compatible; FlaskApp/1.0)'}
    params = {'q': query, 'limit': limit}

    try:
        response = requests.get(url, headers=headers, params=params, timeout=15)
        data = response.json()

        resultados = []
        for post in data['data']['children']:
            post_data = post['data']
            fecha = datetime.fromtimestamp(post_data['created_utc'])
            resultados.append({
                'titulo': post_data['title'],
                'subreddit': post_data['subreddit'],
                'autor': post_data['author'],
                'puntos': post_data['score'],
                'comentarios': post_data['num_comments'],
                'url': f"https://reddit.com{post_data['permalink']}",
                'fecha': fecha.strftime('%d/%m/%Y %H:%M')
            })

        return jsonify(resultados)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/reddit/subreddits/populares')
def subreddits_populares():
    subreddits = [
        {'nombre': 'python', 'descripcion': 'Python programming', 'emoji': '🐍'},
        {'nombre': 'learnprogramming', 'descripcion': 'Aprender programación', 'emoji': '📚'},
        {'nombre': 'webdev', 'descripcion': 'Desarrollo web', 'emoji': '🌐'},
        {'nombre': 'javascript', 'descripcion': 'JavaScript', 'emoji': '⚡'},
        {'nombre': 'flask', 'descripcion': 'Flask framework', 'emoji': '🔥'},
        {'nombre': 'technology', 'descripcion': 'Tecnología', 'emoji': '💻'},
        {'nombre': 'programming', 'descripcion': 'Programación', 'emoji': '👨‍💻'},
        {'nombre': 'worldnews', 'descripcion': 'Noticias mundiales', 'emoji': '🌍'},
        {'nombre': 'science', 'descripcion': 'Ciencia', 'emoji': '🔬'},
        {'nombre': 'askreddit', 'descripcion': 'Preguntas', 'emoji': '❓'}
    ]
    return jsonify(subreddits)

if __name__ == '__main__':
    print("🤖 Reddit Analyzer - http://127.0.0.1:5000")
    app.run(debug=True)
