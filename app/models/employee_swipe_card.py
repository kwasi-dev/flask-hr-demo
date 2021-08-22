from app import db
from sqlalchemy.orm import backref, relationship

class EmployeeSwipeCard(db.Model):
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), primary_key=True)
    swipecard_id = db.Column(db.Integer, db.ForeignKey('swipe_card.id'), primary_key=True)
    issue_date = db.Column(db.Date())

    swipecard = relationship("SwipeCard", backref="empSwipeCard")
    employee = relationship("Employee", backref="empSwipeCard")

    def __repr__(self):
        return f"<User EmployeeSwipeCard:  empid: {self.employee_id}>"
    
    def toJson(self):
        return {
            "id":self.id,
            "employee_id":self.employee_id,
            "swipecard_id":self.swipecard_id,
            "issue_date":self.issue_date,
        }