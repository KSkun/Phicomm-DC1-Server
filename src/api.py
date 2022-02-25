from http import HTTPStatus

from flask import Blueprint, request, abort, jsonify

from server import devices

api_bp = Blueprint('api', __name__, url_prefix='/api')


@api_bp.route('/dev/list', methods=['GET'])
def http_list_device():
    dev_list = []
    for dev in devices.values():
        dev.update_status()
        dev_list.append(dev.to_dict())
    return jsonify(dev_list)


@api_bp.route('/dev', methods=['GET'])
def http_get_device():
    mac = request.args.get('mac')
    if mac not in devices.keys():
        abort(HTTPStatus.BAD_REQUEST)
    dev = devices[mac]
    dev.update_status()
    return jsonify(dev.to_dict())


@api_bp.route('/dev/status', methods=['PUT'])
def http_set_status():
    mac = request.args.get('mac')
    if mac not in devices.keys():
        abort(HTTPStatus.BAD_REQUEST)
    dev = devices[mac]
    body = request.get_json()
    dev.switch(tuple(body['status']))
    return jsonify(dev.to_dict())
