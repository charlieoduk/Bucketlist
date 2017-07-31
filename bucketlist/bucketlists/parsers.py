from flask_restplus import reqparse

parser = reqparse.RequestParser()
parser.add_argument('q', type=str, required=False, location='args')
parser.add_argument('limit', type=int, required=False, default=20, help='Results per page', location='args')
parser.add_argument('page', type=int, default=1, help='Page number', required=False, location='args')