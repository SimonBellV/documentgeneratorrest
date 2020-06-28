from . import app
from flask import jsonify


@app.errorhandler(404)
def page_not_found(e):
    return jsonify({'message': 'Page not found!'}), 404


@app.errorhandler(405)
def page_not_found(e):
    return jsonify({'message': 'Method not allowed!'}), 405
