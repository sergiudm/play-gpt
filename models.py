# models.py
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    # 存储测评结果，比如用 JSON 字符串记录个性特征、喜好等
    personality = db.Column(db.Text)  
    # 可以扩展字段，如：旅行足迹、偏好等
    travel_history = db.Column(db.Text)
