from app import db
from sqlalchemy.orm import backref, relationship

class LeaveApproval(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'),)
    type_id = db.Column(db.Integer, db.ForeignKey('leave_type.id'),)
    date_from = db.Column(db.Date())
    date_to = db.Column(db.Date())
    approved = db.Column(db.Boolean())

    employee = relationship("Employee", backref="leaveApprovals")
    leaveType = relationship("LeaveType", backref="leaveApprovals")


    def __repr__(self):
        return f"<LeaveApproval Record:  employee_id: {self.employee_id}>"
    
    def toJson(self):
        return {
            "id":self.id,
            "employee_id":self.employee_id,
            "type_id":self.type_id,
            "date_from":self.date_from,
            "date_to":self.date_to,
            "approved":self.approved,
        }

