from flask import Blueprint, request, jsonify
from functools import wraps
import jwt
import os
from models import User, VerificationCode, db
from werkzeug.security import generate_password_hash, check_password_hash
from services.email_service import generate_verification_code, send_verification_email
from datetime import datetime, timedelta

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

JWT_SECRET = os.getenv('JWT_SECRET_KEY', 'your-secret-key-change-in-production')

ADMIN_USERNAME = os.getenv('ADMIN_USERNAME', 'admin')

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        try:
            if token.startswith('Bearer '):
                token = token[7:]
            data = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
            current_user = User.query.get(data['user_id'])
            if not current_user:
                return jsonify({'error': 'User not found'}), 401
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 401
        return f(current_user, *args, **kwargs)
    return decorated

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        try:
            if token.startswith('Bearer '):
                token = token[7:]
            data = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
            current_user = User.query.get(data['user_id'])
            if not current_user:
                return jsonify({'error': 'User not found'}), 401
            if current_user.username != ADMIN_USERNAME:
                return jsonify({'error': 'Admin access required'}), 403
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 401
        return f(current_user, *args, **kwargs)
    return decorated

def doctor_or_parent_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        try:
            if token.startswith('Bearer '):
                token = token[7:]
            data = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
            current_user = User.query.get(data['user_id'])
            if not current_user:
                return jsonify({'error': 'User not found'}), 401
            if current_user.role not in ['parent', 'doctor']:
                return jsonify({'error': 'Parent or Doctor access required'}), 403
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 401
        return f(current_user, *args, **kwargs)
    return decorated

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    phone = data.get('phone')
    role = data.get('role', 'parent')
    verification_code = data.get('verification_code')

    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400

    if role == 'doctor':
        return jsonify({'error': 'Only admin can register doctor accounts'}), 403

    if not email:
        return jsonify({'error': 'Email is required'}), 400

    if not verification_code:
        return jsonify({'error': 'Verification code is required'}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'Username already exists'}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already exists'}), 400

    if phone and User.query.filter_by(phone=phone).first():
        return jsonify({'error': 'Phone already exists'}), 400

    verification_code_record = VerificationCode.query.filter_by(
        email=email,
        code=verification_code,
        used=False
    ).first()

    if not verification_code_record:
        return jsonify({'error': 'Invalid or expired verification code'}), 400

    if verification_code_record.expires_at < datetime.utcnow():
        return jsonify({'error': 'Verification code has expired'}), 400

    verification_code_record.used = True

    new_user = User(
        username=username,
        password_hash=generate_password_hash(password),
        email=email,
        phone=phone,
        role=role
    )
    db.session.add(new_user)
    db.session.commit()

    token = jwt.encode({'user_id': new_user.id}, JWT_SECRET, algorithm='HS256')

    return jsonify({
        'message': 'User registered successfully',
        'token': token,
        'user': new_user.to_dict()
    }), 201

@auth_bp.route('/register-doctor', methods=['POST'])
@admin_required
def register_doctor(current_user):
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    phone = data.get('phone')

    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400

    if not email and not phone:
        return jsonify({'error': 'Email or phone is required'}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'Username already exists'}), 400

    if email and User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already exists'}), 400

    if phone and User.query.filter_by(phone=phone).first():
        return jsonify({'error': 'Phone already exists'}), 400

    new_user = User(
        username=username,
        password_hash=generate_password_hash(password),
        email=email,
        phone=phone,
        role='doctor'
    )
    db.session.add(new_user)
    db.session.commit()

    token = jwt.encode({'user_id': new_user.id}, JWT_SECRET, algorithm='HS256')

    return jsonify({
        'message': 'Doctor registered successfully',
        'token': token,
        'user': new_user.to_dict()
    }), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    identifier = data.get('identifier')
    password = data.get('password')

    if not identifier or not password:
        return jsonify({'error': 'Identifier and password are required'}), 400

    user = None

    if '@' in identifier:
        user = User.query.filter_by(email=identifier).first()
    elif identifier.isdigit() and len(identifier) >= 11:
        user = User.query.filter_by(phone=identifier).first()
    else:
        user = User.query.filter_by(username=identifier).first()

    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({'error': 'Invalid credentials'}), 401

    token = jwt.encode({'user_id': user.id}, JWT_SECRET, algorithm='HS256')

    return jsonify({
        'message': 'Login successful',
        'token': token,
        'user': user.to_dict()
    })

@auth_bp.route('/me', methods=['GET'])
@token_required
def get_current_user(current_user):
    return jsonify({'user': current_user.to_dict()})

@auth_bp.route('/doctors', methods=['GET'])
@admin_required
def get_doctors(current_user):
    doctors = User.query.filter_by(role='doctor').all()
    return jsonify({
        'doctors': [doctor.to_dict() for doctor in doctors]
    })

@auth_bp.route('/doctors/<int:doctor_id>', methods=['DELETE'])
@admin_required
def delete_doctor(current_user, doctor_id):
    doctor = User.query.get(doctor_id)
    if not doctor:
        return jsonify({'error': 'Doctor not found'}), 404
    if doctor.role != 'doctor':
        return jsonify({'error': 'User is not a doctor'}), 400
    db.session.delete(doctor)
    db.session.commit()
    return jsonify({'message': 'Doctor deleted successfully'})

@auth_bp.route('/send-verification-code', methods=['POST'])
def send_verification_code():
    data = request.get_json()
    email = data.get('email')

    if not email:
        return jsonify({'error': 'Email is required'}), 400

    if '@' not in email:
        return jsonify({'error': 'Invalid email format'}), 400

    code = generate_verification_code()
    expires_at = datetime.utcnow() + timedelta(minutes=5)

    new_code = VerificationCode(
        email=email,
        code=code,
        expires_at=expires_at
    )

    try:
        db.session.add(new_code)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to save verification code'}), 500

    if send_verification_email(email, code):
        return jsonify({'message': 'Verification code sent successfully'}), 200
    else:
        return jsonify({'error': 'Failed to send verification email'}), 500

@auth_bp.route('/verify-code', methods=['POST'])
def verify_code():
    data = request.get_json()
    email = data.get('email')
    code = data.get('code')

    if not email or not code:
        return jsonify({'error': 'Email and code are required'}), 400

    verification_code = VerificationCode.query.filter_by(
        email=email,
        code=code,
        used=False
    ).first()

    if not verification_code:
        return jsonify({'error': 'Invalid or expired verification code'}), 400

    if verification_code.expires_at < datetime.utcnow():
        return jsonify({'error': 'Verification code has expired'}), 400

    verification_code.used = True
    db.session.commit()

    return jsonify({'message': 'Verification successful'}), 200
