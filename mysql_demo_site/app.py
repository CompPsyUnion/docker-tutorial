import os
import logging
import mysql.connector
from flask import Flask

# Suppress Flask development server warning
log = logging.getLogger("werkzeug")
log.setLevel(logging.ERROR)

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
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Docker Compose Tutorial</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                min-height: 100vh;
                margin: 0;
                background-color: #f5f5f5;
            }
            h1 { color: #333; }
            a.button {
                display: inline-block;
                padding: 12px 24px;
                margin-top: 20px;
                background-color: #007acc;
                color: white;
                text-decoration: none;
                border-radius: 6px;
                font-size: 16px;
                transition: background-color 0.2s;
            }
            a.button:hover {
                background-color: #005fa3;
            }
        </style>
    </head>
    <body>
        <h1>Hello, Docker Compose!</h1>
        <p>Test your MySQL database connection:</p>
        <a href="/mysql" class="button">Test MySQL Connection</a>
    </body>
    </html>
    """


@app.route("/mysql")
def mysql_test():
    """Test MySQL connection and display result."""
    success, message = test_mysql_connection()
    config = get_mysql_config()

    status_color = "#28a745" if success else "#dc3545"
    status_text = "Connected" if success else "Failed"

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>MySQL Connection Test</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                min-height: 100vh;
                margin: 0;
                background-color: #f5f5f5;
            }}
            .container {{
                background: white;
                padding: 40px;
                border-radius: 12px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                text-align: center;
                max-width: 400px;
            }}
            h1 {{ color: #333; margin-bottom: 10px; }}
            .status {{
                display: inline-block;
                padding: 8px 16px;
                border-radius: 20px;
                color: white;
                font-weight: bold;
                margin: 10px 0;
                background-color: {status_color};
            }}
            .message {{
                color: #666;
                margin: 10px 0;
            }}
            .config {{
                background: #f8f9fa;
                padding: 15px;
                border-radius: 8px;
                text-align: left;
                margin: 20px 0;
                font-size: 14px;
            }}
            .config p {{
                margin: 5px 0;
                color: #555;
            }}
            .config span {{
                color: #333;
                font-weight: 500;
            }}
            a.button {{
                display: inline-block;
                padding: 12px 24px;
                background-color: #6c757d;
                color: white;
                text-decoration: none;
                border-radius: 6px;
                font-size: 16px;
                transition: background-color 0.2s;
            }}
            a.button:hover {{
                background-color: #5a6268;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>MySQL Connection</h1>
            <div class="status">{status_text}</div>
            <p class="message">{message}</p>
            <div class="config">
                <p>Host: <span>{config['host']}</span></p>
                <p>Port: <span>{config['port']}</span></p>
                <p>User: <span>{config['user']}</span></p>
                <p>Database: <span>{config['database']}</span></p>
            </div>
            <a href="/" class="button">Back to Home</a>
        </div>
    </body>
    </html>
    """


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
