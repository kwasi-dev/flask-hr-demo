import datetime
from app import db
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import backref
from sqlalchemy.orm import relationship
from datetime import datetime
class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    emp_type = db.Column(db.String())
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'))
    f_name = db.Column(db.String())
    l_name = db.Column(db.String())
    dob = db.Column(db.Date())
    addr_line_1 = db.Column(db.String())
    add_line_2 = db.Column(db.String())
    city = db.Column(db.String())
    phone = db.Column(db.String())
    location = db.Column(db.String())

    department = relationship("Department", backref="employee")


    def __repr__(self):
        return f"<Employee Record:  Name: {self.f_name} {self.l_name}>"
    
    def toJson(self):
        return {
            "id":self.id,
            "emp_type":self.emp_type,
            "department_id":self.department_id,
            "department":self.department,
            "f_name":self.f_name,
            "l_name":self.l_name,
            "dob":self.dob,
            "addr_line_1":self.addr_line_1,
            "add_line_2":self.add_line_2,
            "city":self.city,
            "phone":self.phone,
            "location":self.location,
        }

    def attendance(self):
        from . import EmployeeSwipeCard, Timesheet

        att = "Absent"

        # Being 'present' is defined as having an open timesheet record for the current swipecard that i have
        my_swipecard = EmployeeSwipeCard.query.filter_by(employee_id=self.id).first()

        if my_swipecard:
            swipecard_id = my_swipecard.swipecard_id
            now = datetime.now()
            open_timesheet = Timesheet.query.filter(Timesheet.swipecard_id == swipecard_id).filter(Timesheet.time_out >= now) .filter(Timesheet.time_in <= now) .first()
            if open_timesheet:
                att = "Present"
        return att
