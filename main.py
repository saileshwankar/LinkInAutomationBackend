from flask import Flask
from flask_cors import CORS
from Routes.routes import linkin_automation_bp
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

app.register_blueprint(linkin_automation_bp)

if __name__ == "__main__":
    app.run(debug=False, port=8080)
