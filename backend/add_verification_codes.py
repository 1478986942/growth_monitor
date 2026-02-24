from app import app
from models import db, VerificationCode
from datetime import datetime

def add_verification_codes_table():
    with app.app_context():
        try:
            db.create_all()
            print("✓ verification_codes 表创建成功")
        except Exception as e:
            print(f"✗ 创建表失败: {e}")

if __name__ == '__main__':
    add_verification_codes_table()
