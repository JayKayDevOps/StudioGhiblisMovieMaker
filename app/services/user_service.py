
from app.models import db, Subscriptions, Course

class UserService:
    def get_user_bookings(self, user_id):
        """Fetch all bookings made by a specific user."""
        try:
            bookings = db.session.query(
                Subscriptions.id,
                Course.name.label("course_name"),
                Subscriptions.status,
                Subscriptions.subscription_date
            ).join(Course, Subscriptions.course_id == Course.id)\
             .filter(Subscriptions.user_id == user_id)\
             .all()

            return [
                {
                    "booking_id": b.id,
                    "course_name": b.course_name,
                    "status": b.status,
                    "subscription_date": b.subscription_date.strftime("%Y-%m-%d %H:%M:%S")
                }
                for b in bookings
            ]
        except Exception as e:
            print(f"❌ Error fetching user bookings: {e}")
            return []

    def book_course(self, user_id, course_id, special_requests=None):
        """Create a course subscription for a user."""
        try:
            # Prevent duplicate booking
            existing = db.session.query(Subscriptions).filter_by(
                user_id=user_id, course_id=course_id
            ).first()
            if existing:
                return False  # Already booked

            booking = Subscriptions(
                user_id=user_id,
                course_id=course_id,
                special_requests=special_requests or "",
                status="pending"
            )
            db.session.add(booking)
            db.session.commit()
            return True
        except Exception as e:
            print(f"❌ Error booking course: {e}")
            return False