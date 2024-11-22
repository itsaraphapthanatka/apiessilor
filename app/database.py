from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sshtunnel import SSHTunnelForwarder
import os
from dotenv import load_dotenv

# โหลด environment variables
load_dotenv()
print(os.getenv('ENV_SSH'))
print(os.getenv('ENV'))
if os.getenv('ENV_SSH') == 'SSH':
    # ข้อมูล SSH
    SSH_HOST = os.getenv('SSH_HOST')
    SSH_PORT = int(os.getenv('SSH_PORT', 22))
    SSH_USER = os.getenv('SSH_USER')
    SSH_PASSWORD = os.getenv('SSH_PASSWORD')

# ข้อมูลฐานข้อมูล
DB_HOST = os.getenv('LOCAL_HOST', 'localhost')
DB_PORT = int(os.getenv('LOCAL_PORT', 3306))
DB_USER = os.getenv('LOCAL_USER')
DB_PASSWORD = os.getenv('LOCAL_PASSWORD')
DB_NAME = os.getenv('LOCAL_NAME')
print(DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME)

# สร้าง SSH tunnel
if os.getenv('ENV_SSH') == 'SSH':
    try:
        tunnel = SSHTunnelForwarder(
        (SSH_HOST, SSH_PORT),
        ssh_username=SSH_USER,
        ssh_password=SSH_PASSWORD,
        remote_bind_address=(DB_HOST, DB_PORT),
        local_bind_address=('127.0.0.1', 3306)  # พอร์ตท้องถิ่นสำหรับ tunnel
    )
    # เริ่มต้น tunnel
        tunnel.start()
    except Exception as e:
        print(f"เกิดข้อผิดพลาดในการเปิด SSH tunnel: {e}")
        raise  # ยกข้อผิดพลาดขึ้นเพื่อหยุดการทำงาน

# เริ่มต้น tunnel
if os.getenv('ENV_SSH') == 'SSH':
    tunnel.start()

# สร้าง URL สำหรับการเชื่อมต่อฐานข้อมูล
if os.getenv('ENV_SSH') == 'SSH':
    SQLALCHEMY_DATABASE_URL = f"mysql+mysqlconnector://{os.getenv('MYSQL_USER')}:{os.getenv('MYSQL_PASSWORD')}@127.0.0.1:{tunnel.local_bind_port}/{os.getenv('MYSQL_DATABASE')}"
    print(f"SQLALCHEMY_DATABASE_URL: {SQLALCHEMY_DATABASE_URL}")
elif os.getenv('ENV') == 'local':
    SQLALCHEMY_DATABASE_URL = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    print(f"SQLALCHEMY_DATABASE_URL: {SQLALCHEMY_DATABASE_URL}")



# สร้าง engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# สร้าง SessionLocal
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# สร้าง Base class
Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
