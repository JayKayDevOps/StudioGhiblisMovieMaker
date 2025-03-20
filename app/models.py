from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model, UserMixin):
    """User table for customers and admins."""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255), nullable=False)    
    second_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum('customer', 'admin', name='user_role'), default='customer', nullable=False)

    def set_password(self, password):
        """Hashes password before storing it."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Checks password validity."""
        return check_password_hash(self.password_hash, password)


class Course(db.Model):
    """Table to store movie-making courses."""
    __tablename__ = 'courses'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    

class Module(db.Model):
    """Table to store movie-making modules."""
    __tablename__ = 'modules'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)


class CourseModule(db.Model):
    """Modules within each course."""
    __tablename__ = 'course_modules'

    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    module_id = db.Column(db.Integer, db.ForeignKey('modules.id'), nullable=False)

    course = db.relationship('Course', backref=db.backref('modules', lazy=True))
    module = db.relationship('Module', backref=db.backref('course_modules', lazy=True))


class Subscriptions(db.Model):
    """Stores course subscriptions by customers."""
    __tablename__ = 'subscriptions' 

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    special_requests = db.Column(db.Text, nullable=True)
    status = db.Column(
        db.Enum('pending', 'confirmed', 'cancelled', name='sub_status'),
        nullable=False,
        server_default='pending'  # ✅ Corrected Enum default
    )
    subscription_date = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())

    user = db.relationship('User', backref=db.backref('subscriptions', lazy=True))
    course = db.relationship('Course', backref=db.backref('subscriptions', lazy=True))
