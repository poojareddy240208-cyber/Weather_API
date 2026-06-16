from flask import Flask, jsonify, request
from weather_api import get_weather

app = Flask(__name__)

@app.route("/weather")
def weather():

    city = request.args.get("city")

    if not city:
        return jsonify({
            "error": "City parameter required"
        }), 400

    data = get_weather(city)

    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)