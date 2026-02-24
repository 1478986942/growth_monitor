import psycopg2
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

DATABASE_URI = os.getenv('DATABASE_URI')

def init_database():
    try:
        # 从DATABASE_URI中提取连接信息
        import re
        match = re.search(r'postgresql://(.*?):(.*?)@(.*?):(.*?)/(.*?)', DATABASE_URI)
        if not match:
            print("Invalid DATABASE_URI format")
            return
        
        user, password, host, port, dbname = match.groups()
        
        # 连接到PostgreSQL服务器
        conn = psycopg2.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            dbname='postgres'  # 连接到默认数据库
        )
        conn.set_isolation_level(0)  # 设置为自动提交
        cursor = conn.cursor()
        
        print("开始初始化数据库...")
        
        # 检查数据库是否存在
        cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = '{dbname}'")
        if not cursor.fetchone():
            print(f"创建数据库: {dbname}")
            cursor.execute(f"CREATE DATABASE {dbname} ENCODING 'UTF8' LC_COLLATE 'en_US.utf8' LC_CTYPE 'en_US.utf8'")
        else:
            print(f"数据库 {dbname} 已存在")
        
        # 关闭连接
        cursor.close()
        conn.close()
        
        # 连接到目标数据库
        conn = psycopg2.connect(DATABASE_URI)
        conn.set_isolation_level(0)
        cursor = conn.cursor()
        
        # 读取并执行database.sql文件
        print("执行database.sql文件...")
        with open('../database.sql', 'r', encoding='utf-8') as f:
            sql_commands = f.read()
        
        # 执行SQL命令
        for command in sql_commands.split(';'):
            if command.strip():
                try:
                    cursor.execute(command)
                except Exception as e:
                    print(f"执行命令失败: {command[:100]}...")
                    print(f"错误: {e}")
        
        print("数据库初始化完成！")
        
    except Exception as e:
        print(f"初始化数据库失败: {e}")
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

if __name__ == '__main__':
    init_database()
