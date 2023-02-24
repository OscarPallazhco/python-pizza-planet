from app.common.http_methods import GET
from flask import Blueprint, jsonify, request

from ..controllers import ReportController
from .base import *

report = Blueprint('report', __name__)


@report.route('/', methods=GET)
def get_report():
    return get_reports(ReportController)