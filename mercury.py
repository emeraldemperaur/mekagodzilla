# Flask API Server
from artificer import ASCI_RESET, ASCI_POWER, ASCI_GREEN, ASCI_MERCURY, ASCI_TEAL
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, \
    create_refresh_token, get_jwt
from werkzeug.security import generate_password_hash, check_password_hash
import sys
import warnings

from artisan import Artisan

app_server = Flask("Mercury")
app_server.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///iliad.db'  # SQLite database file
app_server.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app_server.config['JWT_SECRET_KEY'] = 'la-li-lu-le-lo'  # Change this in production
app_server.config['JWT_BLACKLIST_ENABLED'] = True
app_server.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
server_db = SQLAlchemy(app_server)
migrate = Migrate(app_server, server_db)
jwt = JWTManager(app_server)
cli = sys.modules['flask.cli']
cli.show_server_banner = lambda *x: None
warnings.filterwarnings('ignore', category=UserWarning, module='flask')

# In-memory set for blacklisted tokens
blocklisted_tokens = set()


@jwt.token_in_blocklist_loader
def check_if_token_in_blocklist(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    algorithm = jwt_header["alg"]
    token_type = jwt_header["typ"]
    print(F"Executed JWT token blocklist check: {algorithm}, {token_type}, {jti}")
    return jti in blocklisted_tokens


class Mercury:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            # If no instance exists, create a new one using the parent's __new__
            cls._instance = super(Mercury, cls).__new__(cls)
        return cls._instance  # Always return the existing instance

    def __init__(self):
        if not hasattr(self, '_initialized'):
            # Prevent re-initialization
            self.artisan = Artisan()
            self.app_server = app_server
            self.server_db = server_db
            self.jwt = jwt
            self._initialized = True

    def get_alchemy_db(self):
        return self.server_db

    def start_server(self):
        Mercury.init_log(ASCI_GREEN, ASCI_MERCURY, " Activated")
        print(F"\t{ASCI_TEAL}{ASCI_POWER} API Server Online {ASCI_RESET}")
        with self.app_server.app_context():
            self.server_db.create_all()
        self.app_server.run(host='127.0.0.1', port=4134)

    @staticmethod
    def init_log(asci_hex, asci_art, verb):
        print(F"{asci_hex}{asci_art} Mercury{verb}{ASCI_RESET}")


mercury = Mercury()


class User(mercury.server_db.Model):
    id = mercury.server_db.Column(server_db.Integer, primary_key=True)
    username = mercury.server_db.Column(server_db.String(80), unique=True, nullable=False)
    password_hash = mercury.server_db.Column(server_db.String(120), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@mercury.app_server.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    codex = data.get('codex')

    if not username or not password or not codex:
        return jsonify({"mercury": "Missing username, password or codex"}), 400

    if codex != "sahelanthropus":
        return jsonify({"mercury": F"Invalid codex: {codex} provided"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"mercury": "User already exists"}), 409

    new_user = User(username=username)
    new_user.set_password(password)
    server_db.session.add(new_user)
    server_db.session.commit()
    return jsonify({"mercury": "User registered successfully"}), 201


@mercury.app_server.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()

    if user and user.check_password(password):
        access_token = create_access_token(identity=user.username)
        refresh_token = create_refresh_token(identity=user.username)
        return jsonify(access_token=access_token, refresh_token=refresh_token), 200
    return jsonify({"mercury": "Invalid username or password"}), 401

@mercury.app_server.route('/protected', methods=['GET'])
@jwt_required()
def this_user():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

@mercury.app_server.route('/refresh', methods=['POST'])
@jwt.needs_fresh_token_loader
def refresh():
    current_user = get_jwt_identity()
    new_access_token = create_access_token(identity=current_user)
    return jsonify(access_token=new_access_token), 200

@mercury.app_server.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]  # Get the unique identifier (jti) of the current JWT
    blocklisted_tokens.add(jti)  # Add the jti to the blocklist
    return jsonify(mercury="Access token revoked"), 200

@mercury.app_server.route("/health", methods=["GET"])
@jwt_required()
def health():
    return jsonify(mercury="Hello from protected")