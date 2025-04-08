# Code Explanation: AWS Secrets Manager and Flask Configuration Classes

This document explains the provided Python code, which includes:
1. A function to retrieve secrets from AWS Secrets Manager.
2. Configuration classes for Flask applications.

---

## 1. AWS Secrets Manager: `get_secret` Function

### Purpose:
The `get_secret` function retrieves secrets stored in AWS Secrets Manager.

### Arguments:
- **`secret_name`**: Name of the secret to retrieve.

### Returns:
- **`dict`**: Parsed secret retrieved from AWS Secrets Manager.

### Workflow:
1. Establishes a session using `boto3`.
2. Creates a client for AWS Secrets Manager.
3. Retrieves the secret value using `get_secret_value`.
4. Parses the secret JSON string into a Python dictionary.
5. Handles exceptions and raises runtime errors when retrieval fails.

---

## 2. Flask Configuration Classes

### Purpose:
Define configuration settings for Flask applications, depending on the environment (Development, Production, Testing).

### Common Configuration Attributes (`Config`):
- **`SECRET_KEY`**: Security key for Flask sessions.
- **`SQLALCHEMY_TRACK_MODIFICATIONS`**: Disables SQLAlchemy notifications.
- **`CREATE_DB`**: Indicates whether the database should be created.
- **`SESSION_PERMANENT`**: Specifies if sessions are permanent.
- **`SESSION_USE_SIGNER`**: Enables session signing for security.

### Specific Configurations:

#### A. Development Configuration (`DevelopmentConfig`)
- Enables debugging and database creation.
- Uses local PostgreSQL database connection details.
- **Example Attributes**:
  - `DB_USER`: `"postgres"`
  - `DB_HOST`: `"localhost"`
  - `DB_NAME`: `"moviemaking_db"`

#### B. Development Configuration (AWS-hosted) (`DevelopmentConfig2`)
- Similar to `DevelopmentConfig`, but retrieves credentials and database information from environment variables using `os.getenv`.
- Masks sensitive details (e.g., database password) in logs.

#### C. Production Configuration (`ProductionConfig`)
- Disables debugging and database creation for security.
- Uses environment variables to set database connection details.

#### D. Testing Configuration (`TestingConfig`)
- Enables testing mode.
- Uses an in-memory SQLite database for tests.
- Disables CSRF protection for convenience during testing.

---

## Dynamic Loading of Configuration

### Workflow:
- Reads the environment variable `FLASK_ENV` to determine the current environment.
- Defaults to `DevelopmentConfig2` if the environment is not specified.
- Prints the name of the selected configuration class.

### Example:
```python
flask_env = os.getenv("FLASK_ENV", "development2")
selected_config = config.get(flask_env, DevelopmentConfig2)
print(f"Using configuration: {selected_config.__name__}")
