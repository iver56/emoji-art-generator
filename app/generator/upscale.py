import argparse
import os

import joblib
from PIL import Image
from tqdm import tqdm

from app.generator.emoji import get_emojies
from app.settings import OUTPUT_DIR
from app.utils.argparse_sanity import positive_int
from app.utils.files import get_subfolders, get_file_paths


def generate_alpha_image_from_scratch(genotype, image_size, emojies):
    """
    Slower than generate_image_from_scratch, but has transparent background
    """
    image = Image.new(mode="RGBA", size=image_size, color=(255, 255, 255, 0))
    for i in tqdm(range(len(genotype))):
        x = genotype[i][1]
        y = genotype[i][2]
        emoji_index = genotype[i][0]
        if x == 0 and y == 0 and emoji_index == 0:
            continue
        emoji = emojies[emoji_index]
        canvas = Image.new(mode="RGBA", size=image_size, color=(255, 255, 255, 0))
        canvas.paste(emoji, box=(x, y), mask=emoji)
        image = Image.alpha_composite(image, canvas)
    return image


def upscale(args, selected_experiment_folder):
    target_image = Image.open(os.path.join(selected_experiment_folder, "target.png"))

    upscaling_factor = args.upscaling_factor
    original_emoji_size = (args.emoji_size, args.emoji_size)
    original_image_size = target_image.size

    upscaled_emoji_size = (
        original_emoji_size[0] * upscaling_factor,
        original_emoji_size[1] * upscaling_factor,
    )
    upscaled_image_size = (
        original_image_size[0] * upscaling_factor,
        original_image_size[1] * upscaling_factor,
    )

    upscaled_emojies = get_emojies(size=upscaled_emoji_size[0])

    stored_individual_paths = get_file_paths(
        selected_experiment_folder, file_extensions=("pkl",)
    )
    stored_individual_paths.sort(key=lambda f: f.name)
    best_stored_individual_path = stored_individual_paths[-1]
    genotype = joblib.load(best_stored_individual_path)
    genotype[:, 1] *= upscaling_factor  # x
    genotype[:, 2] *= upscaling_factor  # y

    image = generate_alpha_image_from_scratch(genotype, upscaled_image_size, upscaled_emojies)
    image.save(
        os.path.join(
            selected_experiment_folder, best_stored_individual_path.stem + "_upscaled.png"
        )
    )
    print("Done")


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument(
        "--emoji-size",
        dest="emoji_size",
        type=positive_int,
        required=False,
        default=16,
        help="Original emoji size (i.e. not the upscaled size)",
    )
    arg_parser.add_argument(
        "--experiment",
        dest="experiment",
        type=str,
        required=False,
        default=None,
        help="Refers to the experiment folder. If not provided, the upscaling procedure will be"
             "applied to all experiment folders.",
    )
    arg_parser.add_argument(
        "--upscaling-factor",
        dest="upscaling_factor",
        type=positive_int,
        required=False,
        default=8,
    )
    args = arg_parser.parse_args()

    if args.experiment is None:
        experiment_folders = get_subfolders(OUTPUT_DIR)
        for experiment_folder in experiment_folders:
            print(experiment_folder)
            upscale(args, experiment_folder)
    else:
        selected_experiment_folder = OUTPUT_DIR / args.experiment
        upscale(args, selected_experiment_folder)
