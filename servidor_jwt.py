from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///usuarios.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'clave-secreta-segura'  

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# Modelo
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(80), unique=True, nullable=False)
    contraseña = db.Column(db.String(128), nullable=False)

# Crear base de datos
with app.app_context():
    db.create_all()

# Registro
@app.route('/registro', methods=['POST'])
def registro():
    datos = request.get_json()
    usuario = datos['usuario']
    contraseña = bcrypt.generate_password_hash(datos['contraseña']).decode('utf-8')

    if Usuario.query.filter_by(usuario=usuario).first():
        return jsonify({"mensaje": "Usuario ya existe"}), 409

    nuevo_usuario = Usuario(usuario=usuario, contraseña=contraseña)
    db.session.add(nuevo_usuario)
    db.session.commit()
    return jsonify({"mensaje": "Usuario registrado exitosamente"}), 201

# Login con generación de token
@app.route('/login', methods=['POST'])
def login():
    datos = request.get_json()
    usuario = Usuario.query.filter_by(usuario=datos['usuario']).first()

    if usuario and bcrypt.check_password_hash(usuario.contraseña, datos['contraseña']):
        token = create_access_token(identity=usuario.usuario)
        return jsonify({"mensaje": f"Bienvenido {usuario.usuario}", "token": token}), 200
    return jsonify({"mensaje": "Credenciales incorrectas"}), 401

# Ruta protegida con JWT
@app.route('/tareas', methods=['GET'])
@jwt_required()
def tareas():
    usuario = get_jwt_identity()
    return f"""
    <html>
        <body>
            <h1>Bienvenido {usuario}</h1>
            <p>Esta es la vista protegida de tareas.</p>
        </body>
    </html>
    """

# Inicio
if __name__ == '__main__':
    app.run(debug=True)
