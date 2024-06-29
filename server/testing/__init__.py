# tests/__init__.py

import logging

# Enable SQLAlchemy logging to debug mapper configuration
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

# Optionally, you may also set up other test utilities or fixtures here
