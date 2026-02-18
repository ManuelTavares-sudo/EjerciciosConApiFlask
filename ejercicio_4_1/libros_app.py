from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

GOOGLE_BOOKS_API = 'https://www.googleapis.com/books/v1/volumes'

@app.route('/')
def index():
    return render_template('libros.html')

@app.route('/api/libros/buscar')
def buscar_libros():
    query = request.args.get('q', '').strip()
    categoria = request.args.get('categoria', '').strip()
    idioma = request.args.get('idioma', 'es')
    max_results = request.args.get('max', 20, type=int)

    if not query:
        return jsonify({'error': 'Consulta requerida'}), 400

    search_query = query
    if categoria:
        search_query += f'+subject:{categoria}'

    params = {
        'q': search_query,
        'maxResults': min(max_results, 40),
        'printType': 'books',
    }
    if idioma != 'todos':
        params['langRestrict'] = idioma

    try:
        response = requests.get(GOOGLE_BOOKS_API, params=params, timeout=10)
        data = response.json()

        if 'items' not in data:
            return jsonify([])

        libros = []
        for item in data['items']:
            info = item.get('volumeInfo', {})
            venta = item.get('saleInfo', {})

            imagen = (
                info.get('imageLinks', {}).get('thumbnail') or
                info.get('imageLinks', {}).get('smallThumbnail')
            )
            if imagen:
                imagen = imagen.replace('http://', 'https://')

            desc = info.get('description', '')
            if desc and len(desc) > 250:
                desc = desc[:250] + '...'

            libros.append({
                'id': item['id'],
                'titulo': info.get('title', 'Sin título'),
                'subtitulo': info.get('subtitle', ''),
                'autores': info.get('authors', ['Autor desconocido']),
                'descripcion': desc,
                'editorial': info.get('publisher', ''),
                'fecha_publicacion': info.get('publishedDate', ''),
                'paginas': info.get('pageCount', 0),
                'categorias': info.get('categories', []),
                'imagen': imagen,
                'preview_link': info.get('previewLink', ''),
                'info_link': info.get('infoLink', ''),
                'rating': info.get('averageRating', 0),
                'ratings_count': info.get('ratingsCount', 0),
                'idioma': info.get('language', ''),
                'precio': venta.get('listPrice', {}).get('amount', 0),
                'moneda': venta.get('listPrice', {}).get('currencyCode', ''),
                'disponible': venta.get('saleability') == 'FOR_SALE',
                'compra_link': venta.get('buyLink', '')
            })

        return jsonify(libros)
    except requests.exceptions.Timeout:
        return jsonify({'error': 'Google Books tardó demasiado en responder.'}), 504
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/libros/<book_id>')
def detalle_libro(book_id):
    try:
        response = requests.get(f'{GOOGLE_BOOKS_API}/{book_id}', timeout=10)
        data = response.json()
        info = data.get('volumeInfo', {})
        venta = data.get('saleInfo', {})

        imagen = (
            info.get('imageLinks', {}).get('large') or
            info.get('imageLinks', {}).get('medium') or
            info.get('imageLinks', {}).get('thumbnail')
        )
        if imagen:
            imagen = imagen.replace('http://', 'https://')

        return jsonify({
            'id': data['id'],
            'titulo': info.get('title'),
            'subtitulo': info.get('subtitle'),
            'autores': info.get('authors', []),
            'descripcion': info.get('description', ''),
            'editorial': info.get('publisher'),
            'fecha_publicacion': info.get('publishedDate'),
            'paginas': info.get('pageCount'),
            'categorias': info.get('categories', []),
            'imagen': imagen,
            'idioma': info.get('language'),
            'preview_link': info.get('previewLink'),
            'info_link': info.get('infoLink'),
            'rating': info.get('averageRating'),
            'ratings_count': info.get('ratingsCount'),
            'precio': venta.get('listPrice', {}).get('amount'),
            'moneda': venta.get('listPrice', {}).get('currencyCode'),
            'comprable': venta.get('saleability') == 'FOR_SALE',
            'compra_link': venta.get('buyLink')
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/libros/categorias')
def categorias():
    cats = [
        'Fiction', 'Science', 'History', 'Biography', 'Technology',
        'Business', 'Self-Help', 'Poetry', 'Mystery', 'Romance',
        'Fantasy', 'Science Fiction', 'Programming', 'Education',
        'Health', 'Art', 'Cooking', 'Travel', 'Philosophy'
    ]
    return jsonify(cats)

@app.route('/api/libros/populares')
def libros_populares():
    """Búsquedas populares predefinidas"""
    populares = [
        {'query': 'inteligencia artificial', 'label': '🤖 Inteligencia Artificial'},
        {'query': 'programacion python', 'label': '🐍 Python'},
        {'query': 'historia mexico', 'label': '🇲🇽 Historia de México'},
        {'query': 'desarrollo personal', 'label': '💡 Desarrollo Personal'},
        {'query': 'ciencia ficcion', 'label': '🚀 Ciencia Ficción'},
        {'query': 'cocina recetas', 'label': '🍳 Cocina'},
    ]
    return jsonify(populares)

if __name__ == '__main__':
    print("📚 Buscador de Libros - Google Books API")
    print("🌐 App en: http://127.0.0.1:5000")
    app.run(debug=True)
