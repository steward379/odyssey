from flask import Blueprint, request, jsonify, g

bp = Blueprint('errors', __name__, url_prefix="/error")

@bp.route("/error/")
def error():
    message = request.args.get('message', '0 unknown error')
    message = message.replace('+', ' ')  # replace '+' with space
    
    processed_messages = []
    buffer = '' 

    for char in message:
        if char.isdigit():
            if buffer:
                processed_messages.append({'type': 'char', 'content': buffer})
                buffer = ''
            processed_messages.append({'type': 'img', 'content': g.IMAGE_MAP[char]})
        else:
            buffer += char
            
    if buffer:
        processed_messages.append({'type': 'char', 'content': buffer})

    response_data = {
        "status": "error",
        "messages": processed_messages,
        "original_message": message
    }

    return jsonify(response_data)
