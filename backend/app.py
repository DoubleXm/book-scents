import os
import uuid
import json
import os
from datetime import datetime, timedelta
from flask import Flask, request, jsonify, current_app, send_from_directory
from flask_cors import CORS
import mysql.connector
import jwt
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from db_init import init_database
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 初始化数据库
init_database()

# 创建 Flask 应用
app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER', './static/uploads')
app.config['MAX_CONTENT_LENGTH'] = int(os.getenv('MAX_CONTENT_LENGTH', '16777216'))  # 16MB
app.config['BASE_URL'] = os.getenv('BASE_URL', 'http://localhost:5001')

# 确保上传目录存在
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# 允许的文件扩展名
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

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

# 检查文件扩展名是否允许
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# 生成 JWT 令牌
def generate_token(user_id):
    payload = {
        'exp': datetime.utcnow() + timedelta(days=1),  # 令牌有效期为1天
        'iat': datetime.utcnow(),
        'sub': user_id
    }
    return jwt.encode(payload, app.config['JWT_SECRET_KEY'], algorithm='HS256')

# 验证 JWT 令牌
def verify_token(token):
    try:
        payload = jwt.decode(token, app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
        return payload['sub']
    except jwt.ExpiredSignatureError:
        return None  # 令牌已过期
    except jwt.InvalidTokenError:
        return None  # 令牌无效

# 验证用户身份的装饰器
def token_required(f):
    def decorator(*args, **kwargs):
        token = None
        # 从请求头中获取令牌
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith('Bearer '):
                token = auth_header[7:]
        
        if not token:
            return jsonify({'message': '缺少令牌'}), 401
        
        user_id = verify_token(token)
        if not user_id:
            return jsonify({'message': '无效或过期的令牌'}), 401
        
        # 将用户 ID 添加到请求对象中
        request.user_id = user_id
        return f(*args, **kwargs)
    
    decorator.__name__ = f.__name__
    return decorator

# 注册接口
@app.route('/api/v1/register', methods=['POST'])
def register():
    data = request.get_json()
    
    # 验证输入数据
    if not data or 'username' not in data or 'password' not in data or 'mobile' not in data:
        return jsonify({'message': '缺少必要的参数'}), 400
    
    username = data['username']
    password = data['password']
    mobile = data['mobile']
    
    # 检查手机号是否已注册
    connection = get_db_connection()
    if not connection:
        return jsonify({'message': '数据库连接失败'}), 500
    
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE mobile = %s", (mobile,))
        existing_user = cursor.fetchone()
        
        if existing_user:
            return jsonify({'message': '该手机号已注册'}), 400
        
        # 生成用户 ID 和密码哈希
        user_id = str(uuid.uuid4())
        hashed_password = generate_password_hash(password)
        now = datetime.now()
        
        # 插入新用户
        cursor.execute(
            "INSERT INTO users (id, name, password, mobile, cover, created_time, updated_time) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (user_id, username, hashed_password, mobile, 'default_avatar.png', now, now)
        )
        connection.commit()
        
        # 获取用户信息
        cursor.execute("SELECT id, name, cover, mobile FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()
        
        # 生成 JWT 令牌
        token = generate_token(user_id)
        
        return jsonify({
            'profile': user,
            'token': token
        })
    except mysql.connector.Error as error:
        print(f"注册失败: {error}")
        return jsonify({'message': '注册失败，请重试'}), 500
    finally:
        cursor.close()
        connection.close()

# 登录接口
@app.route('/api/v1/login', methods=['POST'])
def login():
    data = request.get_json()
    
    # 验证输入数据
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'message': '缺少必要的参数'}), 400
    
    username = data['username']
    password = data['password']
    
    connection = get_db_connection()
    if not connection:
        return jsonify({'message': '数据库连接失败'}), 500
    
    try:
        cursor = connection.cursor(dictionary=True)
        # 可以通过用户名或手机号登录
        cursor.execute("SELECT * FROM users WHERE name = %s OR mobile = %s", (username, username))
        user = cursor.fetchone()
        
        if not user or not check_password_hash(user['password'], password):
            return jsonify({'message': '用户名或密码错误'}), 401
        
        # 生成 JWT 令牌
        token = generate_token(user['id'])
        
        # 返回用户信息（不包含密码）
        user_profile = {
            'id': user['id'],
            'name': user['name'],
            'cover': user['cover'],
            'mobile': user['mobile']
        }
        
        return jsonify({
            'token': token,
            'profile': user_profile
        })
    except mysql.connector.Error as error:
        print(f"登录失败: {error}")
        return jsonify({'message': '登录失败，请重试'}), 500
    finally:
        cursor.close()
        connection.close()

# 获取用户信息接口
@app.route('/api/v1/user', methods=['GET'])
@token_required
def get_user():
    user_id = request.user_id
    
    connection = get_db_connection()
    if not connection:
        return jsonify({'message': '数据库连接失败'}), 500
    
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT id, name, cover, mobile FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()
        
        if not user:
            return jsonify({'message': '用户不存在'}), 404
        
        return jsonify(user)
    except mysql.connector.Error as error:
        print(f"获取用户信息失败: {error}")
        return jsonify({'message': '获取用户信息失败'}), 500
    finally:
        cursor.close()
        connection.close()

# 获取书籍列表接口
@app.route('/api/v1/books', methods=['GET'])
def get_books():
    # 获取查询参数
    page_size = request.args.get('pageSize', default=10, type=int)
    page_num = request.args.get('pageNum', default=1, type=int)
    name = request.args.get('name', default='', type=str)
    order = request.args.get('order', default='DESC', type=str)
    filed = request.args.get('filed', default='', type=str)
    
    # 验证排序字段和顺序
    if order not in ['ASC', 'DESC']:
        order = 'DESC'
    
    if filed not in ['HOT', 'RECOMMEND', '']:
        filed = ''
    
    # 计算偏移量
    offset = (page_num - 1) * page_size
    
    connection = get_db_connection()
    if not connection:
        return jsonify({'message': '数据库连接失败'}), 500
    
    try:
        cursor = connection.cursor(dictionary=True)
        
        # 构建查询 SQL
        where_clause = """
        """
        params = []
        
        if name:
            where_clause = "WHERE name LIKE %s"
            params.append(f"%{name}%")
        
        # 构建排序 SQL
        order_by_clause = "ORDER BY created_time DESC"
        if filed == 'HOT':
            order_by_clause = f"ORDER BY hot {order}"
        elif filed == 'RECOMMEND':
            order_by_clause = f"ORDER BY recommend {order}"
        
        # 查询书籍列表
        sql = f"""
        SELECT id, name, url, description, cover, author, publisher, publisher_date, hot, recommend, created_time, updated_time
        FROM books
        {where_clause}
        {order_by_clause}
        LIMIT %s OFFSET %s
        """
        params.extend([page_size, offset])
        cursor.execute(sql, params)
        books = cursor.fetchall()
        
        # 查询总记录数
        count_sql = f"""
        SELECT COUNT(*) as count
        FROM books
        {where_clause}
        """
        cursor.execute(count_sql, params[:-2] if params[:-2] else ())
        total = cursor.fetchone()['count']
        
        # 格式化时间字段和处理cover字段
        for book in books:
            if isinstance(book['created_time'], datetime):
                book['created_time'] = book['created_time'].strftime('%Y-%m-%d %H:%M:%S')
            if isinstance(book['updated_time'], datetime):
                book['updated_time'] = book['updated_time'].strftime('%Y-%m-%d %H:%M:%S')
            # 确保cover是完整的URL
            if book['cover'] and not book['cover'].startswith(('http://', 'https://')):
                if book['cover'].startswith('/'):
                    book['cover'] = f"{app.config['BASE_URL']}{book['cover']}"
                else:
                    book['cover'] = f"{app.config['BASE_URL']}/static/{book['cover']}"
        
        return jsonify({
            'list': books,
            'total': total
        })
    except mysql.connector.Error as error:
        print(f"获取书籍列表失败: {error}")
        return jsonify({'message': '获取书籍列表失败'}), 500
    finally:
        cursor.close()
        connection.close()

# 上传书籍接口
@app.route('/api/v1/books', methods=['POST'])
@token_required
def create_book():
    # 获取表单数据
    name = request.form.get('name')
    author = request.form.get('author')
    description = request.form.get('description')
    url = request.form.get('url')
    
    # 验证必要字段
    if not name or not author or not description:
        return jsonify({'message': '缺少必要的参数'}), 400
    
    # 处理文件上传
    cover_url = ''
    if 'cover' in request.files:
        file = request.files['cover']
        if file and allowed_file(file.filename):
            # 生成唯一文件名
            filename = secure_filename(file.filename)
            unique_filename = f"{uuid.uuid4()}_{filename}"
            
            # 保存文件
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            file.save(file_path)
            
            # 构建完整的文件 URL
            cover_url = f"{app.config['BASE_URL']}/static/uploads/{unique_filename}"
    
    # 确保有默认封面
    if not cover_url:
        cover_url = f"{app.config['BASE_URL']}/static/default_book_cover.png"
    
    # 确保有默认阅读地址
    if not url:
        url = '#'
    
    connection = get_db_connection()
    if not connection:
        return jsonify({'message': '数据库连接失败'}), 500
    
    try:
        cursor = connection.cursor()
        
        # 生成书籍 ID
        book_id = str(uuid.uuid4())
        now = datetime.now()
        
        # 插入书籍
        cursor.execute(
            "INSERT INTO books (id, name, author, description, cover, url, publisher, publisher_date, hot, recommend, created_time, updated_time) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (book_id, name, author, description, cover_url, url, '', '', 0, 0, now, now)
        )
        connection.commit()
        
        return jsonify({}), 200
    except mysql.connector.Error as error:
        print(f"上传书籍失败: {error}")
        return jsonify({'message': '上传书籍失败'}), 500
    finally:
        cursor.close()
        connection.close()

# 获取书籍详情接口
@app.route('/api/v1/books/<id>', methods=['GET'])
def get_book_detail(id):
    connection = get_db_connection()
    if not connection:
        return jsonify({'message': '数据库连接失败'}), 500
    
    try:
        cursor = connection.cursor(dictionary=True)
        
        # 查询书籍基本信息
        cursor.execute(
            "SELECT id, name, author, description, cover, url FROM books WHERE id = %s",
            (id,)
        )
        book = cursor.fetchone()
        
        if not book:
            return jsonify({'message': '书籍不存在'}), 404
        
        # 查询评分统计
        cursor.execute(
            "SELECT rating, COUNT(*) as count FROM comments WHERE book_id = %s GROUP BY rating",
            (id,)
        )
        ratings = cursor.fetchall()
        
        # 计算平均评分和星级分布
        total_rating = 0
        total_count = 0
        rating_count = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        
        for item in ratings:
            rating = item['rating']
            count = item['count']
            rating_count[rating] = count
            total_rating += rating * count
            total_count += count
        
        # 计算平均评分
        average_rating = round(total_rating / total_count, 1) if total_count > 0 else 0
        
        # 计算各星级百分比
        statement = []
        for i in range(1, 6):
            percentage = round((rating_count[i] / total_count) * 100) if total_count > 0 else 0
            statement.append(percentage)
        
        # 确保cover是完整的URL
        if book['cover'] and not book['cover'].startswith(('http://', 'https://')):
            if book['cover'].startswith('/'):
                cover = f"{app.config['BASE_URL']}{book['cover']}"
            else:
                cover = f"{app.config['BASE_URL']}/static/{book['cover']}"
        else:
            cover = book['cover']
        
        # 构建响应数据
        book_detail = {
            'id': book['id'],
            'name': book['name'],
            'author': book['author'],
            'description': book['description'],
            'cover': cover,
            'url': book['url'],
            'rating': average_rating,
            'statement': statement
        }
        
        return jsonify(book_detail)
    except mysql.connector.Error as error:
        print(f"获取书籍详情失败: {error}")
        return jsonify({'message': '获取书籍详情失败'}), 500
    finally:
        cursor.close()
        connection.close()

# 记录阅读次数接口
@app.route('/api/v1/books/<id>/read', methods=['PATCH'])
def record_read(id):
    connection = get_db_connection()
    if not connection:
        return jsonify({'message': '数据库连接失败'}), 500
    
    try:
        cursor = connection.cursor(dictionary=True)
        
        # 检查书籍是否存在
        cursor.execute("SELECT id FROM books WHERE id = %s", (id,))
        book = cursor.fetchone()
        
        if not book:
            return jsonify({'message': '书籍不存在'}), 404
        
        # 更新阅读次数
        cursor.execute(
            "UPDATE books SET hot = hot + 1, updated_time = %s WHERE id = %s",
            (datetime.now(), id)
        )
        connection.commit()
        
        # 获取更新后的书籍详情
        return get_book_detail(id)
    except mysql.connector.Error as error:
        print(f"记录阅读次数失败: {error}")
        return jsonify({'message': '记录阅读次数失败'}), 500
    finally:
        cursor.close()
        connection.close()

# 获取评论列表接口
@app.route('/api/v1/comments/<book_id>', methods=['GET'])
def get_comments(book_id):
    connection = get_db_connection()
    if not connection:
        return jsonify({'message': '数据库连接失败'}), 500
    
    try:
        cursor = connection.cursor(dictionary=True)
        
        # 查询评论列表及关联的用户信息
        cursor.execute(
            """
            SELECT c.id, c.content, c.rating, c.created_time, 
                   u.id as user_id, u.name as user_name, u.cover as user_cover, u.mobile as user_mobile
            FROM comments c
            JOIN users u ON c.user_id = u.id
            WHERE c.book_id = %s
            ORDER BY c.created_time DESC
            """,
            (book_id,)
        )
        comments = cursor.fetchall()
        
        # 格式化时间字段并构建返回数据
        result = []
        for comment in comments:
            # 格式化时间
            if isinstance(comment['created_time'], datetime):
                created_time = comment['created_time'].strftime('%Y-%m-%d %H:%M:%S')
            else:
                created_time = comment['created_time']
            
            # 构建用户信息
            user_info = {
                'id': comment['user_id'],
                'name': comment['user_name'],
                'cover': comment['user_cover'],
                'mobile': comment['user_mobile']
            }
            
            result.append({
                'id': comment['id'],
                'content': comment['content'],
                'rating': comment['rating'],
                'createdTime': created_time,
                'user': user_info
            })
        
        # 查询总评论数
        cursor.execute("SELECT COUNT(*) as count FROM comments WHERE book_id = %s", (book_id,))
        total = cursor.fetchone()['count']
        
        # 更新书籍的推荐数
        cursor.execute(
            "UPDATE books SET recommend = %s, updated_time = %s WHERE id = %s",
            (total, datetime.now(), book_id)
        )
        connection.commit()
        
        return jsonify({
            'list': result,
            'total': total
        })
    except mysql.connector.Error as error:
        print(f"获取评论列表失败: {error}")
        return jsonify({'message': '获取评论列表失败'}), 500
    finally:
        cursor.close()
        connection.close()

# 添加评论接口
@app.route('/api/v1/comments/<book_id>', methods=['POST'])
@token_required
def add_comment(book_id):
    user_id = request.user_id
    data = request.get_json()
    
    # 验证输入数据
    if not data or 'content' not in data or 'rating' not in data:
        return jsonify({'message': '缺少必要的参数'}), 400
    
    content = data['content']
    rating = data['rating']
    
    # 验证评分范围
    if not isinstance(rating, int) or rating < 1 or rating > 5:
        return jsonify({'message': '评分必须是1-5之间的整数'}), 400
    
    connection = get_db_connection()
    if not connection:
        return jsonify({'message': '数据库连接失败'}), 500
    
    try:
        cursor = connection.cursor(dictionary=True)
        
        # 检查书籍是否存在
        cursor.execute("SELECT id FROM books WHERE id = %s", (book_id,))
        book = cursor.fetchone()
        
        if not book:
            return jsonify({'message': '书籍不存在'}), 404
        
        # 生成评论 ID
        comment_id = str(uuid.uuid4())
        now = datetime.now()
        
        # 插入评论
        cursor.execute(
            "INSERT INTO comments (id, book_id, user_id, content, rating, created_time) VALUES (%s, %s, %s, %s, %s, %s)",
            (comment_id, book_id, user_id, content, rating, now)
        )
        connection.commit()
        
        # 获取新创建的评论信息
        cursor.execute("SELECT id, content, rating, created_time FROM comments WHERE id = %s", (comment_id,))
        comment = cursor.fetchone()
        
        # 格式化时间
        if isinstance(comment['created_time'], datetime):
            comment['created_time'] = comment['created_time'].strftime('%Y-%m-%d %H:%M:%S')
        
        return jsonify(comment)
    except mysql.connector.Error as error:
        print(f"添加评论失败: {error}")
        return jsonify({'message': '添加评论失败'}), 500
    finally:
        cursor.close()
        connection.close()

# 静态文件服务
@app.route('/uploads/<path:filename>')
def serve_uploads(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

# 主函数
if __name__ == '__main__':
    # 运行 Flask 应用
    app.run(host='0.0.0.0', port=5000, debug=True)