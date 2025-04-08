# Explanation of the Module

## Purpose
This module provides the **service layer** for public-related database operations in a Flask application. It is designed to fetch course data, including associated modules, from the database, and structures the data for use in the frontend. It ensures separation between application logic and data access.

---

## **Modules and Imports**
- **`logging`**: Configured for tracking and debugging operations within the service.
- **`db`**, **`Subscriptions`**, **`User`**, **`Course`**, **`CourseModule`**, **`Module`**:
  - Database models representing courses, users, subscriptions, modules, and their mappings.
- **`joinedload` (SQLAlchemy)**:
  - Used for eager loading of related entities to improve query performance.

---

## **Logging Configuration**
- Configured using `logging.basicConfig()` to log messages at the `INFO` level or higher.
- Log format includes timestamps, log levels, and descriptive messages.
- Utilized throughout the service to log key actions and handle errors.

---

## **PublicService Class**
### Overview
The `PublicService` class encapsulates logic for fetching and structuring public-facing course data. It acts as the mediator between the database models and the application frontend.

### **Methods Explained**

#### **Fetch Course Details**
**`get_all_course_details()`**
- **Purpose**: Fetches all courses from the database along with their associated modules.
- **Implementation**:
  - Queries the `Course` model using SQLAlchemy's ORM.
  - Utilizes `joinedload` to eagerly fetch related `CourseModule` and `Module` entities.
  - Structures the result as a list of dictionaries for easier use in the frontend.
- **Output**: List of dictionaries, where each dictionary contains:
  - `course_id`: ID of the course.
  - `course_name`: Name of the course.
  - `course_description`: Description of the course.
  - `course_price`: Price of the course.
  - `modules`: List of associated modules with details like:
    - `module_id`: ID of the module.
    - `module_title`: Title of the module.
    - `module_description`: Description of the module.
- **Error Handling**:
  - Logs an error message if the query fails.
  - Raises a `RuntimeError` to propagate the issue to higher levels of the application.

---

## **Key Features**
1. **Eager Loading**:
   - Optimizes query performance by fetching related entities (`CourseModule`, `Module`) in a single operation.
2. **Structured Data**:
   - Returns course details in a format easily consumed by frontend components.
3. **Error Handling**:
   - Provides robust exception management and descriptive logging for debugging issues.

---
