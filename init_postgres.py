import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

DATABASE_URI = "postgresql://growth_monitor_user:HrrnZVmtFXmUSRHqErioCQr3ZEJzfSX9@dpg-d6eptjc1hm7c73fbapog-a.oregon-postgres.render.com/growth_monitor"

def init_database():
    try:
        conn = psycopg2.connect(DATABASE_URI)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()

        print("开始初始化数据库...")

        # 创建用户表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                email VARCHAR(100) UNIQUE,
                phone VARCHAR(20) UNIQUE,
                role VARCHAR(20) DEFAULT 'parent',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        print("✓ users表创建成功")

        # 创建儿童表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS children (
                id SERIAL PRIMARY KEY,
                user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                name VARCHAR(50) NOT NULL,
                gender VARCHAR(10) NOT NULL CHECK (gender IN ('male', 'female')),
                birth_date DATE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        print("✓ children表创建成功")

        # 创建生长记录表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS growth_records (
                id SERIAL PRIMARY KEY,
                child_id INTEGER NOT NULL REFERENCES children(id) ON DELETE CASCADE,
                record_date DATE NOT NULL,
                height DECIMAL(5, 2),
                weight DECIMAL(5, 2),
                bmi DECIMAL(4, 2),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        print("✓ growth_records表创建成功")

        # 创建风险评估表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS risk_assessments (
                id SERIAL PRIMARY KEY,
                child_id INTEGER NOT NULL REFERENCES children(id) ON DELETE CASCADE,
                assessment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                stunting_risk DECIMAL(5, 2),
                obesity_risk DECIMAL(5, 2),
                details JSONB
            );
        """)
        print("✓ risk_assessments表创建成功")

        # 创建干预方案表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS interventions (
                id SERIAL PRIMARY KEY,
                child_id INTEGER NOT NULL REFERENCES children(id) ON DELETE CASCADE,
                assessment_id INTEGER REFERENCES risk_assessments(id) ON DELETE SET NULL,
                plan_title VARCHAR(200),
                plan_content TEXT,
                start_date DATE,
                end_date DATE,
                status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'ongoing', 'completed')),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        print("✓ interventions表创建成功")

        # 创建医院表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS hospitals (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                address TEXT,
                phone VARCHAR(20),
                specialty VARCHAR(100),
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        print("✓ hospitals表创建成功")

        # 创建资源表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS resources (
                id SERIAL PRIMARY KEY,
                title VARCHAR(200) NOT NULL,
                category VARCHAR(50) NOT NULL,
                content TEXT,
                url VARCHAR(500),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        print("✓ resources表创建成功")

        # 创建验证码表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS verification_codes (
                id SERIAL PRIMARY KEY,
                email VARCHAR(100) NOT NULL,
                code VARCHAR(6) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                expires_at TIMESTAMP NOT NULL,
                used BOOLEAN DEFAULT FALSE
            );
        """)
        print("✓ verification_codes表创建成功")

        # 创建索引
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_children_user_id ON children(user_id);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_growth_records_child_id ON growth_records(child_id);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_risk_assessments_child_id ON risk_assessments(child_id);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_interventions_child_id ON interventions(child_id);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_verification_codes_email ON verification_codes(email);")
        print("✓ 索引创建成功")

        print("\n数据库初始化完成！")

        cursor.close()
        conn.close()
        return True

    except Exception as e:
        print(f"❌ 数据库初始化失败: {e}")
        return False

if __name__ == '__main__':
    init_database()