from PIL import Image

from app.settings import EMOJI_DIR
from app.utils.files import get_file_paths


def get_emojies(size):
    emoji_paths = get_file_paths(EMOJI_DIR)
    emojies = []
    for path in emoji_paths:
        emoji = Image.open(path).resize((size, size), Image.LANCZOS)
        emojies.append(emoji)
    return emojies
