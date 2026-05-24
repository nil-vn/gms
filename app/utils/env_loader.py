import os

def load_dotenv(dotenv_path=None):
    """
    Load environment variables from a .env file.
    If dotenv_path is not specified, it will look for .env in the parent directory of the 'app' package.
    """
    if dotenv_path is None:
        # Find .env in the root directory (two levels up from this file)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(os.path.dirname(current_dir))
        dotenv_path = os.path.join(project_root, ".env")

    if not os.path.exists(dotenv_path):
        return

    try:
        with open(dotenv_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                # Skip empty lines and comments
                if not line or line.startswith("#"):
                    continue
                
                # Find the first '=' character
                if "=" in line:
                    key, val = line.split("=", 1)
                    key = key.strip()
                    val = val.strip()
                    
                    # Strip single/double quotes around the value
                    if (val.startswith('"') and val.endswith('"')) or (val.startswith("'") and val.endswith("'")):
                        val = val[1:-1]
                    
                    # Set the environment variable
                    os.environ[key] = val
    except Exception as e:
        # Avoid crashing startup if .env cannot be read for some reason
        pass
