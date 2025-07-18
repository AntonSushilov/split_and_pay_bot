from flask import Blueprint, request, jsonify
from models import db, User
from utils import validate_telegram_webapp_hash, parse_webapp_init_data
from urllib.parse import parse_qsl

import os

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

BOT_TOKEN = os.getenv("BOT_TOKEN")


@auth_bp.route("/", methods=["POST"], strict_slashes=False)
def auth():
    data = request.json
    init_data = data.get("initData", "")
    # Проверка наличия initData
    if not init_data:
        return jsonify({"ok": False, "error": "initData is required"}), 400
    # Проверка подписи
    isValid = validate_telegram_webapp_hash(BOT_TOKEN, init_data)
    if not isValid:
        return jsonify({"ok": False, "error": "Invalid signature"}), 403
    # Извлечение данных
    try:
        parsed = parse_webapp_init_data(BOT_TOKEN, init_data)
        print("Parsed data:", parsed.user)
        user = User.query.filter_by(tg_id=parsed.user.id).first()
        if not user:
            user = User(
                tg_id=parsed.user.id,
                first_name=parsed.user.first_name,
                last_name=parsed.user.last_name,
                username=parsed.user.username
            )
            db.session.add(user)
            db.session.commit()
        return jsonify({
            "ok": True,
            "user": user.to_dict()  # Assuming User model has a to_dict method
        })
    except ValueError as e:
        return jsonify({"ok": False, "error": str(e)}), 400


@auth_bp.route("/update-phone", methods=["POST"], strict_slashes=False)
def updatePhoneNumber():
    data = request.json
    contact = data.get("contact", "")
    # Проверка наличия initData
    if not contact:
        return jsonify({"ok": False, "error": "Contact is required"}), 400
    # Извлечение данных
    try:
        user = User.query.filter_by(tg_id=contact["user_id"]).first()
        if not user:
            return jsonify({"ok": False, "error": "User not found"}), 404
        user.phone = contact["phone_number"]  # предполагается, что поле phone есть в модели User
        db.session.commit()
        return jsonify({
            "ok": True,
            "user": user.to_dict()  # Assuming User model has a to_dict method
        })
    except ValueError as e:
        return jsonify({"ok": False, "error": str(e)}), 400
