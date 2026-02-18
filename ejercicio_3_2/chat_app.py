from flask import Flask, render_template, request, jsonify
import firebase_admin
from firebase_admin import credentials, db
from datetime import datetime
import os

app = Flask(__name__)

# === CONFIGURAR FIREBASE ===
# 1. Ve a https://console.firebase.google.com
# 2. Crea un proyecto > Realtime Database > Crear base de datos (modo Test)
# 3. Ve a Configuración > Cuentas de servicio > Generar nueva clave privada
# 4. Guarda el JSON como 'firebase-credentials.json' en esta carpeta
# 5. Reemplaza TU-PROYECTO con el ID de tu proyecto

FIREBASE_DB_URL = 'https://chat-con-api-default-rtdb.firebaseio.com/'  # Cambiar aquí

firebase_ok = False
if not firebase_admin._apps:
    if os.path.exists('firebase-credentials.json'):
        try:
            cred = credentials.Certificate('firebase-credentials.json')
            firebase_admin.initialize_app(cred, {'databaseURL': FIREBASE_DB_URL})
            firebase_ok = True
            print("✅ Firebase conectado correctamente")
        except Exception as e:
            print(f"❌ Error al inicializar Firebase: {e}")
    else:
        print("⚠️  No se encontró 'firebase-credentials.json'")
        print("   Descárgalo desde Firebase Console > Configuración > Cuentas de servicio")

@app.route('/')
def index():
    return render_template('chat.html')

@app.route('/api/status')
def status():
    return jsonify({'firebase_ok': firebase_ok})

@app.route('/api/mensajes', methods=['GET'])
def obtener_mensajes():
    if not firebase_ok:
        return jsonify({'error': 'Firebase no configurado. Revisa firebase-credentials.json'}), 503
    try:
        ref = db.reference('mensajes')
        mensajes = ref.order_by_child('timestamp').limit_to_last(50).get()
        if mensajes:
            lista = []
            for key, value in mensajes.items():
                value['id'] = key
                lista.append(value)
            lista.sort(key=lambda x: x.get('timestamp', ''))
            return jsonify(lista)
        return jsonify([])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/mensajes', methods=['POST'])
def enviar_mensaje():
    if not firebase_ok:
        return jsonify({'error': 'Firebase no configurado'}), 503
    data = request.json
    if not data or not data.get('usuario') or not data.get('texto'):
        return jsonify({'error': 'Usuario y texto son requeridos'}), 400
    if len(data['texto']) > 500:
        return jsonify({'error': 'Mensaje demasiado largo (máx. 500 caracteres)'}), 400
    try:
        ref = db.reference('mensajes')
        nuevo = {
            'usuario': data['usuario'][:30],
            'texto': data['texto'].strip(),
            'timestamp': datetime.now().isoformat(),
            'avatar': data.get('avatar', '👤'),
            'color': data.get('color', '#6366f1')
        }
        nueva_ref = ref.push(nuevo)
        nuevo['id'] = nueva_ref.key
        return jsonify(nuevo), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/mensajes/<mensaje_id>', methods=['DELETE'])
def eliminar_mensaje(mensaje_id):
    if not firebase_ok:
        return jsonify({'error': 'Firebase no configurado'}), 503
    try:
        ref = db.reference(f'mensajes/{mensaje_id}')
        ref.delete()
        return jsonify({'mensaje': 'Eliminado'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/usuarios/ping', methods=['POST'])
def ping_usuario():
    if not firebase_ok:
        return jsonify({'ok': False}), 503
    data = request.json
    usuario = data.get('usuario', '').strip()
    if not usuario:
        return jsonify({'error': 'Usuario requerido'}), 400
    try:
        ref = db.reference(f'presencia/{usuario}')
        ref.set({
            'ultima_actividad': datetime.now().isoformat(),
            'online': True
        })
        return jsonify({'ok': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/usuarios/online', methods=['GET'])
def usuarios_online():
    if not firebase_ok:
        return jsonify([])
    try:
        ref = db.reference('presencia')
        data = ref.get()
        if not data:
            return jsonify([])
        # Solo usuarios activos en últimos 30 segundos
        from datetime import timedelta
        threshold = datetime.now() - timedelta(seconds=30)
        online = []
        for usuario, info in data.items():
            try:
                ultima = datetime.fromisoformat(info.get('ultima_actividad', ''))
                if ultima > threshold:
                    online.append(usuario)
            except:
                pass
        return jsonify(online)
    except Exception as e:
        return jsonify([])

if __name__ == '__main__':
    print("🔥 Chat en Tiempo Real con Firebase")
    print("📝 URL Firebase:", FIREBASE_DB_URL)
    print("🌐 App en: http://127.0.0.1:5000")
    app.run(debug=True)
