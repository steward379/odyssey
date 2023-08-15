# from flask import Flask, jsonify, request, make_response
from app import create_app

app = create_app()

# @app.route('/api/hello', methods=['GET'])
# def hello():
#     return jsonify(message="Hello from Flask!")

if __name__ == "__main__":
    app.run(debug=True, port=3000)
