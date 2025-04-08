# Explanation of the Module

## Purpose
This module implements a robust service layer for admin-related operations in a Flask application. It provides functionality to manage bookings, users, courses, and course modules through database queries and transactions. It ensures separation of concerns by centralizing database logic away from route handlers.

---

## **Modules and Imports**
- **`logging`**: Configures detailed logging for operational insights and debugging.
- **`db`**, **`Subscriptions`**, **`User`**, **`Course`**, **`CourseModule`**, **`Module`**:
  - Database models for managing subscriptions, users, courses, and their associated modules.
- **`SQLAlchemyError`**: Captures exceptions raised during database operations.

---

## **Logging Configuration**
- Configured with `logging.basicConfig()` for capturing messages at `INFO` or higher levels.
- Log format includes timestamps, log levels, and message content for ease of debugging.
- Used extensively throughout the module to track method execution, errors, and results.

---

## **AdminService Class**
This class acts as the **service layer** for admin-specific functionality, handling various database-related operations for courses, bookings, and users.

### **Initialization**
**`__init__(self, db_session=None)`**
- Accepts an optional `db_session` for dependency injection, facilitating easier testing.

---

## **Methods Explained**

### **Fetch Data**
#### `get_all_bookings()`
- **Purpose**: Fetches all course bookings with user and course details.
- **Output**: List of dictionaries containing booking data (e.g., `user_name`, `course_name`, `status`).
- **Error Handling**: Catches exceptions, logs detailed errors, and raises `RuntimeError`.

#### `get_all_users()`
- **Purpose**: Retrieves all users for the admin panel.
- **Output**: List of dictionaries with user details (`full_name`, `email`, `role`, etc.).
- **Error Handling**: Similar to `get_all_bookings()`.

#### `get_all_course_details()`
- **Purpose**: Retrieves all courses and their associated modules in a structured format.
- **Output**: List of dictionaries, where each course includes details of its modules.
- **Error Handling**: Logs and handles exceptions during database operations.

#### `get_bookings_by_course(course_id)`
- **Purpose**: Fetches bookings specific to a given course.
- **Output**: List of dictionaries, similar to `get_all_bookings()`, but filtered by `course_id`.
- **Error Handling**: Logs failures and raises a `RuntimeError` for external handling.

#### `get_all_courses()`
- **Purpose**: Fetches all available courses sorted by their IDs in descending order.
- **Output**: List of course dictionaries with basic details (`id`, `name`).
- **Error Handling**: Logs database and unexpected errors, returning an empty list on failure.

#### `get_existing_course()`
- **Purpose**: Checks whether any course exists in the database.
- **Output**: Returns the first course found or `None` if the database is empty.
- **Error Handling**: Logs errors during the query process for visibility.

---

### **Update Data**
#### `update_booking(booking_id, **kwargs)`
- **Purpose**: Dynamically updates multiple fields of a specific booking based on keyword arguments.
- **Implementation**:
  - Uses `get_booking()` to fetch the booking.
  - Iterates over `kwargs` and updates fields that exist in the model.
  - Commits changes to the database.
- **Error Handling**: Handles failures gracefully and ensures data consistency.

#### `update_booking_status(booking_id, new_status)`
- **Purpose**: Updates the status of a specific booking.
- **Error Handling**:
  - Ensures the booking exists before attempting updates.
  - Logs detailed errors for better debugging.

#### `update_course(course_id, name=None, description=None, price=None)`
- **Purpose**: Updates course details such as `name`, `description`, and `price`.
- **Error Handling**:
  - Ensures course existence before applying changes.
  - Logs detailed exceptions and rolls back the transaction on failure.

---

### **Delete Data**
#### `delete_booking(booking_id)`
- **Purpose**: Deletes a specific booking from the database.
- **Implementation**:
  - Validates booking existence using `get_booking()`.
  - Deletes the booking and commits changes to the database.
- **Error Handling**: Logs warnings if the booking is not found and handles unexpected exceptions.

#### `delete_course(course_id)`
- **Purpose**: Deletes a course along with its associated `CourseModule` mappings.
- **Error Handling**:
  - Ensures the course exists before deletion.
  - Rolls back changes and logs detailed errors on failure.

---

### **Create Data**
#### `create_course(name, description, price)`
- **Purpose**: Adds a new course to the database with the given attributes.
- **Key Features**:
  - Automatically generates the course ID using `flush()`.
  - Ensures data integrity by rolling back on failure.
- **Error Handling**: Logs all steps for traceability and gracefully handles exceptions.

#### `add_course(course_data)`
- **Purpose**: Adds a course using a dictionary of attributes (`name`, `description`, `price`).
- **Key Features**:
  - Similar to `create_course()` but designed for bulk insertion scenarios.
  - Ensures atomicity by rolling back on failure.

#### `add_modules_to_course(course_id, module_data)`
- **Purpose**: Adds modules to a specific course and creates `CourseModule` mappings.
- **Implementation**:
  - Validates the course's existence.
  - Iterates over the provided module data to create new `Module` records.
  - Creates a `CourseModule` mapping for each module.
  - Commits all changes in a single transaction.
- **Error Handling**:
  - Rolls back changes on failure and logs the error for debugging.

---

### **Helper Methods**
#### `get_booking(booking_id)`
- **Purpose**: Retrieves a booking by its ID using the session object.
- **Error Handling**: Raises an exception if the booking is not found.

---

## **Key Features**
1. **Service Layer Abstraction**: Encapsulates admin-specific operations, improving code modularity and testability.
2. **Robust Error Handling**:
   - Logs warnings, errors, and debugging information for all methods.
   - Ensures rollback of database transactions on failure.
3. **Database Efficiency**:
   - Uses eager loading (`joinedload`) to optimize query performance.
   - Employs `flush()` for generating IDs prior to commits.
4. **Extensibility**:
   - Designed to support future features like filtering, sorting, or role-based access control.

---



