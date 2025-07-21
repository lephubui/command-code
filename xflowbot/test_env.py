import os

# Manual .env parsing to bypass dotenv issues
def load_env_manual():
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    env_vars = {}
    if os.path.exists(env_path):
        try:
            with open(env_path, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        try:
                            key, value = line.split('=', 1)
                            key = key.strip()
                            value = value.strip()
                            # Remove quotes if present
                            if value.startswith('"') and value.endswith('"'):
                                value = value[1:-1]
                            elif value.startswith("'") and value.endswith("'"):
                                value = value[1:-1]
                            env_vars[key] = value
                        except ValueError:
                            print(f"Warning: Skipping malformed line {line_num}: {line}")
            print(f"Manual .env load successful. Loaded keys: {list(env_vars.keys())}")
            return env_vars
        except Exception as e:
            print(f"Failed to read .env: {str(e)}")
            return {}
    else:
        print(f".env file not found at {env_path}")
        return {}

env_vars = load_env_manual()
os.environ.update(env_vars)  # Set to os.environ for getenv

# Debug prints for confirmation
print(f"Current working dir: {os.getcwd()}")
print(f"CLIENT_ID: {os.getenv('CLIENT_ID')}")
print(f"CLIENT_SECRET: {os.getenv('CLIENT_SECRET')}")
print(f"REDIRECT_URI: {os.getenv('REDIRECT_URI')}")
print(f"CONSUMER_KEY: {os.getenv('CONSUMER_KEY') or 'NONE_FOUND'}")
print(f"CONSUMER_SECRET: {os.getenv('CONSUMER_SECRET') or 'NONE_FOUND'}")
print(f"ACCESS_TOKEN: {os.getenv('ACCESS_TOKEN') or 'NONE_FOUND'}")
print(f"ACCESS_TOKEN_SECRET: {os.getenv('ACCESS_TOKEN_SECRET') or 'NONE_FOUND'}")
