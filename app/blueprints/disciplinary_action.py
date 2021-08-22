from app.models import employee
import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for,request, jsonify
)

from app import db, bcrypt
from ..models import DisciplinaryAction, LeaveApproval, Department, LeaveType, User, Employee
from flask_login import login_required


bp = Blueprint('discipline', __name__, url_prefix='/')


@bp.route('/discipline', methods=["POST","GET"])
@login_required
def view_discipline():
    if request.method == 'POST':
        formParams = request.form.keys()

        employee_id = request.form['employee_id']
        date = request.form['date']
        reason = request.form['reason']

        if (employee_id and date and reason):
            req = DisciplinaryAction(
                employee_id=employee_id,
                date=date,
                reason=reason,
            )
            db.session.add(req)
            db.session.commit()
        return redirect(url_for('discipline.view_discipline'))

    all_actions = DisciplinaryAction.query.all()
    all_employees = Employee.query.all()
    
    return render_template('auth/discipline_list.html', all_actions=all_actions, employees=all_employees)



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