from app import db
from sqlalchemy.orm import backref

class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    department_name = db.Column(db.String())

    def __repr__(self):
        return f"<Department Record:  Name: {self.department_name}>"
    
    def toJson(self):
        return {
            "id":self.id,
            "emp_type":self.emp_type,
            "department_name":self.department_name,
        }