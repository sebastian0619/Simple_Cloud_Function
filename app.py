import json
from flask import Flask, request, jsonify, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Function, APIKey
import config
import os
import importlib.util
import re

app = Flask(__name__)
app.config['SECRET_KEY'] = config.SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def init_db():
    with app.app_context():
        db.create_all()
        with open('config.json') as f:
            config_data = json.load(f)
        
        # 添加初始用户
        initial_user = config_data['initial_user']
        if not User.query.filter_by(username=initial_user['username']).first():
            hashed_password = generate_password_hash(initial_user['password'], method='pbkdf2:sha256')
            new_user = User(username=initial_user['username'], password=hashed_password)
            db.session.add(new_user)
        
        # 添加初始API密钥
        for key in config_data['api_keys']:
            if not APIKey.query.filter_by(key=key).first():
                new_api_key = APIKey(key=key)
                db.session.add(new_api_key)
        
        db.session.commit()

# 初始化数据库
init_db()

@app.before_request
def authenticate():
    if request.endpoint not in ['login', 'static', 'admin', 'delete_function', 'create_function', 'edit_function', 'update_function']:
        auth_header = request.headers.get('Authorization')
        if auth_header:
            parts = auth_header.split()
            if len(parts) == 2 and parts[0] == 'Bearer':
                api_key = APIKey.query.filter_by(key=parts[1]).first()
                if api_key:
                    return  # 鉴权成功
        return jsonify({"error": "Unauthorized"}), 401

# 动态加载函数并更新 functions.json
def load_functions():
    functions_dir = 'functions'
    functions_json_path = os.path.join(functions_dir, 'functions.json')
    
    functions_data = {}
    function_map = {}
    
    for filename in os.listdir(functions_dir):
        if filename.endswith('.py'):
            module_name = filename[:-3]
            file_path = os.path.join(functions_dir, filename)
            spec = importlib.util.spec_from_file_location(module_name, file_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            func = getattr(module, module_name, None)
            if func:
                function_map[module_name] = func
                functions_data[module_name] = {
                    "route": module_name,
                    "function_name": module_name,
                    "description": "Dynamically loaded function"
                }

    # 更新 functions.json
    with open(functions_json_path, 'w') as f:
        json.dump(functions_data, f, indent=4)

    return function_map

function_map = load_functions()

@app.route('/create_function', methods=['POST'])
@login_required
def create_function():
    route_name = request.form['route_name']
    function_code = request.form['function_code']
    
    # 提取函数名称
    match = re.search(r'def\s+(\w+)\s*\(', function_code)
    if not match:
        flash('Invalid function definition')
        return redirect(url_for('admin'))
    
    function_name = match.group(1)
    
    # 创建新的.py文件
    file_path = os.path.join('functions', f'{route_name}.py')
    with open(file_path, 'w') as f:
        f.write(function_code)
    
    # 更新functions.json
    functions_json_path = os.path.join('functions', 'functions.json')
    with open(functions_json_path, 'r') as f:
        functions_data = json.load(f)
    
    functions_data[route_name] = {
        "route": route_name,
        "function_name": function_name,
        "description": "Newly created function"
    }
    
    with open(functions_json_path, 'w') as f:
        json.dump(functions_data, f, indent=4)
    
    return redirect(url_for('admin'))

# Web UI路由
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('admin'))
        flash('Invalid username or password')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/admin', methods=['GET'])
@login_required
def admin():
    # 每次访问 admin 页面时重新加载函数
    global function_map
    function_map = load_functions()
    
    functions_json_path = os.path.join('functions', 'functions.json')
    with open(functions_json_path, 'r') as f:
        functions_data = json.load(f)
    
    return render_template('admin.html', functions=functions_data)

@app.route('/delete/<int:function_id>', methods=['POST'])
@login_required
def delete_function(function_id):
    # 根据function_id找到要删除的函数
    functions = load_functions()
    route_name = list(functions.keys())[function_id - 1]  # 使用索引来获取路由名称

    # 删除对应的.py文件
    file_path = os.path.join('functions', f'{route_name}.py')
    if os.path.exists(file_path):
        os.remove(file_path)

    # 更新functions.json
    del functions[route_name]
    functions_json_path = os.path.join('functions', 'functions.json')
    with open(functions_json_path, 'w') as f:
        json.dump(functions, f, indent=4)

    return redirect(url_for('admin'))

@app.route('/edit/<route>', methods=['GET'])
@login_required
def edit_function(route):
    functions_json_path = os.path.join('functions', 'functions.json')
    with open(functions_json_path, 'r') as f:
        functions_data = json.load(f)
    
    details = functions_data.get(route)
    
    # 读取函数代码
    file_path = os.path.join('functions', f'{route}.py')
    with open(file_path, 'r') as f:
        function_code = f.read()
    
    return render_template('edit_function.html', route=route, details=details, function_code=function_code)

@app.route('/update/<route>', methods=['POST'])
@login_required
def update_function(route):
    new_route_name = request.form['route_name']
    new_description = request.form['description']
    new_function_code = request.form['function_code']
    
    # 更新.py文件
    old_file_path = os.path.join('functions', f'{route}.py')
    new_file_path = os.path.join('functions', f'{new_route_name}.py')
    if old_file_path != new_file_path:
        if os.path.exists(new_file_path):
            os.remove(new_file_path)
        os.rename(old_file_path, new_file_path)
    with open(new_file_path, 'w') as f:
        f.write(new_function_code)
    
    # 更新functions.json
    functions_json_path = os.path.join('functions', 'functions.json')
    with open(functions_json_path, 'r') as f:
        functions_data = json.load(f)
    
    functions_data[new_route_name] = {
        "route": new_route_name,
        "function_name": new_route_name,
        "description": new_description
    }
    if new_route_name != route:
        del functions_data[route]
    
    with open(functions_json_path, 'w') as f:
        json.dump(functions_data, f, indent=4)
    
    return redirect(url_for('admin'))

@app.route('/<route>', methods=['GET', 'POST'])
def handle_function(route):
    if route in function_map:
        func = function_map[route]
        if request.method == 'POST':
            data = request.json  # 确保 data 是一个字典
        elif request.method == 'GET':
            data = request.args.to_dict()  # 将查询参数转换为字典
        return jsonify(func(data))
    return jsonify({"error": "Function not found"}), 404

# 启动应用
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888)
