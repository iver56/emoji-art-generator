import json
import os
import shutil

import numpy as np
import joblib

from app.generator.emoji import get_emojies
from app.settings import OUTPUT_DIR, EMOJI_DIR
from app.utils.files import get_subfolders, get_file_paths

if __name__ == "__main__":
    experiment_folders = get_subfolders(OUTPUT_DIR)
    experiment_folders.sort(key=lambda f: f.name)
    most_recent_experiment_folder = experiment_folders[-1]

    upscaling_factor = 6
    original_emoji_size = (16, 16)
    original_image_size = (225, 225)

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
        most_recent_experiment_folder, file_extensions=("pkl",)
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

    export_folder = os.path.join(most_recent_experiment_folder, "export")
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
