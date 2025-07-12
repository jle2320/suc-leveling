from flask import Blueprint, request, session
from database import Database
import json
from flask import Response

bp_sucs_rate_indicators = Blueprint('bp_sucs_rate_indicators',__name__)

@bp_sucs_rate_indicators.route('/ajax_suc_get_instrument_kra', methods=['POST'])
def suc_get_instrument_kra():
    
    button = request.form.get('button')
    instrument_id = request.form.get('instrument_id')
    sucID = session['SUCS_ID']

    if button != 'get_instrument_kra':
        data = {
            'status': 'invalid_request',
            'message': 'Button not recognized'
        }
        return Response(json.dumps(data), mimetype='text/plain'), 200
    else:
        db = Database()



        

        query = """
            INSERT IGNORE INTO tbl_points_main
                (indicator_id,suc_id,point_value)
            SELECT
                indicator_main.indicator_id,
                %s,
                0
            FROM 
                tbl_kra as kra
            JOIN
                tbl_indicators_main as indicator_main 
                ON kra.kra_id = indicator_main.kra_id
            WHERE kra.instrument_id = %s
            ORDER BY kra.kra_id ASC;
        """
        params = (sucID,instrument_id,)
        db.execute(query, params)

        query = """
            INSERT IGNORE INTO tbl_points_firstsub
                (indicator_id,suc_id,point_value)
            SELECT 
                firstsub.indicator_id,
                %s,
                0
            FROM 
                tbl_kra as kra 
            JOIN tbl_indicators_main as indicator_main 
                ON kra.kra_id = indicator_main.kra_id
            JOIN tbl_indicators_firstsub as firstsub
                ON indicator_main.indicator_id = firstsub.prime_indicator_id
            WHERE kra.instrument_id = %s
            ORDER BY indicator_main.indicator_id ASC;
        """
        params = (sucID,instrument_id,)
        db.execute(query, params)

        query = """
            INSERT IGNORE INTO tbl_points_secondsub
                (indicator_id,suc_id,point_value)
            SELECT 
                secondsub.indicator_id,
                %s,
                0
            FROM 
                tbl_kra as kra 
            JOIN tbl_indicators_main as indicator_main 
                ON kra.kra_id = indicator_main.kra_id
            JOIN tbl_indicators_firstsub as firstsub
                ON indicator_main.indicator_id = firstsub.prime_indicator_id
            JOIN tbl_indicators_secondsub as secondsub
                ON firstsub.indicator_id = secondsub.indicator_firstsub_id
            WHERE kra.instrument_id = %s
            ORDER BY firstsub.indicator_id ASC;
        """
        params = (sucID,instrument_id,)
        db.execute(query, params)

        query = """
            INSERT IGNORE INTO tbl_points_thirdsub
                (indicator_id,suc_id,point_value)
            SELECT 
                thirdsub.indicator_id,
                %s,
                0
            FROM 
                tbl_kra as kra 
            JOIN tbl_indicators_main as indicator_main 
                ON kra.kra_id = indicator_main.kra_id
            JOIN tbl_indicators_firstsub as firstsub
                ON indicator_main.indicator_id = firstsub.prime_indicator_id
            JOIN tbl_indicators_secondsub as secondsub
                ON firstsub.indicator_id = secondsub.indicator_firstsub_id
            JOIN tbl_indicators_thirdsub as thirdsub
                ON secondsub.indicator_id = thirdsub.indicator_secondsub_id
            WHERE kra.instrument_id = %s
            ORDER BY secondsub.indicator_id ASC;
        """
        params = (sucID,instrument_id,)
        db.execute(query, params)

        query = """
            INSERT IGNORE INTO tbl_points_fourthsub
                (indicator_id,suc_id,point_value)
            SELECT 
                fourthsub.indicator_id,
                %s,
                0
            FROM 
                tbl_kra as kra 
            JOIN tbl_indicators_main as indicator_main 
                ON kra.kra_id = indicator_main.kra_id
            JOIN tbl_indicators_firstsub as firstsub
                ON indicator_main.indicator_id = firstsub.prime_indicator_id
            JOIN tbl_indicators_secondsub as secondsub
                ON firstsub.indicator_id = secondsub.indicator_firstsub_id
            JOIN tbl_indicators_thirdsub as thirdsub
                ON secondsub.indicator_id = thirdsub.indicator_secondsub_id
            JOIN tbl_indicators_fourthsub as fourthsub
                ON thirdsub.indicator_id = fourthsub.indicator_thirdsub_id
            WHERE kra.instrument_id = %s
            ORDER BY thirdsub.indicator_id ASC;
        """
        params = (sucID,instrument_id,)
        db.execute(query, params)



        kra = """
            SELECT 
                kra.kra_id, 
                kra.kra_name, 
                kra.kra_point
            FROM 
                tbl_kra as kra 
            WHERE kra.instrument_id = %s
        """
        params = (instrument_id,)
        db.execute(kra, params)
        raw_data_kra = db.fetchall()

        kraData = {}


        if raw_data_kra:

            





            
            for entryKRA in raw_data_kra:
                kraID = entryKRA["kra_id"]
                kraNAME = entryKRA["kra_name"]
                kraPOINT = entryKRA["kra_point"]
                
                kraData[kraID] = {
                    "kra_id": kraID,
                    "kra_name": kraNAME,
                    "kra_point": kraPOINT,
                    "main_indicators": []
                }

                indicator0 = """
                        SELECT 
                            indicator.indicator_id as main_indicator_id, 
                            indicator.indicator_name as main_indicator_name, 
                            indicator.indicator_point as main_indicator_point, 
                            indicator.indicator_type as main_indicator_type,
                            points.point_id as main_point_id,
                            points.point_value as main_point_value
                        FROM
                            tbl_indicators_main as indicator
                        JOIN
                            tbl_points_main as points
                            ON indicator.indicator_id = points.indicator_id
                        WHERE
                            indicator.kra_id = %s
                        AND
                            points.suc_id = %s;
                    """
                params = (kraID,sucID,)
                db.execute(indicator0, params)
                raw_data_indicator0 = db.fetchall()
                
                if raw_data_indicator0:
                    for entryIndicator0 in raw_data_indicator0:
                        indicatorID0 = entryIndicator0['main_indicator_id']
                        indicatorNAME0 = entryIndicator0['main_indicator_name']
                        indicatorPOINT0 = entryIndicator0['main_indicator_point']
                        indicatorTYPE0 = entryIndicator0['main_indicator_type']
                        pointID0 = entryIndicator0['main_point_id']
                        pointVALUE0 = entryIndicator0['main_point_value']

                        current_main = None
                        if indicatorID0 is not None:
                            existing_main = next(
                                (mi for mi in kraData[kraID]["main_indicators"]
                                if mi["main_indicator_id"] == indicatorID0), None)

                            if not existing_main:
                                current_main = {
                                     "main_indicator_id": indicatorID0,
                                     "main_indicator_name": indicatorNAME0,
                                     "main_indicator_point": indicatorPOINT0,
                                     "main_indicator_type": indicatorTYPE0,
                                     "main_point_id": pointID0,
                                     "main_point_value": pointVALUE0,
                                     "firstsub_indicators": []
                                }
                                kraData[kraID]["main_indicators"].append(current_main)
                            else:
                                current_main = existing_main

                        indicator1 = """
                                SELECT 
                                    indicator.indicator_id as main_indicator_id, 
                                    indicator.indicator_name as main_indicator_name, 
                                    indicator.indicator_point as main_indicator_point, 
                                    indicator.indicator_type as main_indicator_type,
                                    points.point_id as main_point_id,
                                    points.point_value as main_point_value
                                FROM
                                    tbl_indicators_firstsub as indicator
                                JOIN
                                    tbl_points_firstsub as points
                                    ON indicator.indicator_id = points.indicator_id
                                WHERE
                                    indicator.prime_indicator_id = %s
                                AND
                                    points.suc_id = %s;
                            """
                        params = (indicatorID0,sucID,)
                        db.execute(indicator1, params)
                        raw_data_indicator1 = db.fetchall()
                        
                        if raw_data_indicator1:
                            for entryIndicator1 in raw_data_indicator1:
                                indicatorID1 = entryIndicator1['main_indicator_id']
                                indicatorNAME1 = entryIndicator1['main_indicator_name']
                                indicatorPOINT1 = entryIndicator1['main_indicator_point']
                                indicatorTYPE1 = entryIndicator1['main_indicator_type']
                                pointID1 = entryIndicator1['main_point_id']
                                pointVALUE1 = entryIndicator1['main_point_value']

                                current_firstsub = None
                                if indicatorID1 is not None and current_main is not None:
                                    existing_firstsub = next(
                                        (fs for fs in current_main["firstsub_indicators"]
                                        if fs["firstsub_indicator_id"] == indicatorID1), None)

                                    if not existing_firstsub:
                                        current_firstsub = {
                                            "firstsub_indicator_id": indicatorID1,
                                            "firstsub_indicator_name": indicatorNAME1,
                                            "firstsub_indicator_point": indicatorPOINT1,
                                            "firstsub_indicator_type": indicatorTYPE1,
                                            "firstsub_point_id": pointID1,
                                            "firstsub_point_value": pointVALUE1,
                                            "secondsub_indicators": []
                                        }
                                        current_main["firstsub_indicators"].append(current_firstsub)
                                    else:
                                        current_firstsub = existing_firstsub

                                indicator2 = """
                                        SELECT 
                                            indicator.indicator_id as main_indicator_id, 
                                            indicator.indicator_name as main_indicator_name, 
                                            indicator.indicator_point as main_indicator_point, 
                                            indicator.indicator_type as main_indicator_type,
                                            points.point_id as main_point_id,
                                            points.point_value as main_point_value
                                        FROM
                                            tbl_indicators_secondsub as indicator
                                        JOIN
                                            tbl_points_secondsub as points
                                            ON indicator.indicator_id = points.indicator_id
                                        WHERE
                                            indicator.indicator_firstsub_id = %s
                                        AND
                                            points.suc_id = %s;
                                    """
                                params = (indicatorID1,sucID,)
                                db.execute(indicator2, params)
                                raw_data_indicator2 = db.fetchall()

                                if raw_data_indicator2:
                                    for entryIndicator2 in raw_data_indicator2:
                                        indicatorID2 = entryIndicator2['main_indicator_id']
                                        indicatorNAME2 = entryIndicator2['main_indicator_name']
                                        indicatorPOINT2 = entryIndicator2['main_indicator_point']
                                        indicatorTYPE2 = entryIndicator2['main_indicator_type']
                                        pointID2 = entryIndicator2['main_point_id']
                                        pointVALUE2 = entryIndicator2['main_point_value']

                                        current_secondsub = None
                                        if indicatorID2 is not None and current_firstsub is not None:
                                            existing_secondsub = next(
                                                (ss for ss in current_firstsub["secondsub_indicators"]
                                                if ss["secondsub_indicator_id"] == indicatorID2), None)

                                            if not existing_secondsub:
                                                current_secondsub = {
                                                    "secondsub_indicator_id": indicatorID2,
                                                    "secondsub_indicator_name": indicatorNAME2,
                                                    "secondsub_indicator_point": indicatorPOINT2,
                                                    "secondsub_indicator_type": indicatorTYPE2,
                                                    "secondsub_point_id": pointID2,
                                                    "secondsub_point_value": pointVALUE2,
                                                    "thirdsub_indicators": []
                                                }
                                                current_firstsub["secondsub_indicators"].append(current_secondsub)
                                            else:
                                                current_secondsub = existing_secondsub

                                        indicator3 = """
                                                SELECT 
                                                    indicator.indicator_id as main_indicator_id, 
                                                    indicator.indicator_name as main_indicator_name, 
                                                    indicator.indicator_point as main_indicator_point, 
                                                    indicator.indicator_type as main_indicator_type,
                                                    points.point_id as main_point_id,
                                                    points.point_value as main_point_value
                                                FROM
                                                    tbl_indicators_thirdsub as indicator
                                                JOIN
                                                    tbl_points_thirdsub as points
                                                    ON indicator.indicator_id = points.indicator_id
                                                WHERE
                                                    indicator.indicator_secondsub_id = %s
                                                AND
                                                    points.suc_id = %s;
                                            """
                                        params = (indicatorID2,sucID,)
                                        db.execute(indicator3, params)
                                        raw_data_indicator3 = db.fetchall()
                                        if raw_data_indicator3:
                                            for entryIndicator3 in raw_data_indicator3:
                                                indicatorID3 = entryIndicator3['main_indicator_id']
                                                indicatorNAME3 = entryIndicator3['main_indicator_name']
                                                indicatorPOINT3 = entryIndicator3['main_indicator_point']
                                                indicatorTYPE3 = entryIndicator3['main_indicator_type']
                                                pointID3 = entryIndicator3['main_point_id']
                                                pointVALUE3 = entryIndicator3['main_point_value']
                                                
                                                current_thirdsub = None
                                                if indicatorID3 is not None and current_secondsub is not None:
                                                    existing_thirdsub = next(
                                                        (ts for ts in current_secondsub["thirdsub_indicators"]
                                                        if ts["thirdsub_indicator_id"] == indicatorID3), None)

                                                    if not existing_thirdsub:
                                                        current_thirdsub = {
                                                            "thirdsub_indicator_id": indicatorID3,
                                                            "thirdsub_indicator_name": indicatorNAME3,
                                                            "thirdsub_indicator_point": indicatorPOINT3,
                                                            "thirdsub_indicator_type": indicatorTYPE3,
                                                            "thirdsub_point_id": pointID3,
                                                            "thirdsub_point_value": pointVALUE3,
                                                            "fourthsub_indicators": []
                                                        }
                                                        current_secondsub["thirdsub_indicators"].append(current_thirdsub)
                                                    else:
                                                        current_thirdsub = existing_thirdsub
                                                
                                                indicator4 = """
                                                        SELECT 
                                                            indicator.indicator_id as main_indicator_id, 
                                                            indicator.indicator_name as main_indicator_name, 
                                                            indicator.indicator_point as main_indicator_point, 
                                                            indicator.indicator_type as main_indicator_type,
                                                            points.point_id as main_point_id,
                                                            points.point_value as main_point_value
                                                        FROM
                                                            tbl_indicators_fourthsub as indicator
                                                        JOIN
                                                            tbl_points_fourthsub as points
                                                            ON indicator.indicator_id = points.indicator_id
                                                        WHERE
                                                            indicator.indicator_thirdsub_id = %s
                                                        AND
                                                            points.suc_id = %s;
                                                    """
                                                params = (indicatorID3,sucID,)
                                                db.execute(indicator4, params)
                                                raw_data_indicator4 = db.fetchall()
                                                if raw_data_indicator4:
                                                    for entryIndicator4 in raw_data_indicator4:
                                                        indicatorID4 = entryIndicator4['main_indicator_id']
                                                        indicatorNAME4 = entryIndicator4['main_indicator_name']
                                                        indicatorPOINT4 = entryIndicator4['main_indicator_point']
                                                        indicatorTYPE4 = entryIndicator4['main_indicator_type']
                                                        pointID4 = entryIndicator4['main_point_id']
                                                        pointVALUE4 = entryIndicator4['main_point_value']

                                                        if indicatorID4 is not None and current_thirdsub is not None:
                                                            existing_fourthsub = next(
                                                                (fs for fs in current_thirdsub["fourthsub_indicators"]
                                                                if fs["fourthsub_indicator_id"] == indicatorID4), None)

                                                            if not existing_fourthsub:
                                                                current_thirdsub["fourthsub_indicators"].append({
                                                                    "fourthsub_indicator_id": indicatorID4,
                                                                    "fourthsub_indicator_name": indicatorNAME4,
                                                                    "fourthsub_indicator_point": indicatorPOINT4,
                                                                    "fourthsub_indicator_type": indicatorTYPE4,
                                                                    "fourthsub_point_id": pointID4,
                                                                    "fourthsub_point_value": pointVALUE4
                                                                })
            result = list(kraData.values())
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
        
        









@bp_sucs_rate_indicators.route('/ajax_sucs_save_point_0', methods=['POST'])
def sucs_save_point_0():
    
    button = request.form.get('button')
    pointID = request.form.get('pointID')
    pointValue = request.form.get('pointValue')

    if button != 'save_point_0':
        data = {
            'status': 'invalid_request',
            'message': 'Button not recognized'
        }
        return Response(json.dumps(data), mimetype='text/plain'), 200
    else:
        db = Database()
        query = "UPDATE tbl_points_main SET point_value=%s WHERE point_id=%s"
        params = (pointValue,pointID,)
        result = db.execute(query, params)
        
        if result:
            db.close() 
            data = {
                'status': 'success',
                'message': 'Points saved',
            }
            return Response(json.dumps(data), mimetype='text/plain'), 200
        else:
            db.close() 
            data = {
                'status': 'failed',
                'message': 'Failed to saved points',
            }
            return Response(json.dumps(data), mimetype='text/plain'), 200



@bp_sucs_rate_indicators.route('/ajax_sucs_save_point_1', methods=['POST'])
def sucs_save_point_1():
    
    button = request.form.get('button')
    pointID = request.form.get('pointID')
    pointValue = request.form.get('pointValue')

    if button != 'save_point_1':
        data = {
            'status': 'invalid_request',
            'message': 'Button not recognized'
        }
        return Response(json.dumps(data), mimetype='text/plain'), 200
    else:
        db = Database()
        query = "UPDATE tbl_points_firstsub SET point_value=%s WHERE point_id=%s"
        params = (pointValue,pointID,)
        result = db.execute(query, params)
        
        if result:
            db.close() 
            data = {
                'status': 'success',
                'message': 'Points saved',
            }
            return Response(json.dumps(data), mimetype='text/plain'), 200
        else:
            db.close() 
            data = {
                'status': 'failed',
                'message': 'Failed to saved points',
            }
            return Response(json.dumps(data), mimetype='text/plain'), 200



@bp_sucs_rate_indicators.route('/ajax_sucs_save_point_2', methods=['POST'])
def sucs_save_point_2():
    
    button = request.form.get('button')
    pointID = request.form.get('pointID')
    pointValue = request.form.get('pointValue')

    if button != 'save_point_2':
        data = {
            'status': 'invalid_request',
            'message': 'Button not recognized'
        }
        return Response(json.dumps(data), mimetype='text/plain'), 200
    else:
        db = Database()
        query = "UPDATE tbl_points_secondsub SET point_value=%s WHERE point_id=%s"
        params = (pointValue,pointID,)
        result = db.execute(query, params)
        
        if result:
            db.close() 
            data = {
                'status': 'success',
                'message': 'Points saved',
            }
            return Response(json.dumps(data), mimetype='text/plain'), 200
        else:
            db.close() 
            data = {
                'status': 'failed',
                'message': 'Failed to saved points',
            }
            return Response(json.dumps(data), mimetype='text/plain'), 200



@bp_sucs_rate_indicators.route('/ajax_sucs_save_point_3', methods=['POST'])
def sucs_save_point_3():
    
    button = request.form.get('button')
    pointID = request.form.get('pointID')
    pointValue = request.form.get('pointValue')

    if button != 'save_point_3':
        data = {
            'status': 'invalid_request',
            'message': 'Button not recognized'
        }
        return Response(json.dumps(data), mimetype='text/plain'), 200
    else:
        db = Database()
        query = "UPDATE tbl_points_thirdsub SET point_value=%s WHERE point_id=%s"
        params = (pointValue,pointID,)
        result = db.execute(query, params)
        
        if result:
            db.close() 
            data = {
                'status': 'success',
                'message': 'Points saved',
            }
            return Response(json.dumps(data), mimetype='text/plain'), 200
        else:
            db.close() 
            data = {
                'status': 'failed',
                'message': 'Failed to saved points',
            }
            return Response(json.dumps(data), mimetype='text/plain'), 200



@bp_sucs_rate_indicators.route('/ajax_sucs_save_point_4', methods=['POST'])
def sucs_save_point_4():
    
    button = request.form.get('button')
    pointID = request.form.get('pointID')
    pointValue = request.form.get('pointValue')

    if button != 'save_point_4':
        data = {
            'status': 'invalid_request',
            'message': 'Button not recognized'
        }
        return Response(json.dumps(data), mimetype='text/plain'), 200
    else:
        db = Database()
        query = "UPDATE tbl_points_fourthsub SET point_value=%s WHERE point_id=%s"
        params = (pointValue,pointID,)
        result = db.execute(query, params)
        
        if result:
            db.close() 
            data = {
                'status': 'success',
                'message': 'Points saved',
            }
            return Response(json.dumps(data), mimetype='text/plain'), 200
        else:
            db.close() 
            data = {
                'status': 'failed',
                'message': 'Failed to saved points',
            }
            return Response(json.dumps(data), mimetype='text/plain'), 200
        



@bp_sucs_rate_indicators.route('/ajax_sucs_view_result', methods=['POST'])
def sucs_view_result():
    
    button = request.form.get('button')
    instrument_id = request.form.get('instrument_id')
    sucID = session['SUCS_ID']

    if button != 'view_result':
        data = {
            'status': 'invalid_request',
            'message': 'Button not recognized'
        }
        return Response(json.dumps(data), mimetype='text/plain'), 200
    else:
        db = Database()
        query = """
                SELECT 
                    SUM(point_value) as results
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
                AND
                    sucs.suc_id = %s
                """
        param = (instrument_id,sucID,)
        db.execute(query,param)
        raw_result = db.fetchall()

        query = "SELECT * FROM tbl_criteria WHERE instrument_id=%s"
        param = (instrument_id,)
        db.execute(query,param)
        raw_criteria = db.fetchall()
        dataa = []
        if raw_result and raw_criteria:
            for rows in raw_result:
                resultPoint = rows['results']

                for criteria in raw_criteria:
                    levelName = criteria['criteria_level']
                    minPoint = criteria['criteria_minpoint']
                    maxPoint = criteria['criteria_maxpoint']
                
                    if float(minPoint) <= float(resultPoint) <= float(maxPoint):
                        dataa.append({
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
                'message': 'No result found'
            }
            return Response(json.dumps(data), mimetype='text/plain'), 200