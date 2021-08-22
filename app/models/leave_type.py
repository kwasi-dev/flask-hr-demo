from app import db
from sqlalchemy.orm import backref

class LeaveType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    leave_type = db.Column(db.String())

    def __repr__(self):
        return f"<LeaveType Record:  Name: {self.leave_type}>"
    
    def toJson(self):
        return {
            "id":self.id,
            "leave_type":self.leave_type,
        }