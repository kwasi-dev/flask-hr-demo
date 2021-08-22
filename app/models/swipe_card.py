from app import db
from sqlalchemy.orm import backref

class SwipeCard(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    rfid_identifier = db.Column(db.String())
    is_lost = db.Column(db.Boolean())

    def __repr__(self):
        return f"<User SwipeCard:  identifier: {self.rfid_identifier}>"
    
    def toJson(self):
        return {
            "id":self.id,
            "rfid_identifier":self.rfid_identifier,
            "is_lost":self.is_lost,
        }