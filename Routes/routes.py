from flask import Blueprint, jsonify
from APIFile.linkin_automation_request import connect_on_linkin
from APIFile.contact_detail_store import submit_linkin_contact_data
linkin_automation_bp = Blueprint("linkin_automation", __name__)


#Send the connection request 

@linkin_automation_bp.route("/linkedin/connect", methods=["POST"])
def connect_on_linkin_api():
    return connect_on_linkin()


@linkin_automation_bp.route("/linkedin_contact_detail", methods=["POST"])
def submit_linkin_contact_data_api():
    return submit_linkin_contact_data()