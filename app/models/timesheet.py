from app import db
from sqlalchemy.orm import backref, relationship

class Timesheet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    swipecard_id = db.Column(db.Integer, db.ForeignKey('swipe_card.id'),)
    time_in = db.Column(db.DateTime())
    time_out = db.Column(db.DateTime(),     )
    total_time = db.Column(db.Integer)

    swipecard = relationship("SwipeCard", backref="timesheets")

    def __repr__(self):
        return f"<Timesheet Record:  id: {self.id}>"
    
    def toJson(self):
        return {
            "id":self.id,
            "swipecard_id":self.swipecard_id,
            "time_in":self.time_in,
            "time_out":self.time_out,
            "total_time":self.total_time,
        }
    
    def overtime(self):
        emp_type = self.swipecard.empSwipeCard[0].employee.emp_type
        if emp_type == 'clerical':
            return 'N/A'

        # For demonstration, the overtime hours is half of what the user worked
        hours_worked = (self.time_out - self.time_in).total_seconds() / 60.0 / 60.0
        overtime =  hours_worked - 12 if hours_worked > 12 else 0
        return "{:.2f} hours".format(overtime)

    