from app.models import department
import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for,request, jsonify
)
from werkzeug.security import check_password_hash, generate_password_hash
from hashlib import md5
from flask_jwt_extended import create_access_token, unset_jwt_cookies

from app import db, bcrypt
from ..models import Department, User, Employee
from flask_login import login_required


bp = Blueprint('employees', __name__, url_prefix='/')


@bp.route('/employee', methods=["POST","GET"])
@login_required
def view_employee():
    if request.method == 'POST':
        f_name = request.form['f_name']
        l_name = request.form['l_name']
        dob = request.form['dob']
        addr_line_1 = request.form['addr_line_1']
        add_line_2 = request.form['add_line_2']
        city = request.form['city']
        phone = request.form['phone']
        location = request.form['location']
        emp_type = request.form['emp_type']
        department_id = request.form['department_id']
        
        if (f_name and l_name and dob and addr_line_1 and city and phone and location and emp_type and department_id):
            emp = Employee(f_name = f_name, l_name = l_name, dob = dob, addr_line_1 = addr_line_1, add_line_2 = add_line_2, city = city, phone = phone, location = location, emp_type = emp_type, department_id = department_id)
            db.session.add(emp)
            db.session.commit()

    all_employees = Employee.query.all()
    all_departments = Department.query.all()

    return render_template('auth/employee_list.html', employees=all_employees, departments=all_departments)
