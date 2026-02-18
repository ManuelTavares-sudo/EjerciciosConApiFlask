from flask import Flask, request, jsonify, render_template
import sqlite3
from datetime import datetime

app = Flask(__name__)
DATABASE = 'productos.db'

def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            descripcion TEXT,
            precio REAL NOT NULL,
            stock INTEGER DEFAULT 0,
            categoria TEXT,
            fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    cursor.execute('SELECT COUNT(*) FROM productos')
    if cursor.fetchone()[0] == 0:
        productos_ejemplo = [
            ('Laptop HP Pavilion', 'Laptop HP 15.6" Core i5 8GB RAM 512GB SSD', 15999.99, 10, 'Electrónica'),
            ('Mouse Logitech MX Master', 'Mouse inalámbrico ergonómico con scroll horizontal', 1299.99, 50, 'Accesorios'),
            ('Teclado Mecánico Keychron', 'Teclado mecánico RGB switches Cherry MX Red', 2499.99, 25, 'Accesorios'),
            ('Monitor Samsung 24"', 'Monitor 24" Full HD IPS 75Hz 5ms', 3499.99, 15, 'Electrónica'),
            ('Webcam Logitech C920', 'Webcam 1080p 30fps con micrófono estéreo', 899.99, 30, 'Accesorios'),
            ('SSD Samsung 1TB', 'SSD NVMe PCIe 4.0 7000MB/s lectura', 2899.99, 20, 'Almacenamiento'),
            ('Auriculares Sony WH-1000XM5', 'Auriculares inalámbricos cancelación de ruido', 5499.99, 8, 'Audio'),
            ('Hub USB-C 7 en 1', 'Hub USB-C con HDMI, USB 3.0, SD Card, Ethernet', 649.99, 40, 'Accesorios'),
        ]
        cursor.executemany('''
            INSERT INTO productos (nombre, descripcion, precio, stock, categoria)
            VALUES (?, ?, ?, ?, ?)
        ''', productos_ejemplo)
    conn.commit()
    conn.close()

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('productos.html')

# CREATE
@app.route('/api/productos', methods=['POST'])
def crear_producto():
    data = request.json
    if not data or not data.get('nombre') or not data.get('precio'):
        return jsonify({'error': 'Nombre y precio son requeridos'}), 400
    try:
        precio = float(data['precio'])
        if precio <= 0:
            return jsonify({'error': 'El precio debe ser mayor a 0'}), 400
    except (ValueError, TypeError):
        return jsonify({'error': 'El precio debe ser un número válido'}), 400

    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO productos (nombre, descripcion, precio, stock, categoria)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            data['nombre'].strip(),
            data.get('descripcion', '').strip(),
            precio,
            max(0, int(data.get('stock', 0))),
            data.get('categoria', 'General').strip()
        ))
        conn.commit()
        producto_id = cursor.lastrowid
        conn.close()
        return jsonify({'id': producto_id, 'mensaje': 'Producto creado exitosamente'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# READ ALL
@app.route('/api/productos', methods=['GET'])
def obtener_productos():
    categoria = request.args.get('categoria')
    buscar = request.args.get('buscar', '').strip()
    orden = request.args.get('orden', 'nombre')
    orden_dir = request.args.get('dir', 'ASC').upper()

    if orden not in ['nombre', 'precio', 'stock', 'fecha_creacion', 'categoria']:
        orden = 'nombre'
    if orden_dir not in ['ASC', 'DESC']:
        orden_dir = 'ASC'

    try:
        conn = get_db()
        cursor = conn.cursor()
        query = 'SELECT * FROM productos WHERE 1=1'
        params = []
        if categoria:
            query += ' AND categoria = ?'
            params.append(categoria)
        if buscar:
            query += ' AND (nombre LIKE ? OR descripcion LIKE ?)'
            params.extend([f'%{buscar}%', f'%{buscar}%'])
        query += f' ORDER BY {orden} {orden_dir}'
        cursor.execute(query, params)
        productos = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return jsonify(productos)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# READ ONE
@app.route('/api/productos/<int:id>', methods=['GET'])
def obtener_producto(id):
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM productos WHERE id = ?', (id,))
        producto = cursor.fetchone()
        conn.close()
        if producto is None:
            return jsonify({'error': 'Producto no encontrado'}), 404
        return jsonify(dict(producto))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# UPDATE
@app.route('/api/productos/<int:id>', methods=['PUT'])
def actualizar_producto(id):
    data = request.json
    if not data or not data.get('nombre') or data.get('precio') is None:
        return jsonify({'error': 'Nombre y precio son requeridos'}), 400
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT id FROM productos WHERE id = ?', (id,))
        if cursor.fetchone() is None:
            conn.close()
            return jsonify({'error': 'Producto no encontrado'}), 404
        cursor.execute('''
            UPDATE productos
            SET nombre = ?, descripcion = ?, precio = ?, stock = ?, categoria = ?,
                fecha_actualizacion = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (
            data['nombre'].strip(),
            data.get('descripcion', '').strip(),
            float(data['precio']),
            max(0, int(data.get('stock', 0))),
            data.get('categoria', 'General').strip(),
            id
        ))
        conn.commit()
        conn.close()
        return jsonify({'mensaje': 'Producto actualizado exitosamente'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# DELETE
@app.route('/api/productos/<int:id>', methods=['DELETE'])
def eliminar_producto(id):
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM productos WHERE id = ?', (id,))
        if cursor.rowcount == 0:
            conn.close()
            return jsonify({'error': 'Producto no encontrado'}), 404
        conn.commit()
        conn.close()
        return jsonify({'mensaje': 'Producto eliminado exitosamente'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# STATS
@app.route('/api/productos/stats', methods=['GET'])
def estadisticas():
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT
                COUNT(*) as total,
                ROUND(AVG(precio), 2) as precio_promedio,
                SUM(stock) as stock_total,
                ROUND(MIN(precio), 2) as precio_min,
                ROUND(MAX(precio), 2) as precio_max
            FROM productos
        ''')
        stats = dict(cursor.fetchone())
        cursor.execute('''
            SELECT categoria, COUNT(*) as cantidad,
                   ROUND(AVG(precio), 2) as precio_promedio,
                   SUM(stock) as stock_total
            FROM productos GROUP BY categoria ORDER BY cantidad DESC
        ''')
        stats_cat = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return jsonify({'generales': stats, 'por_categoria': stats_cat})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/categorias', methods=['GET'])
def obtener_categorias():
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT DISTINCT categoria FROM productos ORDER BY categoria')
        categorias = [row[0] for row in cursor.fetchall()]
        conn.close()
        return jsonify(categorias)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    init_db()
    print("✅ Base de datos inicializada con datos de ejemplo")
    print("📊 API REST disponible en http://127.0.0.1:5000")
    app.run(debug=True)
