import argparse
import json
import os
import shutil

import joblib
import numpy as np
from PIL import Image

from app.settings import OUTPUT_DIR, EMOJI_DIR
from app.utils.argparse_sanity import positive_int
from app.utils.files import get_subfolders, get_file_paths

if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument(
        "--emoji-size", dest="emoji_size", type=positive_int, required=False, default=16
    )
    arg_parser.add_argument(
        "--experiment",
        dest="experiment",
        type=str,
        required=False,
        default=None,
        help="Refers to the experiment folder. If not provided, the most recent experiment is"
             " used.",
    )
    arg_parser.add_argument(
        "--upscaling-factor",
        dest="upscaling_factor",
        type=positive_int,
        required=False,
        default=8,
    )
    args = arg_parser.parse_args()

    upscaling_factor = args.upscaling_factor
    original_emoji_size = (args.emoji_size, args.emoji_size)

    if args.experiment is None:
        experiment_folders = get_subfolders(OUTPUT_DIR)
        experiment_folders.sort(key=lambda f: f.name)
        selected_experiment_folder = experiment_folders[-1]
    else:
        selected_experiment_folder = OUTPUT_DIR / args.experiment

    target_image = Image.open(os.path.join(selected_experiment_folder, "target.png"))
    
    original_image_size = target_image.size

    upscaled_emoji_size = (
        original_emoji_size[0] * upscaling_factor,
        original_emoji_size[1] * upscaling_factor,
    )
    upscaled_image_size = (
        original_image_size[0] * upscaling_factor,
        original_image_size[1] * upscaling_factor,
    )

    emoji_paths = get_file_paths(EMOJI_DIR)

    stored_individual_paths = get_file_paths(
        selected_experiment_folder, file_extensions=("pkl",)
    )
    stored_individual_paths.sort(key=lambda f: f.name)
    best_stored_individual_path = stored_individual_paths[-1]
    genotype = joblib.load(best_stored_individual_path)
    genotype[:, 1] *= upscaling_factor  # x
    genotype[:, 2] *= upscaling_factor  # y

    used_emoji_ids = set()
    tiles = []
    for i in range(len(genotype)):
        if np.sum(genotype[i]) == 0:
            continue

        used_emoji_ids.add(int(genotype[i, 0]))
        tiles.append(
            {
                "emoji_id": int(genotype[i, 0]),
                "x": int(genotype[i, 1]),
                "y": int(genotype[i, 2]),
            }
        )

    export_folder = os.path.join(selected_experiment_folder, "export")
    os.makedirs(export_folder, exist_ok=True)

    used_emojies = {}
    for emoji_id in used_emoji_ids:
        used_emojies[emoji_id] = emoji_paths[emoji_id].name
        shutil.copy(
            emoji_paths[emoji_id],
            os.path.join(export_folder, emoji_paths[emoji_id].name),
        )

    data = {"emojies": used_emojies, "tiles": tiles}

    json_file_path = os.path.join(
        export_folder, best_stored_individual_path.stem + ".json"
    )
    with open(json_file_path, "w") as out_file:
        json.dump(data, out_file)

    print("Done")
