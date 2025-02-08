# app.py
import os
from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    current_user,
    login_required,
)
import openai
from werkzeug.security import generate_password_hash, check_password_hash

# 导入 models 中的 db 和 User
from models import db, User

app = Flask(__name__)
app.config["SECRET_KEY"] = "your_secret_key"  # 替换为安全的密钥
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///playgpt.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# 初始化数据库和登录管理
db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"

# 设置 OpenAI API key（可以用环境变量存储）
openai.api_key = os.environ.get("OPENAI_API_KEY", "your_openai_api_key_here")


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# 首页
@app.route("/")
def index():
    return render_template("index.html")


# 注册页面
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        # 简单密码哈希
        hashed_password = generate_password_hash(password, method="sha256")
        if User.query.filter_by(username=username).first():
            flash("用户名已存在")
            return redirect(url_for("register"))
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash("注册成功，请登录")
        return redirect(url_for("login"))
    return render_template("register.html")


# 登录页面
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for("index"))
        else:
            flash("用户名或密码错误")
            return redirect(url_for("login"))
    return render_template("login.html")


# 注销
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


# 性格测评页面
@app.route("/personality", methods=["GET", "POST"])
@login_required
def personality():
    if request.method == "POST":
        # 假设测评题目有3题，获取答案（你可以设计更复杂的题目和评分逻辑）
        answer1 = request.form.get("answer1")
        answer2 = request.form.get("answer2")
        answer3 = request.form.get("answer3")
        # 根据答案生成用户的个性标签，比如简单示例：
        traits = []
        if answer1 == "低消费":
            traits.append("不喜欢高消费")
        if answer2 == "独自旅行":
            traits.append("喜欢独自旅行")
        if answer3 == "慢节奏":
            traits.append("喜欢悠闲慢节奏")
        # 将结果以逗号分隔存储，也可以用 JSON 格式
        personality_result = ",".join(traits)
        current_user.personality = personality_result
        db.session.commit()
        flash("测评完成，个性标签已更新！")
        return redirect(url_for("profile"))
    return render_template("personality.html")


# 个人中心页面
@app.route("/profile")
@login_required
def profile():
    return render_template("profile.html", user=current_user)


# 对话页面（展示对话框）
@app.route("/chat")
@login_required
def chat():
    return render_template("chat.html")


# API 接口：根据用户输入生成定制化出行方案
@app.route("/api/chat", methods=["POST"])
@login_required
def api_chat():
    data = request.get_json()
    user_query = data.get("message")
    # 获取用户的个性标签
    personality = current_user.personality or ""

    # 构造 prompt：结合用户个性特征和需求生成方案
    prompt = f"用户的个性特征为：{personality}。\n用户需求：{user_query}。\n请根据以上信息提供详细的出行方案，包含具体安排、时间规划和建议。"

    try:
        response = openai.Completion.create(
            engine="text-davinci-003",  # 或者你使用的其他引擎
            prompt=prompt,
            max_tokens=500,
            temperature=0.7,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )
        answer = response.choices[0].text.strip()
        return jsonify({"result": answer})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# 初始化数据库（首次运行时使用）
@app.before_request
def create_tables():
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True)
