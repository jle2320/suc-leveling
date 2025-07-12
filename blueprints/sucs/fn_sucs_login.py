from flask import Blueprint, request, session
from database import Database
import json
from flask import Response

bp_sucs_login = Blueprint('bp_sucs_login',__name__)

@bp_sucs_login.route('/ajax_sucs_login', methods=['POST'])
def sucs_login():
    
    button = request.form.get('button')
    username = request.form.get('username')
    password = request.form.get('password')

    if button != 'login':
        data = {
            'status': 'invalid_request',
            'message': 'Button not recognized'
        }
        return Response(json.dumps(data), mimetype='text/plain'), 200
    else:
        db = Database()
        query = """
                SELECT 
                    u.user_id,
                    u.user_email,
                    u.user_pass,
                    u.user_type,
                    s.suc_id
                FROM 
                    tbl_users as u 
                JOIN 
                    tbl_sucs as s
                    ON u.user_email = s.suc_email
                WHERE u.user_email = %s AND u.user_pass = %s AND u.user_type = '0'
            """
        result = db.execute(query, (username, password)).fetchone()
        db.close()

        if result:
            session['USER_SUCS_ID'] = result['user_id']
            session['USER_SUCS_EMAIL'] = result['user_email']
            session['USER_SUCS_PASS'] = result['user_pass']
            session['USER_SUCS_TYPE'] = result['user_type']
            session['SUCS_ID'] = result['suc_id']
            data = {
                'status': 'success',
                'message': 'Login successful'
            }
            return Response(json.dumps(data), mimetype='text/plain'), 200
        else:
            data = {
                'status': 'incorrect_details',
                'message': 'Incorrect username or password'
            }
            return Response(json.dumps(data), mimetype='text/plain'), 200
        