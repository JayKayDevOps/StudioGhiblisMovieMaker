# Explanation of the Code

## Purpose
This code extends user-related functionalities in a Flask application. It includes routes for viewing user bookings, creating or updating user profiles, booking courses, and logging out. These enhancements integrate session management, robust error handling, and logging.

---

## **Modules and Imports**
- **`logging`**: Captures and formats log messages for debugging and monitoring.
- **`Blueprint`**: Organizes user-specific routes into a modular structure.
- **`db`**, **`Subscriptions`**, **`User`**, and **`Course`**: Database models for handling users, courses, and subscriptions.
- **`UserService`**: A service layer for user-related operations such as fetching data and bookings.

---

## **Logging Configuration**
- Configured to log messages at the `INFO`, `WARNING`, and `ERROR` levels.
- Log messages are outputted to `stdout` using `StreamHandler`.

---

## **Blueprint Definition**
- **`user_bp`**: A Flask Blueprint that groups all routes related to user functionalities.
- **`UserService()`**: A service object initialized to handle user-specific logic.

---

## **Routes Explained**

### **Dashboard**
- **`GET` Route**: Reserved for rendering the user dashboard.
- **Implementation**: Currently not implemented (`NotImplementedError`).

---

### **View Bookings**
- **`GET` Route**:
  - Retrieves the logged-in user’s bookings and user data using session information.
  - Renders `MyBookings.html` if the data is valid, or redirects to the homepage with an error message if no user is logged in or if bookings cannot be fetched.
- **Error Handling**: Ensures non-logged-in users are redirected with appropriate feedback using `flash`.

---

### **Update User**
- **`POST` Route**:
  - Updates user information based on form input.
  - Passwords are hashed if provided, and the user’s role is enforced as `'customer'`.
  - Calls `UserService.update_user()` for updating user details in the database.
- **Error Handling**:
  - Redirects with feedback if the user cannot be found or if there’s an error during the update process.
  - Logs unexpected exceptions for debugging.

---

### **Create User**
- **`POST` Route**:
  - Validates and creates a new user based on form input.
  - Enforces required fields like `first_name`, `second_name`, `email`, and `password`.
  - Calls `UserService.create_user()` to save the new user to the database.
- **Error Handling**:
  - Provides feedback for missing fields or unexpected errors using `flash`.

---

### **Logout**
- **`GET` Route**:
  - Clears the session to log the user out.
  - Renders the `Homepage.html` template.

---

### **Book Course**
- **`POST` Route**:
  - Books a specific course for the logged-in user by calling `UserService.book_course()`.
  - Provides feedback if the course is already booked.
- **Error Handling**: Logs errors and renders an error template for unexpected issues.

---

### **My Courses**
- **`GET` Route**:
  - Fetches and processes the logged-in user’s course bookings using `UserService`.
  - Currently not implemented (`NotImplementedError`).
- **Error Handling**: Ensures fallback behavior for unexpected errors.

---

## Key Features Highlighted
1. **Session Management**: Maintains user state using session variables (e.g., `user_id`).
2. **Error Handling**:
   - Graceful redirection and feedback for invalid operations.
   - Logging for diagnosing issues and tracking application behavior.
3. **Service Layer Integration**: Delegates operations like booking and profile management to `UserService`.
4. **Password Security**: Hashes user passwords for secure storage.

---

