import argparse
import os
import uuid

import arrow as arrow
from PIL import Image

from app.generator.emoji import get_emojies
from app.settings import TARGET_IMAGES_DIR, OUTPUT_DIR
from app.utils.argparse_sanity import positive_int

if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument(
        "--target",
        dest="target",
        type=str,
        help="Filename of target image. Should reside in data/target_images/",
        required=False,
        default="sunglasses.png",
    )
    arg_parser.add_argument(
        '--emoji-size',
        dest='emoji_size',
        type=positive_int,
        required=False,
        default=16
    )
    args = arg_parser.parse_args()

    experiment_id = "{}_{}".format(
        arrow.utcnow().format("YYYY-MM-DDTHHmm"), uuid.uuid4()
    )
    target_image = Image.open(TARGET_IMAGES_DIR / args.target).convert("RGB")

    emojies = get_emojies(args.emoji_size)

    os.makedirs(OUTPUT_DIR / experiment_id, exist_ok=True)

    canvas = Image.new(
        mode=target_image.mode,
        size=target_image.size,
        color=(255, 255, 255),
    )
