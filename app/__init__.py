from typing import Optional, Union

from flask import Flask, request, render_template
from flask_babel import Babel
import logging

from app.utils.db import migrate
from app.utils.logger import setup_logger


def create_app(env: Optional[Union[str, object]]) -> Flask:
    # Load environment variables
    from app.utils.env_loader import load_dotenv
    load_dotenv()

    # Initialize app
    _app = Flask(
        __name__,
        template_folder="../templates",
        static_folder="../static",
        static_url_path="/",
    )

    _app.config.from_object(env)

    # logger setting up
    setup_logger(_app)

    # Initialize extensions
    from app.utils import db, csrf, bcrypt, login_manager

    db.init_app(_app)
    migrate.init_app(_app, db)
    csrf.init_app(_app)
    bcrypt.init_app(_app)
    login_manager.init_app(_app)
    login_manager.login_view = "admin_routes.login"  # redirect nếu chưa login

    def get_locale():
        lang = request.cookies.get("lang")
        if lang:
            return lang
        try:
            from app.utils.settings import get_setting
            db_lang = get_setting("language")
            if db_lang:
                return db_lang
        except Exception:
            pass
        return _app.config["BABEL_DEFAULT_LOCALE"]

    Babel(_app, locale_selector=get_locale)

    # Register custom Jinja filters and context processors
    from app.utils.settings import format_currency, get_currency_symbol

    _app.jinja_env.filters["format_currency"] = format_currency

    @_app.context_processor
    def inject_currency_symbol():
        return dict(currency_symbol=get_currency_symbol())

    @_app.context_processor
    def inject_system_settings():
        from app.utils.settings import get_setting
        return dict(
            system_name=get_setting("system_name"),
            system_logo=get_setting("system_logo")
        )

    # Create database tables
    import app.admin.models
    import app.homepage.models

    # Register blueprints
    from app.admin import Admin
    from app.homepage import Homepage

    Admin(_app).register()
    Homepage(_app).register()

    # error handler
    @_app.errorhandler(404)
    def page_not_found(e):
        # note that we set the 404 status explicitly
        return render_template("404.html"), 404

    @_app.errorhandler(500)
    def internal_server_error(e):
        return render_template("404.html"), 500

    # Seed default admin user if database is initialized but no user exists
    with _app.app_context():
        try:
            db.create_all()
            import os
            from app.admin.models.user import User
            # Check if there are any users in the database
            if not User.query.first():
                username = os.environ.get("DEFAULT_ADMIN_USERNAME", "admin")
                password = os.environ.get("DEFAULT_ADMIN_PASSWORD", "gemini_admin")
                email = os.environ.get("DEFAULT_ADMIN_EMAIL", "admin@gemini.co.jp")

                if username and password:
                    admin_user = User(
                        username=username,
                        email=email,
                        role="admin",
                        status="Active"
                    )
                    admin_user.set_password(password)
                    db.session.add(admin_user)
                    db.session.commit()
                    _app.logger.info(f"Imported default admin user '{username}' successfully.")
        except Exception as e:
            # Silence exception (OperationalError, ProgrammingError, etc.)
            # so that migrations/scripts can run even if DB isn't fully set up yet.
            pass

    return _app
