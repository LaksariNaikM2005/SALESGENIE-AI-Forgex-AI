from flask import Blueprint, jsonify, request

from ai_ml_engine.inference.predict import predict_lead


ml_bp = Blueprint("ml", __name__, url_prefix="/api/ml")


@ml_bp.route("/predict", methods=["POST"])
def predict():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            "error": "JSON request body is required"
        }), 400

    try:
        result = predict_lead(data)

        return jsonify(result), 200

    except Exception as exc:
        return jsonify({
            "error": str(exc)
        }), 500