from flask import Blueprint, request, session
from database import Database
import json
from flask import Response

bp_admin_university_colleges = Blueprint('bp_admin_university_colleges',__name__)

@bp_admin_university_colleges.route('/ajax_admin_get_university_colleges', methods=['POST'])
def admin_get_university_colleges():
    
    button = request.form.get('button')

    if button != 'get_university_colleges':
        data = {
            'status': 'invalid_request',
            'message': 'Button not recognized'
        }
        return Response(json.dumps(data), mimetype='text/plain'), 200
    else:
        db = Database()
        query = "SELECT * FROM tbl_sucs"
        db.execute(query)
        raw_data = db.fetchall()
        
        if raw_data:
            db.close() 
            data = {
                'status': 'success',
                'message': 'Login successful',
                'raw_data': raw_data
            }
            return Response(json.dumps(data), mimetype='text/plain'), 200
        else:
            db.close() 
            data = {
                'status': 'no_data',
                'message': 'No university colleges found'
            }
            return Response(json.dumps(data), mimetype='text/plain'), 200
        
        
        