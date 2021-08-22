from app import db
from sqlalchemy.orm import backref, relation, relationship

class Appraisal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'))
    appraisal_date = db.Column(db.Date())
    is_completed = db.Column(db.Boolean())

    employee = relationship("Employee", backref="appraisals")

    def __repr__(self):
        return f"<Appraisal Record:  ID: {self.id}>"
    
    def toJson(self):
        return {
            "id":self.id,
            "employee_id":self.employee_id,
            "appraisal_date":self.appraisal_date,
            "is_completed":self.is_completed,
        }