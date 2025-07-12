from flask import Blueprint, request, session
from database import Database
import json
from flask import Response

bp_admin_login = Blueprint('bp_admin_login',__name__)

@bp_admin_login.route('/ajax_admin_login', methods=['POST'])
def admin_login():
    
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
        query = "SELECT * FROM tbl_users WHERE user_email = %s AND user_pass = %s AND user_type = '99'"
        result = db.execute(query, (username, password)).fetchone()
        db.close()

        if result:
            session['USER_ID'] = result['user_id']
            session['USER_EMAIL'] = result['user_email']
            session['USER_PASS'] = result['user_pass']
            session['USER_TYPE'] = result['user_type']
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
        