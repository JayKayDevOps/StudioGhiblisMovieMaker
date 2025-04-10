import os
import logging
from app import create_app

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Create Flask App
app = create_app()

# This block is only used in development mode!
if __name__ == "__main__":
    logger.info("Starting the Flask app in development mode...")
    app.run(host="0.0.0.0", port=5000, debug=True)