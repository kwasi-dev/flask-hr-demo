from app import db, bcrypt
from sqlalchemy.orm import backref,relationship

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'),)

    email = db.Column(db.String())
    password = db.Column(db.String())
    authenticated = db.Column(db.Boolean, default=False)
    employee = relationship("Employee", backref="user")

    def __repr__(self):
        return f"<User Record:  Name: {self.department_name}>"
    
    def toJson(self):
        return {
            "id":self.id,
            "email":self.emp_type,
        }

    def __init__(self, email, password):
        self.email = email
        self.password = bcrypt.generate_password_hash(password).decode('UTF-8')

    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.email

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False