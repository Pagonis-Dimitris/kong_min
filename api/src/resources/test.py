from flask_restful import Resource
from flask import request


def response(success, payload, status): return {'success': success, 'payload': payload}, status

class RouteOne(Resource):
    @classmethod
    def post(cls):
        try:
            request_body = request.get_json()
            payload = {"inside":"one","body": request_body}
            return response(True, payload, 200)
        except Exception as e:
            print(e)
            return response(False, {'error', 500})

