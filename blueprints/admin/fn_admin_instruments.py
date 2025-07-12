from flask import Blueprint, request
from database import Database
import json
from flask import Response
import pprint
bp_admin_instruments = Blueprint('bp_admin_instruments',__name__)

@bp_admin_instruments.route('/ajax_admin_get_instruments', methods=['POST'])
def admin_get_instruments():
    
    button = request.form.get('button')

    if button != 'get_instruments':
        data = {
            'status': 'invalid_request',
            'message': 'Button not recognized'
        }
        return Response(json.dumps(data), mimetype='text/plain'), 200
    else:
        db = Database()
        query = "SELECT * FROM tbl_instruments"
        db.execute(query)
        raw_data = db.fetchall()
        
        if raw_data:
            db.close() 
            data = {
                'status': 'success',
                'message': 'list',
                'raw_data': raw_data
            }
            return Response(json.dumps(data), mimetype='text/plain'), 200
        else:
            db.close() 
            data = {
                'status': 'no_data',
                'message': 'No instruments found'
            }
            return Response(json.dumps(data), mimetype='text/plain'), 200
        


@bp_admin_instruments.route('/ajax_admin_get_level_points', methods=['POST'])
def admin_get_level_points():
    
    button = request.form.get('button')
    instrument_id = request.form.get('instrument_id')

    if button != 'get_level_points':
        data = {
            'status': 'invalid_request',
            'message': 'Button not recognized'
        }
        return Response(json.dumps(data), mimetype='text/plain'), 200
    else:
        db = Database()
        query = "SELECT * FROM tbl_criteria WHERE instrument_id=%s"
        params = (instrument_id,)
        db.execute(query, params,)
        raw_data = db.fetchall()
        
        if raw_data:
            db.close() 
            data = {
                'status': 'success',
                'message': 'list',
                'raw_data': raw_data
            }
            return Response(json.dumps(data), mimetype='text/plain'), 200
        else:
            db.close() 
            data = {
                'status': 'no_data',
                'message': 'No level found'
            }
            return Response(json.dumps(data), mimetype='text/plain'), 200
        



@bp_admin_instruments.route('/ajax_admin_save_instrument', methods=['POST'])
def admin_save_instrument():
    
    button = request.form.get('button')
    input_jc = request.form.get('input_jc')
    input_subject = request.form.get('input_subject')

    if button != 'save_instrument':
        data = {
            'status': 'invalid_request',
            'message': 'Button not recognized'
        }
        return Response(json.dumps(data), mimetype='text/plain'), 200
    else:
        db = Database()
        query = "INSERT INTO tbl_instruments (instrument_jc, instrument_subject,instrument_status) VALUES (%s, %s,'draft')"
        params = (input_jc, input_subject)
        result = db.execute(query, params)
        last_id = result.lastrowid if result else None

        if result:
            query = """
                    INSERT INTO tbl_criteria (instrument_id,criteria_level,criteria_minpoint,criteria_maxpoint) VALUE
                    (%s,'Level I',0,0),
                    (%s,'Level II',0,0),
                    (%s,'Level III',0,0),
                    (%s,'Level IV',0,0),
                    (%s,'Level V',0,0)
                """
            params = (last_id,last_id,last_id,last_id,last_id,)
            db.execute(query, params)

            db.close() 
            data = {
                'status': 'success',
                'message': 'saved',
            }
            return Response(json.dumps(data), mimetype='text/plain'), 200
        else:
            db.close() 
            data = {
                'status': 'failed',
                'message': 'Failed to save instrument',
            }
            return Response(json.dumps(data), mimetype='text/plain'), 200
        

        
@bp_admin_instruments.route('/ajax_admin_save_point_level', methods=['POST'])
def admin_save_point_level():
    
    button = request.form.get('button')
    criteriaId = request.form.get('criteriaId')
    minVal = request.form.get('minVal')
    maxVal = request.form.get('maxVal')

    if button != 'save_point_level':
        data = {
            'status': 'invalid_request',
            'message': 'Button not recognized'
        }
        return Response(json.dumps(data), mimetype='text/plain'), 200
    else:
        db = Database()
        query = "UPDATE tbl_criteria SET criteria_minpoint=%s, criteria_maxpoint=%s WHERE criteria_id=%s "
        params = (minVal,maxVal,criteriaId,)
        result = db.execute(query, params)
        
        if result:
            db.close() 
            data = {
                'status': 'success',
                'message': 'saved',
            }
            return Response(json.dumps(data), mimetype='text/plain'), 200
        else:
            db.close() 
            data = {
                'status': 'failed',
                'message': 'Failed to save point',
            }
            return Response(json.dumps(data), mimetype='text/plain'), 200
        

@bp_admin_instruments.route('/ajax_admin_delete_instrument', methods=['POST'])
def admin_delete_instrument():
    
    button = request.form.get('button')
    instrument_id = request.form.get('instrument_id')

    if button != 'delete_instrument':
        data = {
            'status': 'invalid_request',
            'message': 'Button not recognized'
        }
        return Response(json.dumps(data), mimetype='text/plain'), 200
    else:
        db = Database()
        query = "DELETE FROM tbl_instruments WHERE instrument_id=%s"
        params = (instrument_id,)
        result = db.execute(query, params)
        
        if result:
            db.close() 
            data = {
                'status': 'success',
                'message': 'deleted',
            }
            return Response(json.dumps(data), mimetype='text/plain'), 200
        else:
            db.close() 
            data = {
                'status': 'failed',
                'message': 'Failed to delete instrument',
            }
            return Response(json.dumps(data), mimetype='text/plain'), 200
        


@bp_admin_instruments.route('/ajax_admin_publish_instrument', methods=['POST'])
def admin_publish_instrument():
    
    button = request.form.get('button')
    instrument_id = request.form.get('instrument_id')

    if button != 'publish_instrument':
        data = {
            'status': 'invalid_request',
            'message': 'Button not recognized'
        }
        return Response(json.dumps(data), mimetype='text/plain'), 200
    else:
        db = Database()
        query = "UPDATE tbl_instruments SET instrument_status='Published' WHERE instrument_id=%s"
        params = (instrument_id,)
        result = db.execute(query, params)
        
        if result:
            db.close() 
            data = {
                'status': 'success',
                'message': 'published',
            }
            return Response(json.dumps(data), mimetype='text/plain'), 200
        else:
            db.close() 
            data = {
                'status': 'failed',
                'message': 'Failed to publish instrument',
            }
            return Response(json.dumps(data), mimetype='text/plain'), 200
        


        


@bp_admin_instruments.route('/ajax_admin_add_instrument_kra', methods=['POST'])
def admin_add_instrument_kra():
    
    button = request.form.get('button')
    instrument_id = request.form.get('instrument_id')

    if button != 'add_instrument_kra':
        data = {
            'status': 'invalid_request',
            'message': 'Button not recognized'
        }
        return Response(json.dumps(data), mimetype='text/plain'), 200
    else:
        db = Database()
        query = "INSERT INTO tbl_kra (instrument_id, kra_name,kra_point) VALUES (%s,'KRA Name...','0')"
        params = (instrument_id,)
        result = db.execute(query, params)
        
        if result:
            db.close() 
            data = {
                'status': 'success',
                'message': 'KRA added',
            }
            return Response(json.dumps(data), mimetype='text/plain'), 200
        else:
            db.close() 
            data = {
                'status': 'failed',
                'message': 'Failed to publish instrument',
            }
            return Response(json.dumps(data), mimetype='text/plain'), 200





@bp_admin_instruments.route('/ajax_admin_delete_instrument_kra', methods=['POST'])
def admin_delete_instrument_kra():
    
    button = request.form.get('button')
    kraID = request.form.get('kraID')

    if button != 'delete_instrument_kra':
        data = {
            'status': 'invalid_request',
            'message': 'Button not recognized'
        }
        return Response(json.dumps(data), mimetype='text/plain'), 200
    else:
        db = Database()
        query = "DELETE FROM tbl_kra WHERE kra_id=%s"
        params = (kraID,)
        result = db.execute(query, params)
        
        if result:
            db.close() 
            data = {
                'status': 'success',
                'message': 'KRA deleted',
            }
            return Response(json.dumps(data), mimetype='text/plain'), 200
        else:
            db.close() 
            data = {
                'status': 'failed',
                'message': 'Failed to delete KRA',
            }
            return Response(json.dumps(data), mimetype='text/plain'), 200
        




@bp_admin_instruments.route('/ajax_admin_update_kra_name', methods=['POST'])
def admin_update_kra_name():
    
    button = request.form.get('button')
    kraID = request.form.get('kraID')
    kraName = request.form.get('kraName')

    if button != 'update_kra_name':
        data = {
            'status': 'invalid_request',
            'message': 'Button not recognized'
        }
        return Response(json.dumps(data), mimetype='text/plain'), 200
    else:
        db = Database()
        query = "UPDATE tbl_kra SET kra_name=%s WHERE kra_id=%s"
        params = (kraName,kraID,)
        result = db.execute(query, params)
        
        if result:
            db.close() 
            data = {
                'status': 'success',
                'message': 'KRA name saved',
            }
            return Response(json.dumps(data), mimetype='text/plain'), 200
        else:
            db.close() 
            data = {
                'status': 'failed',
                'message': 'Failed to save KRA name',
            }
            return Response(json.dumps(data), mimetype='text/plain'), 200
        




@bp_admin_instruments.route('/ajax_admin_update_kra_point', methods=['POST'])
def admin_update_kra_point():
    
    button = request.form.get('button')
    kraID = request.form.get('kraID')
    kraPoint = request.form.get('kraPoint')

    if button != 'update_kra_point':
        data = {
            'status': 'invalid_request',
            'message': 'Button not recognized'
        }
        return Response(json.dumps(data), mimetype='text/plain'), 200
    else:
        db = Database()
        query = "UPDATE tbl_kra SET kra_point=%s WHERE kra_id=%s"
        params = (kraPoint,kraID,)
        result = db.execute(query, params)
        
        if result:
            db.close() 
            data = {
                'status': 'success',
                'message': 'KRA point saved',
            }
            return Response(json.dumps(data), mimetype='text/plain'), 200
        else:
            db.close() 
            data = {
                'status': 'failed',
                'message': 'Failed to save KRA point',
            }
            return Response(json.dumps(data), mimetype='text/plain'), 200
        





@bp_admin_instruments.route('/ajax_admin_get_instrument_kra', methods=['POST'])
def admin_get_instrument_kra():
    
    button = request.form.get('button')
    instrument_id = request.form.get('instrument_id')

    if button != 'get_instrument_kra':
        data = {
            'status': 'invalid_request',
            'message': 'Button not recognized'
        }
        return Response(json.dumps(data), mimetype='text/plain'), 200
    else:
        db = Database()
        query = """
            SELECT 
                kra.kra_id, 
                kra.kra_name, 
                kra.kra_point, 
                indicator_main.indicator_id as main_indicator_id, 
                indicator_main.indicator_name as main_indicator_name, 
                indicator_main.indicator_point as main_indicator_point, 
                indicator_main.indicator_type as main_indicator_type,
                firstsub.indicator_id as firstsub_indicator_id,
                firstsub.indicator_name as firstsub_indicator_name,
                firstsub.indicator_point as firstsub_indicator_point,
                firstsub.indicator_type as firstsub_indicator_type,
                secondsub.indicator_id as secondsub_indicator_id,
                secondsub.indicator_name as secondsub_indicator_name,
                secondsub.indicator_point as secondsub_indicator_point,
                secondsub.indicator_type as secondsub_indicator_type,
                thirdsub.indicator_id as thirdsub_indicator_id,
                thirdsub.indicator_name as thirdsub_indicator_name,
                thirdsub.indicator_point as thirdsub_indicator_point,
                thirdsub.indicator_type as thirdsub_indicator_type,
                fourthsub.indicator_id as fourthsub_indicator_id,
                fourthsub.indicator_name as fourthsub_indicator_name,
                fourthsub.indicator_point as fourthsub_indicator_point,
                fourthsub.indicator_type as fourthsub_indicator_type
            FROM 
                tbl_kra as kra 
            LEFT JOIN tbl_indicators_main as indicator_main 
                ON kra.kra_id = indicator_main.kra_id
            LEFT JOIN tbl_indicators_firstsub as firstsub
                ON indicator_main.indicator_id = firstsub.prime_indicator_id
            LEFT JOIN tbl_indicators_secondsub as secondsub
                ON firstsub.indicator_id = secondsub.indicator_firstsub_id
            LEFT JOIN tbl_indicators_thirdsub as thirdsub
                ON secondsub.indicator_id = thirdsub.indicator_secondsub_id
            LEFT JOIN tbl_indicators_fourthsub as fourthsub
                ON thirdsub.indicator_id = fourthsub.indicator_thirdsub_id
            WHERE kra.instrument_id = %s
            ORDER BY kra.kra_id,
                     indicator_main.indicator_id,
                     firstsub.indicator_id,
                     secondsub.indicator_id,
                     thirdsub.indicator_id,
                     fourthsub.indicator_id;
        """
        params = (instrument_id,)
        db.execute(query, params)
        raw_data = db.fetchall()

        if raw_data:
            db.close()

            merged = {}

            for entry in raw_data:
                kra_id = entry["kra_id"]

                if kra_id not in merged:
                    merged[kra_id] = {
                        "kra_id": kra_id,
                        "kra_name": entry["kra_name"],
                        "kra_point": entry["kra_point"],
                        "main_indicators": []
                    }

                current_main = None
                if entry["main_indicator_id"] is not None:
                    existing_main = next(
                        (mi for mi in merged[kra_id]["main_indicators"]
                        if mi["main_indicator_id"] == entry["main_indicator_id"]), None)

                    if not existing_main:
                        current_main = {
                            "main_indicator_id": entry["main_indicator_id"],
                            "main_indicator_name": entry["main_indicator_name"],
                            "main_indicator_point": entry["main_indicator_point"],
                            "main_indicator_type": entry["main_indicator_type"],
                            "firstsub_indicators": []
                        }
                        merged[kra_id]["main_indicators"].append(current_main)
                    else:
                        current_main = existing_main

                current_firstsub = None
                if entry["firstsub_indicator_id"] is not None and current_main is not None:
                    existing_firstsub = next(
                        (fs for fs in current_main["firstsub_indicators"]
                        if fs["firstsub_indicator_id"] == entry["firstsub_indicator_id"]), None)

                    if not existing_firstsub:
                        current_firstsub = {
                            "firstsub_indicator_id": entry["firstsub_indicator_id"],
                            "firstsub_indicator_name": entry["firstsub_indicator_name"],
                            "firstsub_indicator_point": entry["firstsub_indicator_point"],
                            "firstsub_indicator_type": entry["firstsub_indicator_type"],
                            "secondsub_indicators": []
                        }
                        current_main["firstsub_indicators"].append(current_firstsub)
                    else:
                        current_firstsub = existing_firstsub

                current_secondsub = None
                if entry["secondsub_indicator_id"] is not None and current_firstsub is not None:
                    existing_secondsub = next(
                        (ss for ss in current_firstsub["secondsub_indicators"]
                        if ss["secondsub_indicator_id"] == entry["secondsub_indicator_id"]), None)

                    if not existing_secondsub:
                        current_secondsub = {
                            "secondsub_indicator_id": entry["secondsub_indicator_id"],
                            "secondsub_indicator_name": entry["secondsub_indicator_name"],
                            "secondsub_indicator_point": entry["secondsub_indicator_point"],
                            "secondsub_indicator_type": entry["secondsub_indicator_type"],
                            "thirdsub_indicators": []
                        }
                        current_firstsub["secondsub_indicators"].append(current_secondsub)
                    else:
                        current_secondsub = existing_secondsub

                current_thirdsub = None
                if entry["thirdsub_indicator_id"] is not None and current_secondsub is not None:
                    existing_thirdsub = next(
                        (ts for ts in current_secondsub["thirdsub_indicators"]
                        if ts["thirdsub_indicator_id"] == entry["thirdsub_indicator_id"]), None)

                    if not existing_thirdsub:
                        current_thirdsub = {
                            "thirdsub_indicator_id": entry["thirdsub_indicator_id"],
                            "thirdsub_indicator_name": entry["thirdsub_indicator_name"],
                            "thirdsub_indicator_point": entry["thirdsub_indicator_point"],
                            "thirdsub_indicator_type": entry["thirdsub_indicator_type"],
                            "fourthsub_indicators": []
                        }
                        current_secondsub["thirdsub_indicators"].append(current_thirdsub)
                    else:
                        current_thirdsub = existing_thirdsub

                if entry["fourthsub_indicator_id"] is not None and current_thirdsub is not None:
                    existing_fourthsub = next(
                        (fs for fs in current_thirdsub["fourthsub_indicators"]
                        if fs["fourthsub_indicator_id"] == entry["fourthsub_indicator_id"]), None)

                    if not existing_fourthsub:
                        current_thirdsub["fourthsub_indicators"].append({
                            "fourthsub_indicator_id": entry["fourthsub_indicator_id"],
                            "fourthsub_indicator_name": entry["fourthsub_indicator_name"],
                            "fourthsub_indicator_point": entry["fourthsub_indicator_point"],
                            "fourthsub_indicator_type": entry["fourthsub_indicator_type"]
                        })






            result = list(merged.values())
            data = {
                'status': 'success',
                'message': 'list',
                'raw_data': result
            }
            return Response(json.dumps(data), mimetype='text/plain'), 200
        else:
            db.close() 
            data = {
                'status': 'no_data',
                'message': 'No KRA found'
            }
            return Response(json.dumps(data), mimetype='text/plain'), 200
        




@bp_admin_instruments.route('/ajax_admin_add_prime_indicator', methods=['POST'])
def admin_add_prime_indicator():
    
    button = request.form.get('button')
    textIndicator = request.form.get('textIndicator')
    indicatorID = request.form.get('indicatorID')

    if button != 'add_prime_indicator':
        data = {
            'status': 'invalid_request',
            'message': 'Button not recognized'
        }
        return Response(json.dumps(data), mimetype='text/plain'), 200
    else:
        db = Database()
        query = "INSERT INTO tbl_indicators_main (kra_id,indicator_name,indicator_point,indicator_type) VALUES (%s,'Indicator Name...','0',%s)"
        params = (indicatorID,textIndicator,)
        result = db.execute(query, params)
        
        if result:
            db.close() 
            data = {
                'status': 'success',
                'message': 'Indicator added',
            }
            return Response(json.dumps(data), mimetype='text/plain'), 200
        else:
            db.close() 
            data = {
                'status': 'failed',
                'message': 'Failed to add indicator',
            }
            return Response(json.dumps(data), mimetype='text/plain'), 200
        



@bp_admin_instruments.route('/ajax_admin_add_firstsub_indicator', methods=['POST'])
def admin_add_firstsub_indicator():
    
    button = request.form.get('button')
    textIndicator = request.form.get('textIndicator')
    indicatorID = request.form.get('indicatorID')

    if button != 'add_firstsub_indicator':
        data = {
            'status': 'invalid_request',
            'message': 'Button not recognized'
        }
        return Response(json.dumps(data), mimetype='text/plain'), 200
    else:
        db = Database()
        query = "INSERT INTO tbl_indicators_firstsub (prime_indicator_id,indicator_name,indicator_point,indicator_type) VALUES (%s,'Indicator Name...','0',%s)"
        params = (indicatorID,textIndicator,)
        result = db.execute(query, params)
        
        if result:
            db.close() 
            data = {
                'status': 'success',
                'message': 'Indicator added',
            }
            return Response(json.dumps(data), mimetype='text/plain'), 200
        else:
            db.close() 
            data = {
                'status': 'failed',
                'message': 'Failed to add indicator',
            }
            return Response(json.dumps(data), mimetype='text/plain'), 200
        



@bp_admin_instruments.route('/ajax_admin_add_secondsub_indicator', methods=['POST'])
def admin_add_secondsub_indicator():
    
    button = request.form.get('button')
    textIndicator = request.form.get('textIndicator')
    indicatorID = request.form.get('indicatorID')

    if button != 'add_secondsub_indicator':
        data = {
            'status': 'invalid_request',
            'message': 'Button not recognized'
        }
        return Response(json.dumps(data), mimetype='text/plain'), 200
    else:
        db = Database()
        query = "INSERT INTO tbl_indicators_secondsub (indicator_firstsub_id,indicator_name,indicator_point,indicator_type) VALUES (%s,'Indicator Name...','0',%s)"
        params = (indicatorID,textIndicator,)
        result = db.execute(query, params)
        
        if result:
            db.close() 
            data = {
                'status': 'success',
                'message': 'Indicator added',
            }
            return Response(json.dumps(data), mimetype='text/plain'), 200
        else:
            db.close() 
            data = {
                'status': 'failed',
                'message': 'Failed to add indicator',
            }
            return Response(json.dumps(data), mimetype='text/plain'), 200
        



@bp_admin_instruments.route('/ajax_admin_add_thirdsub_indicator', methods=['POST'])
def admin_add_thirdsub_indicator():
    
    button = request.form.get('button')
    textIndicator = request.form.get('textIndicator')
    indicatorID = request.form.get('indicatorID')

    if button != 'add_thirdsub_indicator':
        data = {
            'status': 'invalid_request',
            'message': 'Button not recognized'
        }
        return Response(json.dumps(data), mimetype='text/plain'), 200
    else:
        db = Database()
        query = "INSERT INTO tbl_indicators_thirdsub (indicator_secondsub_id,indicator_name,indicator_point,indicator_type) VALUES (%s,'Indicator Name...','0',%s)"
        params = (indicatorID,textIndicator,)
        result = db.execute(query, params)
        
        if result:
            db.close() 
            data = {
                'status': 'success',
                'message': 'Indicator added',
            }
            return Response(json.dumps(data), mimetype='text/plain'), 200
        else:
            db.close() 
            data = {
                'status': 'failed',
                'message': 'Failed to add indicator',
            }
            return Response(json.dumps(data), mimetype='text/plain'), 200
        
        



@bp_admin_instruments.route('/ajax_admin_add_fourthsub_indicator', methods=['POST'])
def admin_add_fourthsub_indicator():
    
    button = request.form.get('button')
    textIndicator = request.form.get('textIndicator')
    indicatorID = request.form.get('indicatorID')

    if button != 'add_fourthsub_indicator':
        data = {
            'status': 'invalid_request',
            'message': 'Button not recognized'
        }
        return Response(json.dumps(data), mimetype='text/plain'), 200
    else:
        db = Database()
        query = "INSERT INTO tbl_indicators_fourthsub (indicator_thirdsub_id,indicator_name,indicator_point,indicator_type) VALUES (%s,'Indicator Name...','0',%s)"
        params = (indicatorID,textIndicator,)
        result = db.execute(query, params)
        
        if result:
            db.close() 
            data = {
                'status': 'success',
                'message': 'Indicator added',
            }
            return Response(json.dumps(data), mimetype='text/plain'), 200
        else:
            db.close() 
            data = {
                'status': 'failed',
                'message': 'Failed to add indicator',
            }
            return Response(json.dumps(data), mimetype='text/plain'), 200
        


















        
        



@bp_admin_instruments.route('/ajax_admin_update_prime_indicator_name', methods=['POST'])
def admin_update_prime_indicator_name():
    
    button = request.form.get('button')
    indicatorID = request.form.get('indicatorID')
    indicatorName = request.form.get('indicatorName')

    if button != 'update_prime_indicator_name':
        data = {
            'status': 'invalid_request',
            'message': 'Button not recognized'
        }
        return Response(json.dumps(data), mimetype='text/plain'), 200
    else:
        db = Database()
        query = "UPDATE tbl_indicators_main SET indicator_name=%s WHERE indicator_id=%s"
        params = (indicatorName,indicatorID,)
        result = db.execute(query, params)
        
        if result:
            db.close() 
            data = {
                'status': 'success',
                'message': 'Indicator name saved',
            }
            return Response(json.dumps(data), mimetype='text/plain'), 200
        else:
            db.close() 
            data = {
                'status': 'failed',
                'message': 'Failed to save indicator name',
            }
            return Response(json.dumps(data), mimetype='text/plain'), 200
        

@bp_admin_instruments.route('/ajax_admin_update_first_indicator_name', methods=['POST'])
def admin_update_first_indicator_name():
    
    button = request.form.get('button')
    indicatorID = request.form.get('indicatorID')
    indicatorName = request.form.get('indicatorName')

    if button != 'update_first_indicator_name':
        data = {
            'status': 'invalid_request',
            'message': 'Button not recognized'
        }
        return Response(json.dumps(data), mimetype='text/plain'), 200
    else:
        db = Database()
        query = "UPDATE tbl_indicators_firstsub SET indicator_name=%s WHERE indicator_id=%s"
        params = (indicatorName,indicatorID,)
        result = db.execute(query, params)
        
        if result:
            db.close() 
            data = {
                'status': 'success',
                'message': 'Indicator name saved',
            }
            return Response(json.dumps(data), mimetype='text/plain'), 200
        else:
            db.close() 
            data = {
                'status': 'failed',
                'message': 'Failed to save indicator name',
            }
            return Response(json.dumps(data), mimetype='text/plain'), 200
        


@bp_admin_instruments.route('/ajax_admin_update_second_indicator_name', methods=['POST'])
def admin_update_second_indicator_name():
    
    button = request.form.get('button')
    indicatorID = request.form.get('indicatorID')
    indicatorName = request.form.get('indicatorName')

    if button != 'update_second_indicator_name':
        data = {
            'status': 'invalid_request',
            'message': 'Button not recognized'
        }
        return Response(json.dumps(data), mimetype='text/plain'), 200
    else:
        db = Database()
        query = "UPDATE tbl_indicators_secondsub SET indicator_name=%s WHERE indicator_id=%s"
        params = (indicatorName,indicatorID,)
        result = db.execute(query, params)
        
        if result:
            db.close() 
            data = {
                'status': 'success',
                'message': 'Indicator name saved',
            }
            return Response(json.dumps(data), mimetype='text/plain'), 200
        else:
            db.close() 
            data = {
                'status': 'failed',
                'message': 'Failed to save indicator name',
            }
            return Response(json.dumps(data), mimetype='text/plain'), 200
        


@bp_admin_instruments.route('/ajax_admin_update_third_indicator_name', methods=['POST'])
def admin_update_third_indicator_name():
    
    button = request.form.get('button')
    indicatorID = request.form.get('indicatorID')
    indicatorName = request.form.get('indicatorName')

    if button != 'update_third_indicator_name':
        data = {
            'status': 'invalid_request',
            'message': 'Button not recognized'
        }
        return Response(json.dumps(data), mimetype='text/plain'), 200
    else:
        db = Database()
        query = "UPDATE tbl_indicators_thirdsub SET indicator_name=%s WHERE indicator_id=%s"
        params = (indicatorName,indicatorID,)
        result = db.execute(query, params)
        
        if result:
            db.close() 
            data = {
                'status': 'success',
                'message': 'Indicator name saved',
            }
            return Response(json.dumps(data), mimetype='text/plain'), 200
        else:
            db.close() 
            data = {
                'status': 'failed',
                'message': 'Failed to save indicator name',
            }
            return Response(json.dumps(data), mimetype='text/plain'), 200
        


@bp_admin_instruments.route('/ajax_admin_update_fourth_indicator_name', methods=['POST'])
def admin_update_fourth_indicator_name():
    
    button = request.form.get('button')
    indicatorID = request.form.get('indicatorID')
    indicatorName = request.form.get('indicatorName')

    if button != 'update_fourth_indicator_name':
        data = {
            'status': 'invalid_request',
            'message': 'Button not recognized'
        }
        return Response(json.dumps(data), mimetype='text/plain'), 200
    else:
        db = Database()
        query = "UPDATE tbl_indicators_fourthsub SET indicator_name=%s WHERE indicator_id=%s"
        params = (indicatorName,indicatorID,)
        result = db.execute(query, params)
        
        if result:
            db.close() 
            data = {
                'status': 'success',
                'message': 'Indicator name saved',
            }
            return Response(json.dumps(data), mimetype='text/plain'), 200
        else:
            db.close() 
            data = {
                'status': 'failed',
                'message': 'Failed to save indicator name',
            }
            return Response(json.dumps(data), mimetype='text/plain'), 200
        


















        
        



@bp_admin_instruments.route('/ajax_admin_update_prime_indicator_point', methods=['POST'])
def admin_update_prime_indicator_point():
    
    button = request.form.get('button')
    indicatorID = request.form.get('indicatorID')
    indicatorPoint = request.form.get('indicatorPoint')

    if button != 'update_prime_indicator_point':
        data = {
            'status': 'invalid_request',
            'message': 'Button not recognized'
        }
        return Response(json.dumps(data), mimetype='text/plain'), 200
    else:
        db = Database()
        query = "UPDATE tbl_indicators_main SET indicator_point=%s WHERE indicator_id=%s"
        params = (indicatorPoint,indicatorID,)
        result = db.execute(query, params)
        
        if result:
            db.close() 
            data = {
                'status': 'success',
                'message': 'Indicator point saved',
            }
            return Response(json.dumps(data), mimetype='text/plain'), 200
        else:
            db.close() 
            data = {
                'status': 'failed',
                'message': 'Failed to save indicator point',
            }
            return Response(json.dumps(data), mimetype='text/plain'), 200
        

@bp_admin_instruments.route('/ajax_admin_update_first_indicator_point', methods=['POST'])
def admin_update_first_indicator_point():
    
    button = request.form.get('button')
    indicatorID = request.form.get('indicatorID')
    indicatorPoint = request.form.get('indicatorPoint')

    if button != 'update_first_indicator_point':
        data = {
            'status': 'invalid_request',
            'message': 'Button not recognized'
        }
        return Response(json.dumps(data), mimetype='text/plain'), 200
    else:
        db = Database()
        query = "UPDATE tbl_indicators_firstsub SET indicator_point=%s WHERE indicator_id=%s"
        params = (indicatorPoint,indicatorID,)
        result = db.execute(query, params)
        
        if result:
            db.close() 
            data = {
                'status': 'success',
                'message': 'Indicator point saved',
            }
            return Response(json.dumps(data), mimetype='text/plain'), 200
        else:
            db.close() 
            data = {
                'status': 'failed',
                'message': 'Failed to save indicator point',
            }
            return Response(json.dumps(data), mimetype='text/plain'), 200
        


@bp_admin_instruments.route('/ajax_admin_update_second_indicator_point', methods=['POST'])
def admin_update_second_indicator_point():
    
    button = request.form.get('button')
    indicatorID = request.form.get('indicatorID')
    indicatorPoint = request.form.get('indicatorPoint')

    if button != 'update_second_indicator_point':
        data = {
            'status': 'invalid_request',
            'message': 'Button not recognized'
        }
        return Response(json.dumps(data), mimetype='text/plain'), 200
    else:
        db = Database()
        query = "UPDATE tbl_indicators_secondsub SET indicator_point=%s WHERE indicator_id=%s"
        params = (indicatorPoint,indicatorID,)
        result = db.execute(query, params)
        
        if result:
            db.close() 
            data = {
                'status': 'success',
                'message': 'Indicator point saved',
            }
            return Response(json.dumps(data), mimetype='text/plain'), 200
        else:
            db.close() 
            data = {
                'status': 'failed',
                'message': 'Failed to save indicator point',
            }
            return Response(json.dumps(data), mimetype='text/plain'), 200
        


@bp_admin_instruments.route('/ajax_admin_update_third_indicator_point', methods=['POST'])
def admin_update_third_indicator_point():
    
    button = request.form.get('button')
    indicatorID = request.form.get('indicatorID')
    indicatorPoint = request.form.get('indicatorPoint')

    if button != 'update_third_indicator_point':
        data = {
            'status': 'invalid_request',
            'message': 'Button not recognized'
        }
        return Response(json.dumps(data), mimetype='text/plain'), 200
    else:
        db = Database()
        query = "UPDATE tbl_indicators_thirdsub SET indicator_point=%s WHERE indicator_id=%s"
        params = (indicatorPoint,indicatorID,)
        result = db.execute(query, params)
        
        if result:
            db.close() 
            data = {
                'status': 'success',
                'message': 'Indicator point saved',
            }
            return Response(json.dumps(data), mimetype='text/plain'), 200
        else:
            db.close() 
            data = {
                'status': 'failed',
                'message': 'Failed to save indicator point',
            }
            return Response(json.dumps(data), mimetype='text/plain'), 200
        


@bp_admin_instruments.route('/ajax_admin_update_fourth_indicator_point', methods=['POST'])
def admin_update_fourth_indicator_point():
    
    button = request.form.get('button')
    indicatorID = request.form.get('indicatorID')
    indicatorPoint = request.form.get('indicatorPoint')

    if button != 'update_fourth_indicator_point':
        data = {
            'status': 'invalid_request',
            'message': 'Button not recognized'
        }
        return Response(json.dumps(data), mimetype='text/plain'), 200
    else:
        db = Database()
        query = "UPDATE tbl_indicators_fourthsub SET indicator_point=%s WHERE indicator_id=%s"
        params = (indicatorPoint,indicatorID,)
        result = db.execute(query, params)
        
        if result:
            db.close() 
            data = {
                'status': 'success',
                'message': 'Indicator point saved',
            }
            return Response(json.dumps(data), mimetype='text/plain'), 200
        else:
            db.close() 
            data = {
                'status': 'failed',
                'message': 'Failed to save indicator point',
            }
            return Response(json.dumps(data), mimetype='text/plain'), 200
        


















        

@bp_admin_instruments.route('/ajax_admin_delete_prime_indicator', methods=['POST'])
def admin_delete_prime_indicator_point():
    
    button = request.form.get('button')
    indicatorID = request.form.get('indicatorID')

    if button != 'delete_prime_indicator':
        data = {
            'status': 'invalid_request',
            'message': 'Button not recognized'
        }
        return Response(json.dumps(data), mimetype='text/plain'), 200
    else:
        db = Database()
        query = "DELETE FROM  tbl_indicators_main WHERE indicator_id=%s"
        params = (indicatorID,)
        result = db.execute(query, params)
        
        if result:
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
                'message': 'Failed to delete indicator',
            }
            return Response(json.dumps(data), mimetype='text/plain'), 200
        

@bp_admin_instruments.route('/ajax_admin_delete_firstsub_indicator', methods=['POST'])
def admin_delete_firstsub_indicator():
    
    button = request.form.get('button')
    indicatorID = request.form.get('indicatorID')

    if button != 'delete_firstsub_indicator':
        data = {
            'status': 'invalid_request',
            'message': 'Button not recognized'
        }
        return Response(json.dumps(data), mimetype='text/plain'), 200
    else:
        db = Database()
        query = "DELETE FROM  tbl_indicators_firstsub WHERE indicator_id=%s"
        params = (indicatorID,)
        result = db.execute(query, params)
        
        if result:
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
                'message': 'Failed to delete indicator',
            }
            return Response(json.dumps(data), mimetype='text/plain'), 200
        
        

@bp_admin_instruments.route('/ajax_admin_delete_secondsub_indicator', methods=['POST'])
def admin_delete_secondsub_indicator():
    
    button = request.form.get('button')
    indicatorID = request.form.get('indicatorID')

    if button != 'delete_secondsub_indicator':
        data = {
            'status': 'invalid_request',
            'message': 'Button not recognized'
        }
        return Response(json.dumps(data), mimetype='text/plain'), 200
    else:
        db = Database()
        query = "DELETE FROM  tbl_indicators_secondsub WHERE indicator_id=%s"
        params = (indicatorID,)
        result = db.execute(query, params)
        
        if result:
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
                'message': 'Failed to delete indicator',
            }
            return Response(json.dumps(data), mimetype='text/plain'), 200
        
        

@bp_admin_instruments.route('/ajax_admin_delete_thirdsub_indicator', methods=['POST'])
def admin_delete_thirdsub_indicator():
    
    button = request.form.get('button')
    indicatorID = request.form.get('indicatorID')

    if button != 'delete_thirdsub_indicator':
        data = {
            'status': 'invalid_request',
            'message': 'Button not recognized'
        }
        return Response(json.dumps(data), mimetype='text/plain'), 200
    else:
        db = Database()
        query = "DELETE FROM  tbl_indicators_thirdsub WHERE indicator_id=%s"
        params = (indicatorID,)
        result = db.execute(query, params)
        
        if result:
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
                'message': 'Failed to delete indicator',
            }
            return Response(json.dumps(data), mimetype='text/plain'), 200
        
        

@bp_admin_instruments.route('/ajax_admin_delete_fourthsub_indicator', methods=['POST'])
def admin_delete_fourthsub_indicator():
    
    button = request.form.get('button')
    indicatorID = request.form.get('indicatorID')

    if button != 'delete_fourthsub_indicator':
        data = {
            'status': 'invalid_request',
            'message': 'Button not recognized'
        }
        return Response(json.dumps(data), mimetype='text/plain'), 200
    else:
        db = Database()
        query = "DELETE FROM  tbl_indicators_fourthsub WHERE indicator_id=%s"
        params = (indicatorID,)
        result = db.execute(query, params)
        
        if result:
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
                'message': 'Failed to delete indicator',
            }
            return Response(json.dumps(data), mimetype='text/plain'), 200