from flask import Flask
from app.auth.routes import auth_bp
# from app.campaigns.routes import campaigns_bp
# from app.analytics.routes import analytics_bp
from app.utils.firebase import initialize_firebase

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    initialize_firebase()

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    # app.register_blueprint(campaigns_bp, url_prefix='/api/campaigns')
    # app.register_blueprint(analytics_bp, url_prefix='/api/analytics')

    return app
