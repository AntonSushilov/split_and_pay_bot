from flask import Flask
from flask_cors import CORS
from models import db
from routes import auth_bp, event_bp
from dotenv import load_dotenv, dotenv_values
import os
app = Flask(__name__)
CORS(app, origins=["*"])
db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'splitandpay.db'))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
load_dotenv(".env")
# # Получить все ключи
# env_vars = dotenv_values()

# # Очистить из os.environ
# for key in env_vars.keys():
#     os.environ.pop(key, None)

db.init_app(app)

app.register_blueprint(auth_bp)
app.register_blueprint(event_bp)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
