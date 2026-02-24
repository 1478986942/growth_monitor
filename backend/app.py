from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 创建Flask应用
app = Flask(__name__)

# 配置
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI', 'mysql+pymysql://root:root@localhost:3306/growth_monitor1')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'your-secret-key')

# 初始化数据库
from models import db
from models.user import User
from models.child import Child
from models.growth import GrowthRecord
from models.risk import RiskAssessment
from models.intervention import Intervention
from models.hospital import Hospital
from models.resource import Resource
from models.verification_code import VerificationCode

# 初始化路由
from routes import auth_bp, children_bp, growth_bp, risk_bp, intervention_bp, hospital_bp, resource_bp

# 配置CORS
CORS(app, resources={r"/api/*": {"origins": ["*"], "methods": ["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"]}})

# 注册路由
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(children_bp, url_prefix='/api/children')
app.register_blueprint(growth_bp, url_prefix='/api/growth')
app.register_blueprint(risk_bp, url_prefix='/api/risk')
app.register_blueprint(intervention_bp, url_prefix='/api/intervention')
app.register_blueprint(hospital_bp, url_prefix='/api/hospital')
app.register_blueprint(resource_bp, url_prefix='/api/resource')

# 健康检查
@app.route('/health')
def health_check():
    return {'status': 'ok'}

if __name__ == '__main__':
    # 创建数据库表
    with app.app_context():
        db.create_all()
    
    # 启动应用
    port = int(os.getenv('PORT', 5555))
    app.run(host='0.0.0.0', port=port, debug=False)