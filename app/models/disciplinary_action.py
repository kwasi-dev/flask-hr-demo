from app import db
from sqlalchemy.orm import backref, relationship

class DisciplinaryAction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'))

    reason = db.Column(db.String())
    date = db.Column(db.Date())

    employee = relationship("Employee", backref="disciplinaryActions")

    def __repr__(self):
        return f"<DisciplinaryAction Record:  Employee ID: {self.employee_id}>"
    
    def toJson(self):
        return {
            "id":self.id,
            "employee_id":self.emp_type,
            "reason":self.reason,
            "date":self.date,
        }