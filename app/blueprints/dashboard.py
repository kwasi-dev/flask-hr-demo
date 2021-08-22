from flask import (Blueprint, redirect, render_template, request, session, url_for,request)

from app import db
from app.models import Appraisal, DisciplinaryAction, LeaveApproval, SwipeCard, EmployeeSwipeCard, Employee, Department, Timesheet, User, disciplinary_action
from flask_login import login_required
from datetime import datetime
bp = Blueprint('dashboard', __name__, url_prefix='/')
from datetime import date


@bp.route('/', methods=["POST","GET"])
@login_required
def home():
    today = date.today()
    d2 = today.strftime("%B %d, %Y")

    present_employees = Timesheet.query.filter(Timesheet.time_in >= today).all()
    emp_count = len(set([x.swipecard_id for x in present_employees]))

    incomplete_appraisals = Appraisal.query.filter(Appraisal.is_completed == False).all()
    appraisal_count = len(incomplete_appraisals)

    unapproved_leave = LeaveApproval.query.filter(LeaveApproval.approved == False).all()
    leave_count = len(unapproved_leave)

    disciplinary_actions = DisciplinaryAction.query.all()
    disciplinary_action_count = len(disciplinary_actions)
    return render_template('auth/dashboard.html', day=d2, emp_count=emp_count, appraisal_count=appraisal_count, leave_count=leave_count, disciplinary_action_count=disciplinary_action_count)

@bp.route('/read-card', methods=["POST","GET"])
def readCard():
    import nfc
    from nfc.tag.tt2 import Type2Tag
    with nfc.ContactlessFrontend('usb') as clf:
        tagg = clf.connect(rdwr={'on-connect': lambda tag: False})
        tag_id = (str(tagg)).split("=",1)[1] 
        print(tag_id)

    return tag_id

@bp.route('/assign-swipecard', methods=["POST","GET"])
@login_required
def assign_swipecard():
    if request.method == 'POST':
        employee_id = request.form['employee_id']
        swipecard_id = request.form['swipecard_id']
        
        if (employee_id and swipecard_id ):
            swipecard = SwipeCard.query.filter_by(rfid_identifier=swipecard_id).first()
            
            if not swipecard:
                swipecard = SwipeCard(rfid_identifier=swipecard_id)
                db.session.add(swipecard)
                db.session.commit()
            
            EmployeeSwipeCard.query.filter_by(swipecard_id=swipecard.id).delete()

            esc = EmployeeSwipeCard(
                employee_id = employee_id,
                swipecard_id = swipecard.id,
                issue_date = datetime.now(),
            )
            db.session.add(esc)
            db.session.commit()
        return redirect(url_for("dashboard.home"))
    return render_template('auth/dashboard.html')


@bp.route('/clerical', methods=["GET"])
@login_required
def clerical():
    all_employees = Employee.query.filter(Employee.emp_type=='clerical')
    swipecard_ids = []
    for rec in all_employees:
        if rec.empSwipeCard:
            swipecard_ids.append(rec.empSwipeCard[0].swipecard.id)
    all_timesheets = [x for x in Timesheet.query.all() if x.swipecard_id in swipecard_ids]

    today = date.today()
    present_employees = Timesheet.query.filter(Timesheet.time_in >= today).all()

    emp_count = len(set([x.swipecard_id for x in present_employees if x.swipecard_id in swipecard_ids]))
    return render_template('auth/clerical.html', employees=all_employees, timesheets=all_timesheets, emp_count=emp_count)


@bp.route('/technical', methods=["GET"])
@login_required
def technical():
    all_employees = Employee.query.filter(Employee.emp_type=='technical')
    swipecard_ids = []
    for rec in all_employees:
        if rec.empSwipeCard:
            swipecard_ids.append(rec.empSwipeCard[0].swipecard.id)
    all_timesheets = [x for x in Timesheet.query.all() if x.swipecard_id in swipecard_ids]
    return render_template('auth/technical.html', employees=all_employees, timesheets=all_timesheets)


@bp.route('/grant-login', methods=["POST"])
def create_user():
    emp_id = request.form['emp_id']
    email = request.form['email']
    password = request.form['password']
    
    # See if that user is created already, if it is, delete and recreate
    usr = User.query.filter(User.email == email).first()
    
    if usr:
        User.query.filter(User.email == email).delete()
        db.session.commit()

    usr = User(email, password)
    usr.employee_id = emp_id

    db.session.add(usr)
    db.session.commit()

    return redirect(url_for("employees.view_employee"))