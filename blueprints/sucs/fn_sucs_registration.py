from flask import Blueprint, request, session
from database import Database
import json
from flask import Response

bp_sucs_registration = Blueprint('bp_sucs_registration',__name__)

@bp_sucs_registration.route('/ajax_sucs_registration', methods=['POST'])
def sucs_registration():
    
    button = request.form.get('button')
    sucname = request.form.get('sucname')
    typology = request.form.get('typology')
    region = request.form.get('region')
    address = request.form.get('address')
    email = request.form.get('email')
    password = request.form.get('password')

    if button != 'registration':
        data = {
            'status': 'invalid_request',
            'message': 'Button not recognized'
        }
        return Response(json.dumps(data), mimetype='text/plain'), 200
    else:
        db = Database()
        query = "INSERT INTO tbl_sucs (suc_name, suc_typology, suc_region, suc_address, suc_email, suc_logo) VALUES (%s, %s, %s, %s, %s, '')"
        params = (sucname,typology,region,address,email,)
        result = db.execute(query, params)
        
        if result:

            query = "INSERT INTO tbl_users (user_email,user_pass,user_type) VALUES (%s, %s, '0')"
            params = (email,password,)
            result = db.execute(query, params)

            db.close() 
            data = {
                'status': 'success',
                'message': 'Indicator deleted',
            }
            return Response(json.dumps(data), mimetype='text/plain'), 200
        else:
            db.close() 
            data = {
                'status': 'failed',
                'message': 'Failed to register SUC',
            }
            return Response(json.dumps(data), mimetype='text/plain'), 200
        