import re
from flask import Blueprint, request, jsonify

api_bp = Blueprint("api", __name__)

MAX_MESSAGE_LENGTH = 500

# Basic heuristic patterns for prompt injection & unauthorized actions
INJECTION_PATTERNS = [
    r"ignore\s+(all\s+)?previous\s+instructions",
    r"system\s+prompt",
    r"reveal\s+(your\s+)?(instructions|secrets|password|api\s*key)",
    r"execute\s+(shell|command|transfer|delete)",
    r"bypass\s+security",
]


def _contains_prompt_injection(text: str) -> bool:
    lowered = text.lower()
    return any(re.search(pattern, lowered) for pattern in INJECTION_PATTERNS)


def _sanitize_output(text: str) -> str:
    # Ensure no HTML/script tags or simulated secrets leak in output
    sanitized = re.sub(r"<[^>]*?>", "", text)
    return sanitized.strip()


def _generate_mock_ai_response(user_message: str) -> str:
    """
    Mock financial assistant response generator with guardrails.
    Note: Real LLM resistance requires model-level evaluation in addition to input/output filtering.
    """
    if _contains_prompt_injection(user_message):
        return (
            "I cannot process instructions that attempt to override system guidelines "
            "or access restricted information. How can I help you with personal finance?"
        )

    msg_lower = user_message.lower()
    if "budget" in msg_lower:
        raw_response = "You can start by tracking your monthly income and categorizing fixed vs. variable expenses."
    elif "save" in msg_lower or "saving" in msg_lower:
        raw_response = "Consider automating transfers to a high-yield savings account right after payday (50/30/20 rule)."
    elif "invest" in msg_lower:
        raw_response = "Diversified low-cost index funds are commonly used for long-term wealth building."
    else:
        raw_response = "I am Mini-VulnFinBot. Ask me about budgeting, saving, or general financial planning."

    return _sanitize_output(raw_response)


@api_bp.route("/", methods=["GET"])
def index():
    return jsonify({
        "service": "Mini-VulnFinBot",
        "version": "1.0.0",
        "endpoints": ["/health", "/api/chat"]
    }), 200


@api_bp.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "healthy"}), 200


@api_bp.route("/api/chat", methods=["POST"])
def chat():
    if not request.is_json:
        return jsonify({"error": "Content-Type must be application/json"}), 400

    data = request.get_json(silent=True)
    if data is None or not isinstance(data, dict):
        return jsonify({"error": "Invalid JSON payload"}), 400

    if "message" not in data:
        return jsonify({"error": "Missing required field: 'message'"}), 400

    message = data["message"]

    if not isinstance(message, str):
        return jsonify({"error": "Field 'message' must be a string"}), 400

    cleaned_message = message.strip()
    if not cleaned_message:
        return jsonify({"error": "Message cannot be empty"}), 400

    if len(cleaned_message) > MAX_MESSAGE_LENGTH:
        return jsonify({
            "error": f"Message exceeds maximum allowed length of {MAX_MESSAGE_LENGTH} characters"
        }), 400

    assistant_reply = _generate_mock_ai_response(cleaned_message)
    return jsonify({"response": assistant_reply}), 200

@bp.route("/debug-eval", methods=["POST"])
def debug_eval():
    return str(eval("2 + 2"))