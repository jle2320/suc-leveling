from flask import Blueprint, request
from database import Database
import json
from flask import Response
import pprint
bp_admin_results = Blueprint('bp_admin_results',__name__)

@bp_admin_results.route('/ajax_admin_get_results', methods=['POST'])
def admin_get_results():
    
    button = request.form.get('button')
    instrument_id = request.form.get('instrument_id')

    if button != 'get_results':
        data = {
            'status': 'invalid_request',
            'message': 'Button not recognized'
        }
        return Response(json.dumps(data), mimetype='text/plain'), 200
    else:
        db = Database()
        query = """
                SELECT 
                    SUM(point_value) as results,
                    sucs.suc_name,
                    sucs.suc_region,
                    sucs.suc_typology,
                    sucs.suc_logo
                FROM 
                	tbl_kra as kra
                JOIN
                	tbl_indicators_main as indi
                    ON kra.kra_id = indi.kra_id
                 JOIN
                    tbl_points_main as points
                    ON indi.indicator_id = points.indicator_id
                JOIN
                    tbl_sucs as sucs
                    ON points.suc_id = sucs.suc_id
                WHERE
                	kra.instrument_id = %s
                GROUP BY
                    sucs.suc_name
                ORDER BY 
                    results DESC;
                """
        db.execute(query, (instrument_id,))
        raw_result = db.fetchall()

        query = "SELECT * FROM tbl_criteria WHERE instrument_id=%s"
        param = (instrument_id,)
        db.execute(query,param)
        raw_criteria = db.fetchall()

        dataa = []

        if raw_result and raw_criteria:
            for rows in raw_result:
                resultPoint = rows['results']
                sucName = rows['suc_name']
                sucRegion = rows['suc_region']
                sucTypology = rows['suc_typology']
                sucLogo = rows['suc_logo']

                for criteria in raw_criteria:
                    levelName = criteria['criteria_level']
                    minPoint = criteria['criteria_minpoint']
                    maxPoint = criteria['criteria_maxpoint']
                
                    if float(minPoint) <= float(resultPoint) <= float(maxPoint):
                        dataa.append({
                            'sucName': sucName,
                            'sucRegion': sucRegion,
                            'sucTypology': sucTypology,
                            'sucLogo': sucLogo,
                            'levelName': levelName,
                            'resultPoint': resultPoint
                        })


            db.close() 
            data = {
                'status': 'success',
                'message': 'list',
                'raw_data': dataa
            }
            return Response(json.dumps(data), mimetype='text/plain'), 200
        else:
            db.close() 
            data = {
                'status': 'no_data',
                'message': 'No data'
            }
            return Response(json.dumps(data), mimetype='text/plain'), 200
        
