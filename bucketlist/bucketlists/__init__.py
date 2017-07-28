from flask import Blueprint

bucketlists = Blueprint('bucketlists', __name__)

from . import views