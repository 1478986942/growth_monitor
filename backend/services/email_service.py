from flask_mail import Mail, Message
from flask import current_app
import random
from datetime import datetime, timedelta
import traceback

mail = Mail()

def generate_verification_code():
    return ''.join([str(random.randint(0, 9)) for _ in range(6)])

def send_verification_email(email, code):
    try:
        msg = Message(
            subject='【儿童生长发育监测平台】邮箱验证码',
            recipients=[email]
        )
        
        html_content = f'''
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                body {{
                    font-family: 'Microsoft YaHei', 'PingFang SC', 'Helvetica Neue', Arial, sans-serif;
                    background-color: #f5f7fa;
                    margin: 0;
                    padding: 20px;
                    line-height: 1.6;
                }}
                .container {{
                    max-width: 600px;
                    margin: 0 auto;
                    background-color: #ffffff;
                    border-radius: 12px;
                    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
                    overflow: hidden;
                }}
                .header {{
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    padding: 40px 30px;
                    text-align: center;
                }}
                .header h1 {{
                    color: #ffffff;
                    margin: 0;
                    font-size: 28px;
                    font-weight: 600;
                }}
                .header p {{
                    color: #ffffff;
                    margin: 10px 0 0 0;
                    font-size: 14px;
                    opacity: 0.9;
                }}
                .content {{
                    padding: 40px 30px;
                }}
                .greeting {{
                    font-size: 18px;
                    color: #333333;
                    margin-bottom: 20px;
                }}
                .code-box {{
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    padding: 25px;
                    border-radius: 8px;
                    text-align: center;
                    margin: 30px 0;
                }}
                .code {{
                    font-size: 36px;
                    font-weight: bold;
                    color: #ffffff;
                    letter-spacing: 8px;
                    font-family: 'Courier New', monospace;
                }}
                .info {{
                    color: #666666;
                    font-size: 14px;
                    line-height: 1.8;
                }}
                .warning {{
                    background-color: #fff3cd;
                    border-left: 4px solid #ffc107;
                    padding: 15px;
                    margin: 20px 0;
                    border-radius: 4px;
                }}
                .warning-text {{
                    color: #856404;
                    font-size: 14px;
                    margin: 0;
                }}
                .footer {{
                    background-color: #f8f9fa;
                    padding: 25px 30px;
                    text-align: center;
                    border-top: 1px solid #e9ecef;
                }}
                .footer p {{
                    color: #6c757d;
                    font-size: 12px;
                    margin: 5px 0;
                }}
                .footer a {{
                    color: #667eea;
                    text-decoration: none;
                }}
                .icon {{
                    font-size: 48px;
                    margin-bottom: 10px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <div class="icon">👶</div>
                    <h1>儿童生长发育监测平台</h1>
                    <p>智能监测 · 科学评估 · 专业干预</p>
                </div>
                
                <div class="content">
                    <p class="greeting">您好！</p>
                    
                    <p class="info">您正在进行邮箱验证操作，您的验证码是：</p>
                    
                    <div class="code-box">
                        <div class="code">{code}</div>
                    </div>
                    
                    <p class="info">验证码有效期为 <strong>5分钟</strong>，请尽快使用。</p>
                    
                    <div class="warning">
                        <p class="warning-text">⚠️ 如果这不是您本人的操作，请忽略此邮件，您的账号安全不会受到影响。</p>
                    </div>
                </div>
                
                <div class="footer">
                    <p>此致</p>
                    <p><strong>儿童生长发育智能监测与干预平台</strong></p>
                    <p>如有疑问，请联系客服 | <a href="#">访问官网</a></p>
                    <p style="margin-top: 15px; color: #999;">© 2026 Lighthouse of Growth. All rights reserved.</p>
                </div>
            </div>
        </body>
        </html>
        '''
        
        msg.html = html_content
        mail.send(msg)
        return True
    except Exception as e:
        print(f"发送邮件失败: {e}")
        print(f"详细错误: {traceback.format_exc()}")
        return False
