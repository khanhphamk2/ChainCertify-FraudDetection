from flask import Blueprint, request, jsonify
import src.services.data as data

data_bp = Blueprint('data_eth', __name__)

@data_bp.route('/api/data', methods=['GET'])
def get_data():
    address = request.args.get('address')
    if not address:
        return jsonify({'error': 'Please provide an address'})

    stats = data.get_data(address)
    return jsonify(stats)