import flask_sqlalchemy
from werkzeug.security import generate_password_hash, check_password_hash


db = flask_sqlalchemy.SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(240), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    career = db.Column(db.String(120), nullable=False)
    semestre = db.Column(db.String(120), nullable=False)
    cursos = db.relationship('Curso', backref='user', lazy=True)
    def __repr__(self):
        return '<User %r>' % self.username
    def set_password(self, password):
        self.password = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password, password)
    def save(self):
        db.session.add(self)
        db.session.commit()
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    def update(self):
        db.session.commit()
    def generate_token(self):
        pass
class Curso(db.Model):
    __tablename__ = 'cursos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), unique=True, nullable=False)
    descripcion = db.Column(db.String(240), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    def __repr__(self):
        return '<Curso %r>' % self.nombre
    def save(self):
        db.session.add(self)
        db.session.commit()
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    def update(self):
        db.session.commit()
    def generate_token(self):
        pass