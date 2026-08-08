import os
from pathlib import Path

# Required environment variables
REQUIRED_ENV_VARS = {
    "BOT_TOKEN": "Telegram Bot Token",
    "DATABASE_URL": "Database URL (e.g., postgresql://user:pass@host:5432/db)",
    "CONTENT_API": "Content API URL",
}

ENV_FILE = Path(__file__).parent.parent.parent / ".env"


def load_env():
    """Load environment variables from .env file and prompt for missing ones."""
    # Environment variables take precedence over values stored in .env.
    env_vars = {
        name: os.environ[name]
        for name in REQUIRED_ENV_VARS
        if os.environ.get(name)
    }

    # Load existing .env file
    if ENV_FILE.exists():
        with open(ENV_FILE, "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, _, value = line.partition("=")
                    env_vars.setdefault(
                        key.strip(), value.strip().strip('"').strip("'")
                    )

    # Check for missing variables and prompt user
    missing_vars = []
    for var_name, description in REQUIRED_ENV_VARS.items():
        if var_name not in env_vars or not env_vars[var_name]:
            missing_vars.append((var_name, description))

    if missing_vars:
        print("\n" + "=" * 50)
        print("⚠️  Missing environment variables detected!")
        print("=" * 50)
        for var_name, description in missing_vars:
            value = input(f"\n{description}\nEnter {var_name}: ").strip()
            env_vars[var_name] = value

        # Save to .env file
        with open(ENV_FILE, "a") as f:
            for var_name, description in missing_vars:
                f.write(f'{var_name}="{env_vars[var_name]}"\n')
        print(f"\n✅ Variables saved to {ENV_FILE}")

    # Set environment variables
    for key, value in env_vars.items():
        if key not in os.environ:
            os.environ[key] = value

    return env_vars


# Load environment variables on import
load_env()

BOT_TOKEN = os.environ["BOT_TOKEN"]
DATABASE_URL = os.environ["DATABASE_URL"]
CONTENT_API = os.environ["CONTENT_API"]
