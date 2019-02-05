import os
from pathlib import Path

BASE_DIR = Path(
    os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
)
DATA_DIR = BASE_DIR / "data"
EMOJI_DIR = DATA_DIR / "emoji"
TARGET_IMAGES_DIR = DATA_DIR / "target_images"
OUTPUT_DIR = DATA_DIR / "output"


# If local.py is available, Load those local settings that may override the defaults above.
# This is be useful because each computer may have the files stored in different locations.
try:
    from app.settings.local import *
except ImportError:
    pass
