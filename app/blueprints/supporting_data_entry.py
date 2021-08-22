import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for,request, jsonify
)
from werkzeug.security import check_password_hash, generate_password_hash
from hashlib import md5
from flask_jwt_extended import create_access_token, unset_jwt_cookies

from app import db, bcrypt
from ..models import Department, LeaveType, Timesheet, Employee
from flask_login import login_required

bp = Blueprint('support', __name__, url_prefix='/supporting-data-entry')


@bp.route('/department', methods=["POST","GET"])
@login_required
def department():
    if request.method == 'POST':
        formParams = request.form.keys()

        if ('department_name' in formParams):
            department_name = request.form['department_name']

            exists = Department.query.filter_by(department_name = department_name).first()
            if not exists:
                dept = Department(department_name=department_name)
                db.session.add(dept)
                db.session.commit()
    
    all_departments = Department.query.all()
    return render_template('auth/department.html', all_departments=all_departments)

@bp.route('/timesheets', methods=["POST","GET"])
@login_required
def timesheet():
    if request.method == 'POST':
        employee_id = request.form['employee_id']
        time_in = request.form['time_in']
        time_out = request.form['time_out']
        
        swipecard_id = Employee.query.filter(Employee.id == employee_id).first().empSwipeCard[0].swipecard_id
        timesheet = Timesheet(swipecard_id=swipecard_id, time_in=time_in, time_out=time_out)
        db.session.add(timesheet)
        db.session.commit()
        return redirect(url_for("support.timesheet"))
    
    all_timesheets = Timesheet.query.all()
    employee_with_cards = Employee.query.filter(Employee.empSwipeCard != None).all()

    return render_template('auth/timesheets.html', all_timesheets=all_timesheets, employees=employee_with_cards)


@bp.route('/leavetype', methods=["POST","GET"])
@login_required
def leavetype():
    if request.method == 'POST':
        formParams = request.form.keys()

        if ('leave_type_name' in formParams):
            leave_type = request.form['leave_type_name']

            exists = LeaveType.query.filter_by(leave_type = leave_type).first()
            if not exists:
                dept = LeaveType(leave_type = leave_type)
                db.session.add(dept)
                db.session.commit()
        return redirect(url_for('support.leavetype'))
    
    all_leavetypes = LeaveType.query.all()
    return render_template('auth/leavetype.html', all_leavetypes=all_leavetypes)