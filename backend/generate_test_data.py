import os
import uuid
import random
from datetime import datetime, timedelta
import mysql.connector
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash
import os

# 加载环境变量
load_dotenv()

# 数据库连接函数
def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME')
        )
        return connection
    except mysql.connector.Error as error:
        print(f"数据库连接失败: {error}")
        return None

# 测试数据生成函数
def generate_test_data():
    """生成测试数据"""
    connection = get_db_connection()
    if not connection:
        print("无法连接到数据库，无法生成测试数据")
        return
    
    cursor = connection.cursor()
    
    try:
        # ------------------------------
        # 生成测试用户数据
        # ------------------------------
        print("生成测试用户数据...")
        
        # 用户头像链接模板（使用较短的URL以符合varchar(255)限制）
        avatar_templates = [
            "https://randomuser.me/api/portraits/men/32.jpg",
            "https://randomuser.me/api/portraits/women/44.jpg",
            "https://randomuser.me/api/portraits/men/76.jpg",
            "https://randomuser.me/api/portraits/women/22.jpg",
            "https://randomuser.me/api/portraits/men/12.jpg"
        ]
        
        # 用户数据
        users = [
            {"name": "张三", "password": "password123", "mobile": "13800138001", "cover": random.choice(avatar_templates)},
            {"name": "李四", "password": "password123", "mobile": "13800138002", "cover": random.choice(avatar_templates)},
            {"name": "王五", "password": "password123", "mobile": "13800138003", "cover": random.choice(avatar_templates)},
            {"name": "赵六", "password": "password123", "mobile": "13800138004", "cover": random.choice(avatar_templates)},
            {"name": "钱七", "password": "password123", "mobile": "13800138005", "cover": random.choice(avatar_templates)},
            {"name": "孙八", "password": "password123", "mobile": "13800138006", "cover": random.choice(avatar_templates)},
            {"name": "周九", "password": "password123", "mobile": "13800138007", "cover": random.choice(avatar_templates)},
            {"name": "吴十", "password": "password123", "mobile": "13800138008", "cover": random.choice(avatar_templates)}
        ]
        
        # 存储生成的用户ID，用于后续生成评论
        user_ids = []
        
        # 插入用户数据
        for user in users:
            # 检查用户是否已存在
            cursor.execute("SELECT id FROM users WHERE mobile = %s", (user['mobile'],))
            existing_user = cursor.fetchone()
            
            if not existing_user:
                user_id = str(uuid.uuid4())
                hashed_password = generate_password_hash(user['password'])
                now = datetime.now()
                
                cursor.execute(
                    "INSERT INTO users (id, name, password, mobile, cover, created_time, updated_time) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                    (user_id, user['name'], hashed_password, user['mobile'], user['cover'], now, now)
                )
                user_ids.append(user_id)
            else:
                user_ids.append(existing_user[0])
        
        connection.commit()
        print(f"成功插入 {len(user_ids)} 个用户")
        
        # ------------------------------
        # 生成测试书籍数据
        # ------------------------------
        print("生成测试书籍数据...")
        
        # 书籍封面链接模板（使用较短的URL以符合varchar(255)限制）
        cover_templates = [
            "https://picsum.photos/id/1/200/300",
            "https://picsum.photos/id/20/200/300",
            "https://picsum.photos/id/42/200/300",
            "https://picsum.photos/id/65/200/300",
            "https://picsum.photos/id/99/200/300",
            "https://picsum.photos/id/119/200/300",
            "https://picsum.photos/id/142/200/300",
            "https://picsum.photos/id/167/200/300",
            "https://picsum.photos/id/192/200/300"
        ]
        
        # 书籍数据
        books = [
            {
                "name": "三体",
                "author": "刘慈欣",
                "publisher": "重庆出版社",
                "publisher_date": "2008-01-01",
                "description": "科幻小说，讲述了人类文明与三体文明之间的故事。三体问题、黑暗森林理论、降维打击等科幻概念深入人心。",
                "cover": random.choice(cover_templates),
                "url": "https://example.com/books/santi",
                "hot": random.randint(100, 1000),
                "recommend": random.randint(10, 100)
            },
            {
                "name": "活着",
                "author": "余华",
                "publisher": "作家出版社",
                "publisher_date": "1993-01-01",
                "description": "讲述了农村人福贵悲惨的人生遭遇。福贵本是个阔少爷，可他嗜赌如命，终于赌光了家业，一贫如洗。他的父亲被他活活气死，母亲则在穷困中患了重病...",
                "cover": random.choice(cover_templates),
                "url": "https://example.com/books/huozhe",
                "hot": random.randint(100, 1000),
                "recommend": random.randint(10, 100)
            },
            {
                "name": "围城",
                "author": "钱钟书",
                "publisher": "人民文学出版社",
                "publisher_date": "1947-01-01",
                "description": "描绘了抗战初期知识分子的群像，讲述了方鸿渐留学回国后在爱情、婚姻、事业上的种种遭遇。",
                "cover": random.choice(cover_templates),
                "url": "https://example.com/books/weicheng",
                "hot": random.randint(100, 1000),
                "recommend": random.randint(10, 100)
            },
            {
                "name": "百年孤独",
                "author": "加西亚·马尔克斯",
                "publisher": "南海出版公司",
                "publisher_date": "2011-06-01",
                "description": "魔幻现实主义文学的代表作，描写了布恩迪亚家族七代人的传奇故事，以及加勒比海沿岸小镇马孔多的百年兴衰，反映了拉丁美洲一个世纪以来风云变幻的历史。",
                "cover": random.choice(cover_templates),
                "url": "https://example.com/books/bainiangudu",
                "hot": random.randint(100, 1000),
                "recommend": random.randint(10, 100)
            },
            {
                "name": "解忧杂货店",
                "author": "东野圭吾",
                "publisher": "南海出版公司",
                "publisher_date": "2014-05-01",
                "description": "僻静的街道旁有一家杂货店，只要写下烦恼投进店前门卷帘门的投信口，第二天就会在店后的牛奶箱里得到回答：因男友身患绝症，年轻女孩月兔在爱情与梦想间徘徊...",
                "cover": random.choice(cover_templates),
                "url": "https://example.com/books/jieyouzhahuodian",
                "hot": random.randint(100, 1000),
                "recommend": random.randint(10, 100)
            },
            {
                "name": "红楼梦",
                "author": "曹雪芹",
                "publisher": "人民文学出版社",
                "publisher_date": "1982-03-01",
                "description": "中国古典四大名著之首，清代作家曹雪芹创作的章回体长篇小说。小说以贾、史、王、薛四大家族的兴衰为背景，以贾府的家庭琐事、闺阁闲情为脉络...",
                "cover": random.choice(cover_templates),
                "url": "https://example.com/books/hongloumeng",
                "hot": random.randint(100, 1000),
                "recommend": random.randint(10, 100)
            },
            {
                "name": "西游记",
                "author": "吴承恩",
                "publisher": "人民文学出版社",
                "publisher_date": "1980-05-01",
                "description": "中国古典四大名著之一，明代小说家吴承恩所著中国古代第一部浪漫主义长篇神魔小说。主要描写孙悟空、猪八戒、沙僧三人保护唐僧西行取经...",
                "cover": random.choice(cover_templates),
                "url": "https://example.com/books/xiyouji",
                "hot": random.randint(100, 1000),
                "recommend": random.randint(10, 100)
            },
            {
                "name": "水浒传",
                "author": "施耐庵",
                "publisher": "人民文学出版社",
                "publisher_date": "1975-01-01",
                "description": "中国古典四大名著之一，元末明初施耐庵编著的章回体长篇小说。全书通过描写梁山好汉反抗压迫、水泊梁山壮大和受宋朝招安，以及受招安后为宋朝征战...",
                "cover": random.choice(cover_templates),
                "url": "https://example.com/books/shuihuzhuan",
                "hot": random.randint(100, 1000),
                "recommend": random.randint(10, 100)
            },
            {
                "name": "三国演义",
                "author": "罗贯中",
                "publisher": "人民文学出版社",
                "publisher_date": "1973-01-01",
                "description": "中国古典四大名著之一，是中国第一部长篇章回体历史演义小说，全名为《三国志通俗演义》。作者是元末明初的著名小说家罗贯中。",
                "cover": random.choice(cover_templates),
                "url": "https://example.com/books/sanguoyanyi",
                "hot": random.randint(100, 1000),
                "recommend": random.randint(10, 100)
            },
            {
                "name": "哈利·波特与魔法石",
                "author": "J.K.罗琳",
                "publisher": "人民文学出版社",
                "publisher_date": "2000-09-01",
                "description": "哈利·波特系列小本的第1部。主要讲述了自幼父母双亡的孤儿哈利·波特收到霍格沃茨魔法学校的邀请，前去学习魔法，之后遭遇的一系列历险。",
                "cover": random.choice(cover_templates),
                "url": "https://example.com/books/harrypotter1",
                "hot": random.randint(100, 1000),
                "recommend": random.randint(10, 100)
            },
            {
                "name": "小王子",
                "author": "安托万·德·圣埃克苏佩里",
                "publisher": "人民文学出版社",
                "publisher_date": "2003-08-01",
                "description": "讲述了小王子从自己星球出发前往地球的过程中，所经历的各种历险。作者以小王子的孩子式的眼光，透视出成人的空虚、盲目，愚妄和死板教条...",
                "cover": random.choice(cover_templates),
                "url": "https://example.com/books/xiaowangzi",
                "hot": random.randint(100, 1000),
                "recommend": random.randint(10, 100)
            },
            {
                "name": "追风筝的人",
                "author": "卡勒德·胡赛尼",
                "publisher": "上海人民出版社",
                "publisher_date": "2006-05-01",
                "description": "以温暖细腻的笔法勾勒人性的本质与救赎，读来令人荡气回肠。12岁的阿富汗富家少爷阿米尔被他父亲仆人儿子哈桑之间的友情故事...",
                "cover": random.choice(cover_templates),
                "url": "https://example.com/books/zhuifengzhengderen",
                "hot": random.randint(100, 1000),
                "recommend": random.randint(10, 100)
            }
        ]
        
        # 存储生成的书籍ID，用于后续生成评论
        book_ids = []
        
        # 插入书籍数据
        for book in books:
            # 检查书籍是否已存在
            cursor.execute("SELECT id FROM books WHERE name = %s AND author = %s", (book['name'], book['author']))
            existing_book = cursor.fetchone()
            
            if not existing_book:
                book_id = str(uuid.uuid4())
                # 随机生成创建时间，在过去一年内
                days_ago = random.randint(0, 365)
                created_time = datetime.now() - timedelta(days=days_ago)
                
                cursor.execute(
                    "INSERT INTO books (id, name, author, publisher, publisher_date, description, cover, url, hot, recommend, created_time, updated_time) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    (book_id, book['name'], book['author'], book['publisher'], book['publisher_date'], 
                     book['description'], book['cover'], book['url'], book['hot'], book['recommend'], 
                     created_time, created_time)
                )
                book_ids.append(book_id)
            else:
                book_ids.append(existing_book[0])
        
        connection.commit()
        print(f"成功插入 {len(book_ids)} 本书籍")
        
        # ------------------------------
        # 生成测试评论数据
        # ------------------------------
        print("生成测试评论数据...")
        
        # 评论内容模板
        comment_templates = [
            "这本书写得非常好，强烈推荐给大家！",
            "故事情节跌宕起伏，人物形象鲜明，值得一读。",
            "作者的文笔很细腻，读起来很舒服。",
            "内容很有深度，让人思考良多。",
            "这本书改变了我的一些看法，感谢作者。",
            "整体还不错，但有些地方节奏有点慢。",
            "一般般吧，没有特别惊艳的地方。",
            "不太符合我的口味，可能其他人会喜欢。",
            "失望，没有达到预期的效果。",
            "浪费时间，不推荐阅读。"
        ]
        
        # 为每本书生成多条评论
        comment_count = 0
        
        for book_id in book_ids:
            # 为每本书生成3-8条评论
            num_comments = random.randint(3, 8)
            
            for _ in range(num_comments):
                comment_id = str(uuid.uuid4())
                user_id = random.choice(user_ids)
                content = random.choice(comment_templates)
                rating = random.randint(1, 5)  # 1-5星评分
                
                # 随机生成评论时间，在书籍创建时间之后
                cursor.execute("SELECT created_time FROM books WHERE id = %s", (book_id,))
                book_created_time = cursor.fetchone()[0]
                
                # 如果是datetime对象，转换为datetime类型
                if isinstance(book_created_time, str):
                    book_created_time = datetime.strptime(book_created_time, '%Y-%m-%d %H:%M:%S')
                
                # 计算最大可能的天数差
                max_days = (datetime.now() - book_created_time).days
                if max_days < 1:
                    max_days = 1
                
                # 随机生成评论时间
                days_after = random.randint(0, max_days)
                comment_time = book_created_time + timedelta(days=days_after)
                
                # 插入评论
                cursor.execute(
                    "INSERT INTO comments (id, book_id, user_id, content, rating, created_time) VALUES (%s, %s, %s, %s, %s, %s)",
                    (comment_id, book_id, user_id, content, rating, comment_time)
                )
                
                comment_count += 1
        
        connection.commit()
        print(f"成功插入 {comment_count} 条评论")
        
        print("\n测试数据生成完成！")
        print(f"- 生成用户: {len(user_ids)} 个")
        print(f"- 生成书籍: {len(book_ids)} 本")
        print(f"- 生成评论: {comment_count} 条")
        
    except mysql.connector.Error as error:
        print(f"生成测试数据失败: {error}")
        connection.rollback()
    finally:
        cursor.close()
        connection.close()

if __name__ == "__main__":
    generate_test_data()