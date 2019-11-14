import argparse
import os

import joblib
import numpy as np
from PIL import Image
from tqdm import tqdm

from app.generator.emoji import get_emojies
from app.generator.individual import Individual
from app.settings import OUTPUT_DIR
from app.utils.argparse_sanity import positive_int
from app.utils.files import get_subfolders, get_file_paths
from app.utils.fitness import LABDeltaESSIMFitnessEvaluator


def generate_image_from_scratch(genotype, image_size, emojies):
    """
    :param genotype:
    :param image_size:
    :param emojies:
    :return:
    """
    image = Image.new(mode="RGB", size=image_size, color=(255, 255, 255, 0))
    for i in range(len(genotype)):
        x = genotype[i][1]
        y = genotype[i][2]
        emoji_index = genotype[i][0]
        if x == 0 and y == 0 and emoji_index == 0:
            continue
        emoji = emojies[emoji_index]
        image.paste(emoji, box=(x, y), mask=emoji)
    return image


if __name__ == "__main__":
    """
    For each emoji, try to remove it and see if that removal improves the fitness.
    """

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
    args = arg_parser.parse_args()

    if args.experiment is None:
        experiment_folders = get_subfolders(OUTPUT_DIR)
        experiment_folders.sort(key=lambda f: f.name)
        selected_experiment_folder = experiment_folders[-1]
    else:
        selected_experiment_folder = OUTPUT_DIR / args.experiment

    target_image = Image.open(
        os.path.join(selected_experiment_folder, "target.png")
    ).convert("RGB")

    upscaling_factor = 1
    original_emoji_size = (args.emoji_size, args.emoji_size)
    original_image_size = target_image.size
    upscaled_image_size = (
        original_image_size[0] * upscaling_factor,
        original_image_size[1] * upscaling_factor,
    )
    upscaled_emoji_size = (
        original_emoji_size[0] * upscaling_factor,
        original_emoji_size[1] * upscaling_factor,
    )

    stored_individual_paths = get_file_paths(
        selected_experiment_folder, file_extensions=("pkl",)
    )
    stored_individual_paths.sort(key=lambda f: f.name)
    best_stored_individual_path = stored_individual_paths[-1]
    genotype = joblib.load(best_stored_individual_path)

    upscaled_emojies = get_emojies(size=upscaled_emoji_size[0])

    fitness_evaluator = LABDeltaESSIMFitnessEvaluator(target_image)

    image = generate_image_from_scratch(
        genotype, upscaled_image_size, upscaled_emojies
    ).convert("RGB")
    base_individual = Individual(image)
    fitness_evaluator.evaluate_fitness([base_individual])
    current_fitness = base_individual.fitness
    print("Base fitness: {}".format(current_fitness))
    current_genotype = genotype
    num_emojies_removed = 0
    for i in tqdm(range(len(genotype))):
        candidate_genotype = np.copy(current_genotype)
        candidate_genotype[i, :] = 0  # Remove this emoji
        image = generate_image_from_scratch(
            candidate_genotype, upscaled_image_size, upscaled_emojies
        ).convert("RGB")
        candidate_individual = Individual(image)
        fitness_evaluator.evaluate_fitness([candidate_individual])
        if candidate_individual.fitness >= current_fitness:
            current_genotype = candidate_genotype
            current_fitness = candidate_individual.fitness
            num_emojies_removed += 1

    print("Removed {} of {} emojies".format(num_emojies_removed, len(genotype)))
    print("Fitness after culling emojies: {}".format(current_fitness))

    joblib.dump(
        current_genotype,
        os.path.join(
            selected_experiment_folder, best_stored_individual_path.stem + "_pruned.pkl"
        ),
    )

    image.save(
        os.path.join(
            selected_experiment_folder, best_stored_individual_path.stem + "_pruned.png"
        )
    )
    print("Done")
