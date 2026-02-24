from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from datetime import timedelta
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 初始化应用
app = Flask(__name__)

# 配置
app.config['SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'default-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_POOL_RECYCLE'] = 280

# 邮件配置
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 465))
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'False').lower() == 'true'
app.config['MAIL_USE_SSL'] = os.getenv('MAIL_USE_SSL', 'True').lower() == 'true'
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')

# 初始化扩展
db = SQLAlchemy(app)
mail = Mail(app)

# 配置CORS
CORS(app, origins=['http://localhost:3000', 'http://127.0.0.1:3000'], supports_credentials=True)

# 导入并注册蓝图
from routes import auth_bp, children_bp, growth_bp, risk_bp, intervention_bp, hospital_bp, resource_bp

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
    return {'status': 'healthy'}

# 启动应用
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5555, debug=True)