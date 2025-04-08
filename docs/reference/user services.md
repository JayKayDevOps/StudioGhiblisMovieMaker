# Explanation of the Module

## Purpose
This module defines the **UserService** class, which serves as a service layer for user-related database operations in a Flask application. The service covers functionalities such as managing user data, creating new users, updating user details or passwords, fetching course details, and booking courses.

---

## **Modules and Imports**
- **`logging`**: Configured for tracking and debugging operations.
- **`db`**, **`Subscriptions`**, **`User`**, **`Course`**, **`CourseModule`**, **`Module`**:
  - Database models representing users, courses, subscriptions, modules, and their relationships.
- **`joinedload` (SQLAlchemy)**:
  - Optimizes query performance by eagerly fetching related entities.
- **`IntegrityError`**:
  - Handles database integrity issues like duplicate email constraints.

---

## **Logging Configuration**
- Configured using `logging.basicConfig()` to log messages at the `INFO` level or higher.
- Logs include timestamps, severity levels, and descriptive messages for debugging purposes.

---

## **UserService Class**

### **Overview**
The `UserService` class abstracts user-related logic, offering methods for fetching user details, managing bookings, and updating user data securely. It promotes clean separation of application layers.

---

### **Methods Explained**

#### **Fetch Course Details**
**`get_all_course_details()`**
- **Purpose**: Fetches all courses from the database along with their associated modules.
- **Implementation**:
  - Eagerly loads related entities like `CourseModule` and `Module` to optimize query performance.
  - Returns the result as a list of dictionaries, each containing:
    - `course_id`: The ID of the course.
    - `course_name`: Name of the course.
    - `course_description`: Description of the course.
    - `course_price`: Price of the course.
    - `modules`: List of associated modules with details like `module_title` and `module_description`.
- **Error Handling**: Logs errors during the query execution and raises a `RuntimeError` to propagate the issue.

---

#### **Fetch User Data**
**`get_user_data(user_id)`**
- **Purpose**: Fetches user data from the database using the provided user ID.
- **Output**: Returns a user object if found, or `None` if no data exists.
- **Error Handling**:
  - Logs warnings when no user is found.
  - Catches and logs unexpected exceptions with detailed traces.

---

#### **Update User**
**`update_user(user_id, **kwargs)`**
- **Purpose**: Updates a user's details dynamically based on provided keyword arguments.
- **Implementation**:
  - Iterates through `kwargs` to update fields in the `User` model.
  - Commits the changes to the database.
- **Output**: Returns a tuple `(success: bool, message: str)` indicating the result.
- **Error Handling**:
  - Rolls back changes on failure and logs detailed error messages.

---

#### **Create User**
**`create_user(password, **kwargs)`**
- **Purpose**: Creates a new user record in the database.
- **Implementation**:
  - Hashes the raw password using the `set_password()` method in the `User` model.
  - Adds the user to the database and commits the changes.
- **Output**: Returns a tuple `(success: bool, message: str)` indicating the result.
- **Error Handling**:
  - Detects and handles integrity errors (e.g., duplicate email).
  - Logs other unexpected exceptions and ensures data rollback on failure.

---

#### **Update Password**
**`update_password(user_id, new_password)`**
- **Purpose**: Updates a user's password.
- **Implementation**:
  - Hashes the new password using `generate_password_hash` before storing it in the database.
  - Commits the updated password securely.
- **Output**: Returns a tuple `(success: bool, message: str)` indicating the result.
- **Error Handling**:
  - Rolls back changes on failure.
  - Logs errors and ensures user feedback for unsuccessful attempts.

---

#### **Fetch User Bookings**
**`get_user_bookings(user_id)`**
- **Purpose**: Retrieves all bookings made by a specific user.
- **Implementation**:
  - Joins the `Subscriptions` and `Course` tables to fetch related course details.
  - Formats results as a list of dictionaries with fields like:
    - `booking_id`: The ID of the booking.
    - `course_name`: The name of the booked course.
    - `status`: The current status of the booking.
    - `subscription_date`: The date the booking was made.
- **Error Handling**:
  - Logs errors during query execution.
  - Returns an empty list if any issues arise.

---

#### **Create Course Booking**
**`book_course(user_id, course_id, special_requests=None)`**
- **Purpose**: Creates a new booking for a user in a specific course.
- **Implementation**:
  - Checks for existing bookings to prevent duplicate entries.
  - Adds a new record to the `Subscriptions` table with a default status of "pending."
- **Output**: Returns `True` for successful bookings, `False` for duplicates or failures.
- **Error Handling**:
  - Catches and logs errors to ensure the operation fails gracefully.

---

#### **Fetch All Bookings**
**`get_all_bookings(user_id)`**
- **Purpose**: Fetches all course bookings for a specific user, including user and course details.
- **Implementation**:
  - Joins the `User`, `Course`, and `Subscriptions` tables to retrieve comprehensive booking data.
  - Formats the result as a list of dictionaries with details like:
    - `user_name`: User's full name.
    - `user_email`: User's email address.
    - `course_name`: Booked course name.
    - `status`: Booking status.
    - `special_requests`: Any special notes added by the user.
- **Error Handling**:
  - Logs database and query errors.
  - Raises a `RuntimeError` when the operation fails.

---

## **Key Features**
1. **Dynamic Data Handling**:
   - Supports dynamic field updates for users using keyword arguments.
   - Provides formatted data structures for easy consumption by frontend applications.
2. **Secure Operations**:
   - Hashes passwords before storing them in the database.
   - Prevents duplicate bookings to ensure database integrity.
3. **Comprehensive Logging**:
   - Tracks actions, errors, and query results with detailed log entries.
   - Utilizes different log levels (`INFO`, `WARNING`, `ERROR`) for appropriate categorization.
4. **Error Management**:
   - Handles database errors gracefully with rollback mechanisms.
   - Provides descriptive error messages for debugging and user feedback.

---
