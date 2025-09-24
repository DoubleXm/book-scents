import os
import mysql.connector
from dotenv import load_dotenv
import os

# 加载环境变量
load_dotenv()

def test_db_connection():
    """测试数据库连接"""
    print("测试数据库连接...")
    try:
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME')
        )
        if connection.is_connected():
            print("数据库连接成功！")
            cursor = connection.cursor()
            
            # 检查是否存在表
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            print(f"存在 {len(tables)} 个表：")
            for table in tables:
                print(f"- {table[0]}")
                
            # 检查表结构
            for table in tables:
                table_name = table[0]
                print(f"\n表 {table_name} 的结构：")
                cursor.execute(f"DESCRIBE {table_name}")
                columns = cursor.fetchall()
                for column in columns:
                    print(f"- {column[0]}: {column[1]}")
                    
            cursor.close()
        
    except mysql.connector.Error as error:
        print(f"数据库连接失败: {error}")
    finally:
        if 'connection' in locals() and connection.is_connected():
            connection.close()
            print("\n数据库连接已关闭")

if __name__ == "__main__":
    test_db_connection()