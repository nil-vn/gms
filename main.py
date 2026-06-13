import os
from app.utils.env_loader import load_dotenv

# Load environment variables from .env file
load_dotenv()

from app import create_app
from app.utils.constants import ENV


env = os.environ.get(ENV.INIT.value, ENV.PRODUCTION.value)  # default is production

_app = create_app(f"config.{env}.{env.capitalize()}Config")

if __name__ == "__main__":
    try:
        from waitress import serve
        print("Starting Waitress server on http://0.0.0.0:5000")
        serve(_app, host="0.0.0.0", port=5000)
    except ImportError:
        print("Waitress not installed. Falling back to Flask development server...")
        _app.run(host="0.0.0.0", port=5000, debug=True)
