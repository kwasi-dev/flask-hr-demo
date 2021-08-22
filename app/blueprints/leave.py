from app.models import employee
import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for,request, jsonify
)

from app import db, bcrypt
from ..models import LeaveApproval, Department, LeaveType, User, Employee
from flask_login import login_required


bp = Blueprint('leave', __name__, url_prefix='/')


@bp.route('/leave', methods=["POST","GET"])
@login_required
def view_leave():
    if request.method == 'POST':
        formParams = request.form.keys()

        employee_id = request.form['employee_id']
        leave_type_id = request.form['leave_type_id']
        date_from = request.form['date_from']
        date_to = request.form['date_to']
        approved = 'is_approved' in formParams

        if (employee_id and leave_type_id and date_from and date_to):
            appr = LeaveApproval(
                employee_id=employee_id,
                type_id=leave_type_id,
                date_from=date_from,
                date_to=date_to,
                approved=approved,
            )
            db.session.add(appr)
            db.session.commit()
        return redirect(url_for('leave.view_leave'))

    all_leaves = LeaveApproval.query.all()
    leave_types = LeaveType.query.all()
    all_employees = Employee.query.all()
    
    return render_template('auth/leave_list.html', leaves=all_leaves, employees=all_employees, leave_types=leave_types)



@bp.route('/confirm-leave', methods=["POST"])
@login_required
def confirm_leave():
    leave_id = request.form['leave_id']
    appr = LeaveApproval.query.filter(LeaveApproval.id == leave_id).first()
    if (appr):
        appr.approved = True
        db.session.add(appr)
        db.session.commit()
    return redirect(url_for('leave.view_leave'))