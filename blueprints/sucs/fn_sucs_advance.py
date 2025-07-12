from flask import Blueprint, request, session
from database import Database
import json
from flask import Response
from .fn_sucs_predictor import predict_next_level
import subprocess

bp_sucs_advance = Blueprint('bp_sucs_advance',__name__)





def generate_llama_recommendation(kra_name, current_score, max_point):
    prompt = f"""
        You are an expert evaluator. An indicator under the KRA \"{kra_name}\" has a current score of {current_score} out of {max_point}.
        What specific actions or strategies should be implemented to achieve the maximum points for this indicator?
        Provide 1–2 short but concise practical and realistic examples.
        """

    try:
        result = subprocess.run(
            ["C:\\Users\\ASUS\\AppData\\Local\\Programs\\Ollama\\ollama.exe", "run", "llama3.2"],
            input=prompt.encode('utf-8'),
            capture_output=True,
            check=True
        )
        output = result.stdout.decode('utf-8').strip()
        return output

    except subprocess.CalledProcessError as e:
        return f"Error running llama3 model: {e.stderr.decode('utf-8')}"
    except Exception as e:
        return f"General error: {str(e)}"
    







@bp_sucs_advance.route('/ajax_sucs_recommendations', methods=['POST'])
def sucs_recommendations():
    
    button = request.form.get('button')
    indicatorNAME = request.form.get('indicatorNAME')
    indicatorPOINT = request.form.get('indicatorPOINT')
    indicatorMAXPOINT = request.form.get('indicatorMAXPOINT')

    if button != 'recommendations':
        data = {
            'status': 'invalid_request',
            'message': 'Button not recognized'
        }
        return Response(json.dumps(data), mimetype='text/plain'), 200
    else:

        data = {
            'status': 'success',
            'message': 'list',
            'recommendations': generate_llama_recommendation(indicatorNAME, indicatorPOINT, indicatorMAXPOINT)
        }
        return Response(json.dumps(data), mimetype='text/plain'), 200
        














@bp_sucs_advance.route('/ajax_sucs_intializeData', methods=['POST'])
def sucs_intializeData():
    

    button = request.form.get('button')
    sucID = session['SUCS_ID']

    if button != 'initializeData':
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
                    kra.instrument_id,
                    inss.instrument_jc,
                    inss.instrument_id
                FROM
                	tbl_instruments as inss
                JOIN
                    tbl_kra as kra
                    ON inss.instrument_id = kra.instrument_id
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
                    sucs.suc_id = %s
                GROUP BY
                    kra.instrument_id
                ORDER BY
                    kra.instrument_id DESC
                LIMIT 5;
                """
        param = (sucID,)
        db.execute(query,param)
        raw_result = db.fetchall()




        queryKRA = """
                SELECT * FROM tbl_kra WHERE instrument_id = (SELECT MAX(instrument_id) FROM tbl_instruments)
                """
        db.execute(queryKRA,)
        KRADATA = db.fetchall()

        if KRADATA:
            mergedIndicators = {}

            for kraRow in KRADATA:
                KRAID = kraRow['kra_id']
                KRANAME = kraRow['kra_name']

                if KRAID not in mergedIndicators:
                    mergedIndicators[KRAID] = {
                        "KRAID": KRAID,
                        "KRANAME": KRANAME,
                        "main_indicators": []
                    }
            
                queryMAIN= """
                        SELECT 
                            indi.indicator_id as indicator_id,
                            indi.indicator_name as indicator_name,
                            indi.indicator_point as indicator_maxpoint,
                            indi.indicator_type as indicator_type,
                            points.point_value as point_value
                        FROM 
                            tbl_indicators_main  as indi
                        JOIN
                            tbl_points_main as points
                            ON indi.indicator_id = points.indicator_id
                        WHERE 
                            indi.kra_id = %s
                        AND 
                            points.suc_id = %s
                        """
                db.execute(queryMAIN,(KRAID,sucID,))
                MAINDATA = db.fetchall()
                for main_row in MAINDATA:
                    current_main = None
                    if main_row['indicator_id'] is not None:
                        existing_main = next(
                            (mi for mi in mergedIndicators[KRAID]["main_indicators"]
                            if mi["indicator_id"] == main_row['indicator_id']), None)

                        if not existing_main:
                            current_main = {
                                "indicator_id": main_row['indicator_id'],
                                "indicator_name": main_row["indicator_name"],
                                "indicator_maxpoint": main_row["indicator_maxpoint"],
                                "indicator_type": main_row["indicator_type"],
                                "indicator_point": main_row["point_value"],
                                "firstsub_indicators": []
                            }
                            mergedIndicators[KRAID]["main_indicators"].append(current_main)
                        else:
                            current_main = existing_main



                    queryFIRST= """
                            SELECT 
                                indi.indicator_id as indicator_id,
                                indi.indicator_name as indicator_name,
                                indi.indicator_point as indicator_maxpoint,
                                indi.indicator_type as indicator_type,
                                points.point_value as point_value
                            FROM 
                                tbl_indicators_firstsub  as indi
                            JOIN
                                tbl_points_firstsub as points
                                ON indi.indicator_id = points.indicator_id
                            WHERE 
                                indi.prime_indicator_id = %s
                            AND 
                                points.suc_id = %s
                            """
                    db.execute(queryFIRST,(main_row['indicator_id'],sucID,))
                    FIRSTDATA = db.fetchall()
                    for first_row in FIRSTDATA:

                        current_firstsub = None
                        if first_row["indicator_id"] is not None and current_main is not None:
                            existing_firstsub = next(
                                (fs for fs in current_main["firstsub_indicators"]
                                if fs["indicator_id"] == first_row["indicator_id"]), None)

                            if not existing_firstsub:
                                current_firstsub = {
                                    "indicator_id": first_row['indicator_id'],
                                    "indicator_name": first_row["indicator_name"],
                                    "indicator_maxpoint": first_row["indicator_maxpoint"],
                                    "indicator_type": first_row["indicator_type"],
                                    "indicator_point": first_row["point_value"],
                                    "secondsub_indicators": []
                                }
                                current_main["firstsub_indicators"].append(current_firstsub)
                            else:
                                current_firstsub = existing_firstsub

                        querySECOND= """
                                SELECT 
                                    indi.indicator_id as indicator_id,
                                    indi.indicator_name as indicator_name,
                                    indi.indicator_point as indicator_maxpoint,
                                    indi.indicator_type as indicator_type,
                                    points.point_value as point_value
                                FROM 
                                     tbl_indicators_secondsub  as indi
                                JOIN
                                    tbl_points_secondsub as points
                                    ON indi.indicator_id = points.indicator_id
                                WHERE 
                                    indi.indicator_firstsub_id = %s
                                    AND 
                                        points.suc_id = %s
                                """
                        db.execute(querySECOND,(first_row['indicator_id'],sucID,))
                        SECONDDATA = db.fetchall()
                        for second_row in SECONDDATA:

                            current_secondsub = None
                            if second_row["indicator_id"] is not None and current_firstsub is not None:
                                existing_secondsub = next(
                                    (ss for ss in current_firstsub["secondsub_indicators"]
                                    if ss["indicator_id"] == second_row["indicator_id"]), None)

                                if not existing_secondsub:
                                    current_secondsub = {
                                        "indicator_id": second_row['indicator_id'],
                                        "indicator_name": second_row["indicator_name"],
                                        "indicator_maxpoint": second_row["indicator_maxpoint"],
                                        "indicator_type": second_row["indicator_type"],
                                        "indicator_point": second_row["point_value"],
                                        "thirdsub_indicators": []
                                    }
                                    current_firstsub["secondsub_indicators"].append(current_secondsub)
                                else:
                                    current_secondsub = existing_secondsub
                            
                            queryTHIRD= """
                                SELECT 
                                    indi.indicator_id as indicator_id,
                                    indi.indicator_name as indicator_name,
                                    indi.indicator_point as indicator_maxpoint,
                                    indi.indicator_type as indicator_type,
                                    points.point_value as point_value
                                FROM 
                                     tbl_indicators_thirdsub  as indi
                                JOIN
                                    tbl_points_thirdsub as points
                                    ON indi.indicator_id = points.indicator_id
                                WHERE 
                                    indi.indicator_secondsub_id = %s
                                AND 
                                    points.suc_id = %s
                                """
                            db.execute(queryTHIRD,(second_row['indicator_id'],sucID,))
                            THIRDDATA = db.fetchall()
                            for third_row in THIRDDATA:

                                current_thirdsub = None
                                if third_row["indicator_id"] is not None and current_secondsub is not None:
                                    existing_thirdsub = next(
                                        (ts for ts in current_secondsub["thirdsub_indicators"]
                                        if ts["indicator_id"] == third_row["indicator_id"]), None)

                                    if not existing_thirdsub:
                                        current_thirdsub = {
                                            "indicator_id": third_row['indicator_id'],
                                            "indicator_name": third_row["indicator_name"],
                                            "indicator_maxpoint": third_row["indicator_maxpoint"],
                                            "indicator_type": third_row["indicator_type"],
                                            "indicator_point": third_row["point_value"],
                                            "fourthsub_indicators": []
                                        }
                                        current_secondsub["thirdsub_indicators"].append(current_thirdsub)
                                    else:
                                        current_thirdsub = existing_thirdsub

                                    queryFOURTH= """
                                        SELECT 
                                            indi.indicator_id as indicator_id,
                                            indi.indicator_name as indicator_name,
                                            indi.indicator_point as indicator_maxpoint,
                                            indi.indicator_type as indicator_type,
                                            points.point_value as point_value
                                        FROM 
                                            tbl_indicators_fourthsub  as indi
                                        JOIN
                                            tbl_points_fourthsub as points
                                            ON indi.indicator_id = points.indicator_id
                                        WHERE 
                                            indi.indicator_thirdsub_id = %s
                                        AND 
                                            points.suc_id = %s
                                        """
                                    db.execute(queryFOURTH,(third_row['indicator_id'],sucID,))
                                    FOURTHDATA = db.fetchall()
                                    for fourth_row in FOURTHDATA:

                                        if fourth_row["indicator_id"] is not None and current_thirdsub is not None:
                                            existing_fourthsub = next(
                                                (fs for fs in current_thirdsub["fourthsub_indicators"]
                                                if fs["indicator_id"] == fourth_row["indicator_id"]), None)

                                            if not existing_fourthsub:
                                                current_thirdsub["fourthsub_indicators"].append({
                                                    "indicator_id": fourth_row['indicator_id'],
                                                    "indicator_name": fourth_row["indicator_name"],
                                                    "indicator_maxpoint": fourth_row["indicator_maxpoint"],
                                                    "indicator_type": fourth_row["indicator_type"],
                                                    "indicator_point": fourth_row["point_value"],
                                                })
        dataa = {}
        if raw_result:
            
            for rows in raw_result:
                resultPoint = rows['results']
                resultJC = rows['instrument_jc']
                instrumentID = rows['instrument_id']
                if instrumentID not in dataa:
                    dataa[instrumentID] = {
                        'instrumentID': instrumentID,
                        'resultPoint': resultPoint,
                        'resultJC': 'Joint Circular No. ' + resultJC,
                        'levelName': None, 
                        'criteria': []
                    }

                query = "SELECT * FROM tbl_criteria WHERE instrument_id=%s"
                db.execute(query,(instrumentID,))
                raw_criteria = db.fetchall()
                for criteria in raw_criteria:
                    levelName = criteria['criteria_level']
                    minPoint = float(criteria['criteria_minpoint'])
                    maxPoint = float(criteria['criteria_maxpoint'])

                    dataa[instrumentID]['criteria'].append({
                        'levelName': levelName,
                        'minPoint': minPoint,
                        'maxPoint': maxPoint,
                    })

                    if minPoint <= resultPoint <= maxPoint:
                        dataa[instrumentID]['levelName'] = levelName

            db.close() 
            data = {
                'status': 'success',
                'message': 'list',
                'raw_data': dataa,
                'prediction': predict_next_level(dataa),
                'merge_indicators':mergedIndicators
            }
            return Response(json.dumps(data), mimetype='text/plain'), 200
        else:
            db.close() 
            data = {
                'status': 'no_data',
                'message': 'No result found'
            }
            return Response(json.dumps(data), mimetype='text/plain'), 200