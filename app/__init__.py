from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from flask_cors import CORS

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # إعدادات قاعدة البيانات
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///restorate.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # سر الجلسة
    app.secret_key = 'your_secret_key'

    # إعداد الجلسات
    app.config["SESSION_TYPE"] = "filesystem"
    Session(app)

    # تفعيل CORS (للسماح بالوصول من دومينات أخرى)
    CORS(app)

    # تهيئة قاعدة البيانات
    db.init_app(app)

    # تسجيل Blueprints
    from app.routes.ratings_route import ratings_routes
    from app.routes.facilities_route import owner_facility_routes
    from app.routes.auth_route import auth_routes
    from app.routes.owner_route import owner_routes
    app.register_blueprint(owner_routes)
    app.register_blueprint(auth_routes)
    app.register_blueprint(ratings_routes)
    app.register_blueprint(owner_facility_routes)

    return app