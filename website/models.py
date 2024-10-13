from . import db
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from sqlalchemy.sql import func
from datetime import datetime
import pytz
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy import UniqueConstraint

def get_itc_time():
    itc_timezone = pytz.timezone('Asia/Kolkata')
    return datetime.now(itc_timezone)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    university = db.Column(db.String(160), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    date_created = db.Column(db.DateTime, default=get_itc_time)
    phone = db.Column(db.String(100), unique=False)
    linkedin = db.Column(db.String(100), unique=False)
    github = db.Column(db.String(100), unique=False)
    birthday = db.Column(db.String(50), unique=False)
    gender = db.Column(db.String(50), unique=False)
    bio = db.Column(db.String(180), unique=False)
    experience = db.Column(db.JSON, nullable=True)
    last_post_date = db.Column(db.Date, nullable=True)
    daily_streak = db.Column(db.Integer, default=0)
    coins = db.Column(db.Integer, default=0)
    profile_picture = db.Column(db.String(100), nullable=True)
    image_url = db.Column(db.String(200), nullable=True)
    verified = db.Column(db.Boolean, default=False)
    posts = db.relationship('BlogPost', backref='author', lazy=True)
    oauth_tokens = db.relationship('OAuthToken', back_populates='user', cascade='all, delete-orphan')


class OAuthToken(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    provider = db.Column(db.String(50), nullable=False)
    access_token = db.Column(db.String(500), nullable=False)
    refresh_token = db.Column(db.String(500), nullable=True)
    token_expiry = db.Column(db.DateTime, nullable=False)
    user = db.relationship('User', back_populates='oauth_tokens')


class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.TEXT, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now)
    endpoint = db.Column(db.String(120), nullable=False, unique=True)
    img_url = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


class BasicPage(db.Model):
    __tablename__ = 'basicpage'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    content = db.Column(db.Text, nullable=False)


class Pageadv(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    content = db.Column(db.Text, nullable=False)


class Pagemod(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    content = db.Column(db.Text, nullable=False)


class Bookmark(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    blog_id = db.Column(db.Integer, db.ForeignKey('blog_post.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('bookmarks', lazy=True))
    blog = db.relationship('BlogPost', backref=db.backref('bookmarks', lazy=True))
    __table_args__ = (
        UniqueConstraint('user_id', 'blog_id'),
    )


class Upvote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    blog_id = db.Column(db.Integer, db.ForeignKey('blog_post.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('upvotes', lazy=True))
    blog = db.relationship('BlogPost', backref=db.backref('upvotes', lazy=True))
    __table_args__ = (
        UniqueConstraint('user_id', 'blog_id'),
    )


class Devote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    blog_id = db.Column(db.Integer, db.ForeignKey('blog_post.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('devotes', lazy=True))
    blog = db.relationship('BlogPost', backref=db.backref('devotes', lazy=True))
    __table_args__ = (
        UniqueConstraint('user_id', 'blog_id'),
    )


class Profilepic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    bio = db.Column(db.Text, nullable=True)
    profile_picture = db.Column(db.String(255), default='default.jpg')

    def __repr__(self):
        return f"User('{self.username}', '{self.profile_picture}')"


class ContactMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    subject = db.Column(db.String(255), nullable=False)
    message = db.Column(db.String(2000), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now, nullable=False)


class cpppages(db.Model):
    __tablename__ = 'cpppages'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    post_date = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)


class cpages(db.Model):
    __tablename__ = 'cpages'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    post_date = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)