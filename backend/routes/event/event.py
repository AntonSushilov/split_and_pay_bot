from flask import Blueprint, request, jsonify
from models import db, User, Event, EventParticipant
from utils import validate_telegram_webapp_hash, parse_webapp_init_data
from urllib.parse import parse_qsl

import os

event_bp = Blueprint("event", __name__, url_prefix="/event")

BOT_TOKEN = os.getenv("BOT_TOKEN")


@event_bp.route("/add", methods=["POST"], strict_slashes=False)
def addEvent():
    data = request.json
    event_data = data.get("eventItem", "")
    print("Event data:", event_data)
    # Проверка наличия initData
    if not event_data:
        return jsonify({"ok": False, "error": "event_data is required"}), 400

    # Извлечение данных
    try:
        event = Event(
            title=event_data["title"],
            description=event_data["description"],
            created_by=event_data["user_id"]
        )
        db.session.add(event)
        db.session.commit()
        participant = EventParticipant(
            event_id=event.id,
            user_id=event.created_by
        )
        db.session.add(participant)
        db.session.commit()
        return jsonify({
            "ok": True,
            "eventItem": event.to_dict()  # Assuming User model has a to_dict method
        })
    except ValueError as e:
        return jsonify({"ok": False, "error": str(e)}), 400
