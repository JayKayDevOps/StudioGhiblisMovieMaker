from app import db


class MovieMakerBookingDB(db.Model):

    __tablename__ = "StudioGhiblisMovieMaker"

    mm_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    course = db.Column(db.String(120), nullable=False)