import os
import mysql.connector
from flask import Flask, jsonify

app = Flask(__name__)


def get_mysql_config():
    """Get MySQL connection configuration from environment variables."""
    return {
        "host": os.environ.get("MYSQL_HOST", "localhost"),
        "port": int(os.environ.get("MYSQL_PORT", 3306)),
        "user": os.environ.get("MYSQL_USER", "root"),
        "password": os.environ.get("MYSQL_PASSWORD", ""),
        "database": os.environ.get("MYSQL_DATABASE", "testdb"),
    }


def test_mysql_connection():
    """Test MySQL connection and return status."""
    config = get_mysql_config()
    try:
        conn = mysql.connector.connect(**config)
        conn.close()
        return True, "Connection successful!"
    except mysql.connector.Error as err:
        return False, f"Connection failed: {err}"
    except Exception as err:
        return False, f"Unexpected error: {err}"


@app.route("/")
def hello():
    return "Hello, Docker Compose! Visit /mysql to test database connection."


@app.route("/mysql")
def mysql_test():
    """Test MySQL connection and display result."""
    success, message = test_mysql_connection()

    config = get_mysql_config()

    result = {
        "status": "connected" if success else "failed",
        "message": message,
        "config": {
            "host": config["host"],
            "port": config["port"],
            "user": config["user"],
            "database": config["database"],
        },
    }

    return jsonify(result)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
