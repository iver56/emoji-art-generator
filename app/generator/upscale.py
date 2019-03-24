import os

import joblib
from PIL import Image

from app.generator.emoji import get_emojies
from app.settings import OUTPUT_DIR
from app.utils.files import get_subfolders, get_file_paths

if __name__ == "__main__":
    experiment_folders = get_subfolders(OUTPUT_DIR)
    experiment_folders.sort(key=lambda f: f.name)
    most_recent_experiment_folder = experiment_folders[-1]

    upscaling_factor = 4
    original_emoji_size = (16, 16)
    original_image_size = (225, 225)
    upscaled_image_size = (
        original_image_size[0] * upscaling_factor,
        original_image_size[1] * upscaling_factor,
    )
    upscaled_emoji_size = (
        original_emoji_size[0] * upscaling_factor,
        original_emoji_size[1] * upscaling_factor,
    )

    upscaled_emojies = get_emojies(size=upscaled_emoji_size[0])

    image = Image.new(mode="RGB", size=upscaled_image_size, color=(255, 255, 255))

    stored_individual_paths = get_file_paths(
        most_recent_experiment_folder, file_extensions=("pkl",)
    )
    stored_individual_paths.sort(key=lambda f: f.name)
    best_stored_individual_path = stored_individual_paths[-1]
    genotype = joblib.load(best_stored_individual_path)

    for i in range(len(genotype)):
        x = genotype[i][1] * upscaling_factor
        y = genotype[i][2] * upscaling_factor
        emoji_index = genotype[i][0]
        if x == 0 and y == 0 and emoji_index == 0:
            continue
        emoji = upscaled_emojies[emoji_index]
        image.paste(emoji, box=(x, y), mask=emoji)

    image.save(
        os.path.join(
            most_recent_experiment_folder,
            best_stored_individual_path.stem + "_upscaled.png",
        )
    )
    print("Done")
