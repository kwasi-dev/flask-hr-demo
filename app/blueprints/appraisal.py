from app.models import employee
import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for,request, jsonify
)

from app import db, bcrypt
from ..models import Appraisal, Department, User, Employee
from flask_login import login_required


bp = Blueprint('appraisal', __name__, url_prefix='/')


@bp.route('/appraisal', methods=["POST","GET"])
@login_required
def view_appraisal():
    if request.method == 'POST':
        formParams = request.form.keys()

        employee_id = request.form['employee_id']
        appraisal_date = request.form['appraisal_date']
        is_complete = 'is_complete' in formParams

        if (employee_id and appraisal_date):
            appr = Appraisal(
                employee_id=employee_id,
                appraisal_date=appraisal_date,
                is_completed=is_complete,
            )
            db.session.add(appr)
            db.session.commit()
        return redirect(url_for('appraisal.view_appraisal'))

    all_appraisals = Appraisal.query.all()
    all_employees = Employee.query.all()
    
    return render_template('auth/appraisal_list.html', appraisals=all_appraisals, employees=all_employees)



@bp.route('/confirm-appraisal', methods=["POST"])
@login_required
def confirm_appraisal():
    appraisal_id = request.form['appraisal_id']
    appr = Appraisal.query.filter(Appraisal.id == appraisal_id).first()
    if (appr):
        appr.is_completed = True
        db.session.add(appr)
        db.session.commit()
    return redirect(url_for('appraisal.view_appraisal'))