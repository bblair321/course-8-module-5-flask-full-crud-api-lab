from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory event storage using dicts
events = [
    {"id": 1, "title": "Tech Meetup"},
    {"id": 2, "title": "Python Workshop"}
]

def find_event(event_id):
    return next((event for event in events if event["id"] == event_id), None)

@app.route("/events", methods=["POST"])
def create_event():
    data = request.get_json()
    if not data or "title" not in data:
        return jsonify({"error": "Missing 'title' field"}), 400

    new_id = max((event["id"] for event in events), default=0) + 1
    new_event = {"id": new_id, "title": data["title"]}
    events.append(new_event)
    return jsonify(new_event), 201

@app.route("/events/<int:event_id>", methods=["PATCH"])
def update_event(event_id):
    event = find_event(event_id)
    if not event:
        return jsonify({"error": "Event not found"}), 404

    data = request.get_json()
    if not data or "title" not in data:
        return jsonify({"error": "Missing 'title' field"}), 400

    event["title"] = data["title"]
    return jsonify(event), 200

@app.route("/events/<int:event_id>", methods=["DELETE"])
def delete_event(event_id):
    event = find_event(event_id)
    if not event:
        return jsonify({"error": "Event not found"}), 404

    events.remove(event)
    return '', 204

if __name__ == "__main__":
    app.run(debug=True)
