from flask import Flask, render_template, session, redirect, request
import os


from blueprints.admin.fn_admin_login import bp_admin_login
from blueprints.admin.fn_admin_university_colleges import bp_admin_university_colleges
from blueprints.admin.fn_admin_instruments import bp_admin_instruments
from blueprints.admin.fn_admin_results import bp_admin_results

from blueprints.sucs.fn_sucs_registration import bp_sucs_registration
from blueprints.sucs.fn_sucs_login import bp_sucs_login
from blueprints.sucs.fn_sucs_rate_indicators import bp_sucs_rate_indicators
from blueprints.sucs.fn_sucs_advance import bp_sucs_advance

app = Flask(__name__,  template_folder='pages', static_folder='assets')
app.secret_key = os.getenv('SECRET_KEY', 'default_fallback_key')

app.register_blueprint(bp_admin_login)
app.register_blueprint(bp_admin_university_colleges)
app.register_blueprint(bp_admin_instruments)
app.register_blueprint(bp_admin_results)



app.register_blueprint(bp_sucs_registration)
app.register_blueprint(bp_sucs_login)
app.register_blueprint(bp_sucs_rate_indicators)
app.register_blueprint(bp_sucs_advance)



@app.route('/admin')
def admin_login():
    if 'USER_ID' in session and 'USER_EMAIL' in session:
        return redirect('/admin-dashboard')
    return render_template('admin/pg_admin_login.html', titleBar=os.getenv('MY_APP_NAME'), footerNAme=os.getenv('MY_APP_NAME'))

@app.route('/admin-dashboard')
def admin_dashboard():
    if 'USER_ID' not in session and 'USER_EMAIL' not in session:
        return redirect('/admin')
    return render_template('admin/pg_admin_dashboard.html', titleBar=os.getenv('MY_APP_NAME'), footerNAme=os.getenv('MY_APP_NAME'))

@app.route('/admin-university-colleges')
def admin_university_colleges():
    if 'USER_ID' not in session and 'USER_EMAIL' not in session:
        return redirect('/admin')
    return render_template('admin/pg_admin_university_colleges.html', titleBar=os.getenv('MY_APP_NAME'), footerNAme=os.getenv('MY_APP_NAME'))

@app.route('/admin-instruments')
def admin_instruments():
    if 'USER_ID' not in session and 'USER_EMAIL' not in session:
        return redirect('/admin')
    return render_template('admin/pg_admin_instruments.html', titleBar=os.getenv('MY_APP_NAME'), footerNAme=os.getenv('MY_APP_NAME'))

@app.route('/admin-edit-instruments', methods=['post', 'get'])
def admin_edit_instruments():
    if 'USER_ID' not in session and 'USER_EMAIL' not in session:
        return redirect('/admin')
    
    data_id = request.form.get('data_id')
    data_jc = request.form.get('data_jc')

    if not data_id and not data_jc:
        return redirect('/admin-instruments')
    return render_template('admin/pg_admin_edit_instruments.html', dataID=data_id, dataJC=data_jc, titleBar=os.getenv('MY_APP_NAME'), footerNAme=os.getenv('MY_APP_NAME'))

@app.route('/admin-view-results', methods=['post', 'get'])
def admin_view_results():
    if 'USER_ID' not in session and 'USER_EMAIL' not in session:
        return redirect('/admin')
    
    data_id = request.form.get('data_id')
    data_jc = request.form.get('data_jc')

    if not data_id and not data_jc:
        return redirect('/admin-instruments')
    return render_template('admin/pg_admin_view_results.html', dataID=data_id, dataJC=data_jc, titleBar=os.getenv('MY_APP_NAME'), footerNAme=os.getenv('MY_APP_NAME'))








@app.route('/sucs-register')
def sucs_register():
    if 'USER_SUCS_ID' in session and 'USER_SUCS_EMAIL' in session:
        return redirect('/sucs-dashboard')
    return render_template('sucs/pg_sucs_register.html', titleBar=os.getenv('MY_APP_NAME'), footerNAme=os.getenv('MY_APP_NAME'))

@app.route('/sucs-login')
def sucs_login():
    if 'USER_SUCS_ID' in session and 'USER_SUCS_EMAIL' in session:
        return redirect('/sucs-dashboard')
    return render_template('sucs/pg_sucs_login.html', titleBar=os.getenv('MY_APP_NAME'), footerNAme=os.getenv('MY_APP_NAME'))

@app.route('/sucs-dashboard')
def sucs_dashboard():
    if 'USER_SUCS_ID' not in session and 'USER_SUCS_EMAIL' not in session:
        return redirect('/sucs-login')
    return render_template('sucs/pg_sucs_dashboard.html', titleBar=os.getenv('MY_APP_NAME'), footerNAme=os.getenv('MY_APP_NAME'))

@app.route('/sucs-instruments')
def sucs_instruments():
    if 'USER_SUCS_ID' not in session and 'USER_SUCS_EMAIL' not in session:
        return redirect('/sucs-login')
    return render_template('sucs/pg_sucs_instruments.html', titleBar=os.getenv('MY_APP_NAME'), footerNAme=os.getenv('MY_APP_NAME'))

@app.route('/sucs-edit-point', methods=['post', 'get'])
def sucs_edit_point():
    if 'USER_SUCS_ID' not in session and 'USER_SUCS_EMAIL' not in session:
        return redirect('/sucs-login')
    
    data_id = request.form.get('data_id')
    data_jc = request.form.get('data_jc')
    
    return render_template('sucs/pg_sucs_edit_point.html', dataID=data_id, dataJC=data_jc,  titleBar=os.getenv('MY_APP_NAME'), footerNAme=os.getenv('MY_APP_NAME'))

@app.route('/sucs-advance')
def sucs_advance():
    if 'USER_SUCS_ID' not in session and 'USER_SUCS_EMAIL' not in session:
        return redirect('/sucs-login')
    return render_template('sucs/pg_sucs_advance.html', titleBar=os.getenv('MY_APP_NAME'), footerNAme=os.getenv('MY_APP_NAME'))













@app.route('/')
def users_home():
    return render_template('users/pg_users_home.html', titleBar=os.getenv('MY_APP_NAME'), footerNAme=os.getenv('MY_APP_NAME'))

@app.route('/university-performance-evaluation')
def user_university_performance_evaluation():
    return render_template('users/pg_users_home.html', titleBar=os.getenv('MY_APP_NAME'), footerNAme=os.getenv('MY_APP_NAME'))











@app.route('/admin_logout')
def admin_logout():
    session.clear()
    return redirect('/admin')

@app.route('/sucs_logout')
def sucs_logout():
    session.clear()
    return redirect('/sucs-login')

if __name__ == '__main__':
    app.run(debug=True)
