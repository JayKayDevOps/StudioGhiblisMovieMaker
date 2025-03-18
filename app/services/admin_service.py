from models import db, Subscription, User, Course

class AdminService:
    """Service layer for admin-related database operations."""

    def get_all_bookings(self):
        """Fetch all course bookings with user and course details."""
        print("Getting bookings from the database...")
        try:
            bookings = db.session.query(
                Subscription.id,
                User.first_name,
                User.second_name,
                User.email,
                Course.name.label("course_name"),
                Subscription.status,
                Subscription.subscription_date
            ).join(User, Subscription.user_id == User.id)\
             .join(Course, Subscription.course_id == Course.id)\
             .all()

            # Convert to a list of dictionaries
            print(bookings)
            return [
                {
                    "booking_id": b.id,
                    "user_name": f"{b.first_name} {b.second_name}",
                    "user_email": b.email,
                    "course_name": b.course_name,
                    "status": b.status,
                    "subscription_date": b.subscription_date.strftime("%Y-%m-%d %H:%M:%S")
                }
                for b in bookings
            ]

        except Exception as e:
            print(f"❌ Error fetching bookings: {e}")
            raise e  # Raise the error so the route can handle it

    def get_all_users(self):
        """Fetch all users for the admin panel."""
        try:
            users = db.session.query(
                User.id,
                User.first_name,
                User.second_name,
                User.email,
                User.role
            ).all()

            # Convert query results to a list of dictionaries
            return [
                {
                    "user_id": u.id,
                    "full_name": f"{u.first_name} {u.second_name}",
                    "email": u.email,
                    "role": u.role
                }
                for u in users
            ]

        except Exception as e:
            print(f"❌ Error fetching users: {e}")
            raise e  # Raise error to be handled by the route