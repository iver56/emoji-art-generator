from PIL import Image

from app.settings import EMOJI_DIR
from app.utils.files import get_file_paths

emoji_size = 16

emoji_paths = get_file_paths(EMOJI_DIR)
emojies = []
for path in emoji_paths:
    emoji = Image.open(path).resize((emoji_size, emoji_size), Image.LANCZOS)
    emojies.append(emoji)
