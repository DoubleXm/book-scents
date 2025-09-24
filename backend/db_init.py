import mysql.connector
import os
from datetime import datetime
from dotenv import load_dotenv
import mysql.connector

# 加载环境变量
load_dotenv()

def create_connection():
    """创建数据库连接"""
    try:
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME')
        )
        print("数据库连接成功")
        return connection
    except mysql.connector.Error as error:
        print(f"数据库连接失败: {error}")
        # 如果数据库不存在，尝试创建
        if 'Unknown database' in str(error):
            try:
                connection = mysql.connector.connect(
                    host=os.getenv('DB_HOST'),
                    port=os.getenv('DB_PORT'),
                    user=os.getenv('DB_USER'),
                    password=os.getenv('DB_PASSWORD')
                )
                cursor = connection.cursor()
                cursor.execute(f"CREATE DATABASE {os.getenv('DB_NAME')}")
                print(f"数据库 {os.getenv('DB_NAME')} 创建成功")
                connection.close()
                # 重新连接到新创建的数据库
                return create_connection()
            except mysql.connector.Error as create_error:
                print(f"创建数据库失败: {create_error}")
        return None

def create_tables(connection):
    """创建数据库表"""
    cursor = connection.cursor()
    
    # 创建用户表
    create_users_table = """
    CREATE TABLE IF NOT EXISTS users (
        id VARCHAR(36) PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        password VARCHAR(255) NOT NULL,
        mobile VARCHAR(20) NOT NULL,
        cover VARCHAR(255) DEFAULT 'default_avatar.png',
        created_time DATETIME NOT NULL,
        updated_time DATETIME NOT NULL,
        UNIQUE KEY unique_mobile (mobile)
    )
    """
    
    # 创建书籍表
    create_books_table = """
    CREATE TABLE IF NOT EXISTS books (
        id VARCHAR(36) PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        author VARCHAR(100) NOT NULL,
        publisher VARCHAR(100) DEFAULT '',
        publisher_date VARCHAR(20) DEFAULT '',
        description TEXT,
        cover VARCHAR(255) NOT NULL,
        url VARCHAR(255) NOT NULL,
        hot INT DEFAULT 0,
        recommend INT DEFAULT 0,
        created_time DATETIME NOT NULL,
        updated_time DATETIME NOT NULL
    )
    """
    
    # 创建评论表
    create_comments_table = """
    CREATE TABLE IF NOT EXISTS comments (
        id VARCHAR(36) PRIMARY KEY,
        book_id VARCHAR(36) NOT NULL,
        user_id VARCHAR(36) NOT NULL,
        content TEXT NOT NULL,
        rating INT NOT NULL,
        created_time DATETIME NOT NULL,
        FOREIGN KEY (book_id) REFERENCES books(id) ON DELETE CASCADE,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    """
    
    try:
        cursor.execute(create_users_table)
        cursor.execute(create_books_table)
        cursor.execute(create_comments_table)
        connection.commit()
        print("所有表创建成功")
    except mysql.connector.Error as error:
        print(f"创建表失败: {error}")
    finally:
        cursor.close()

def init_database():
    """初始化数据库"""
    connection = create_connection()
    if connection:
        create_tables(connection)
        connection.close()

if __name__ == "__main__":
    init_database()