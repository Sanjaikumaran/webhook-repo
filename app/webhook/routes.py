from flask import Blueprint, request, jsonify
from datetime import datetime
import uuid
from ..extensions import mongo

webhook = Blueprint('Webhook', __name__, url_prefix='/webhook')

@webhook.route('/receiver', methods=["POST"])
def receiver():
    payload = request.json
    event = request.headers.get("X-GitHub-Event")

    doc = {
        "request_id": str(uuid.uuid4()),
        "timestamp": datetime.utcnow()
    }

    if event == "push":
        doc.update({
            "author": payload["pusher"]["name"],
            "action": "push",
            "from_branch": None,
            "to_branch": payload["ref"].split("/")[-1]
        })

    elif event == "pull_request":
        pr = payload["pull_request"]
        pr_action = payload.get("action")

        if pr_action == "opened":
            action = "pull_request"

        elif pr_action == "reopened":
            action = "reopened"

        elif pr_action == "closed" and pr.get("merged") is True:
            action = "merge"

        elif pr_action == "closed":
            action = "closed"

        else:
            return jsonify({"status": "ignored"}), 200

        doc.update({
            "author": pr["user"]["login"],
            "action": action,
            "from_branch": pr["head"]["ref"],
            "to_branch": pr["base"]["ref"]
        })

    else:
        return jsonify({"status": "ignored"}), 200

    mongo.db.events.insert_one(doc)
    return jsonify({"status": "stored"}), 200

@webhook.route('/events', methods=["GET"])
def get_events():
    docs = list(mongo.db.events.find().sort("timestamp", -1).limit(20))

    events = []

    for d in docs:
        ts = d["timestamp"].strftime("%d %B %Y - %I:%M %p UTC")

        events.append({
            "request_id": d["request_id"],
            "author": d["author"],
            "action": d["action"],
            "from_branch": d["from_branch"],
            "to_branch": d["to_branch"],
            "timestamp": d["timestamp"].isoformat()
        })

    return jsonify(events)