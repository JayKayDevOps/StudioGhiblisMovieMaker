import pytest
from flask import Flask
from app.models import User, Course, Subscriptions, db, CourseModule, Module
from app.services.admin_service import AdminService
from app.services.user_service import UserService


def test_course_subscription_and_management_flow(client, app):
    """
    Integration test verifying the end-to-end flow of:
    1. User registration
    2. Course creation by admin
    3. User booking a course
    4. Admin confirming the booking
    5. User viewing their confirmed booking
    6. Admin updating course details
    7. Admin cancelling the booking
    """
    with app.app_context():
        # Create service instances
        admin_service = AdminService()
        user_service = UserService()

        # 1. Create admin and regular user
        admin = User(
            first_name="Admin",
            second_name="User",
            email="admin@studioghibli.com",
            role="admin"
        )
        admin.set_password("adminpassword")

        customer = User(
            first_name="Test",
            second_name="Customer",
            email="customer@example.com",
            role="customer"
        )
        customer.set_password("customerpassword")

        # Save users to database
        db.session.add_all([admin, customer])
        db.session.commit()

        # 2. Admin creates a new course - returns course_id (integer)
        new_course_id = admin_service.create_course(
            name="Animation Fundamentals",
            description="Learn the basics of animation in Ghibli style",
            price=199.99
        )

        # 3. Customer books a course - returns boolean
        booking_success = user_service.book_course(
            user_id=customer.id,
            course_id=new_course_id,
            special_requests="I'd like extra material on character design"
        )

        # Verify booking was successful
        assert booking_success is True

        # Fetch the booking from the database
        booking = db.session.query(Subscriptions).filter_by(
            user_id=customer.id,
            course_id=new_course_id
        ).first()

        # Ensure we found the booking
        assert booking is not None
        assert booking.status == "pending"

        # 4. Admin updates booking status to confirmed
        updated_booking = admin_service.update_booking_status(
            booking_id=booking.id,
            new_status="confirmed"
        )

        # Verify booking status was updated
        assert updated_booking == True

        # 5. Customer views their bookings
        customer_bookings = user_service.get_user_bookings(customer.id)
        assert len(customer_bookings) == 1
        assert customer_bookings[0]['booking_id'] == booking.id
        assert customer_bookings[0]['status'] == "confirmed"

        # 6. Admin updates course details
        updated_course = admin_service.update_course(
            course_id=new_course_id,
            description="Learn the fundamentals of animation in Studio Ghibli style with expert instructors",
            price=249.99
        )

        # Verify course was updated
        assert updated_course == True


        # 7. Admin cancels the booking
        cancelled_booking = admin_service.update_booking_status(
            booking_id=booking.id,
            new_status="cancelled"
        )

        # Verify booking was cancelled
        assert cancelled_booking == True

        # Check that the database reflects all changes
        final_booking = db.session.get(Subscriptions, booking.id)
        assert final_booking.status == "cancelled"

        final_course = db.session.get(Course, new_course_id)
        assert final_course.price == 249.99