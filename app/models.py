from app import db

class Login(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return "<User {}>".format(self.username)
    
class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    user_id = db.Column(db.Integer, db.ForeignKey("login.id"))
    github = db.Column(db.String(128))
    skills = db.Column(db.String(1000))
    interests = db.Column(db.String(1000))

    def __repr__(self):
        return "Commited"