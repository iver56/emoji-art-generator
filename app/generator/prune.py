import os

import joblib
import numpy as np
from PIL import Image
from tqdm import tqdm

from app.generator.emoji import get_emojies
from app.generator.individual import Individual
from app.generator.upscale import generate_image_from_scratch
from app.settings import OUTPUT_DIR, TARGET_IMAGES_DIR
from app.utils.files import get_subfolders, get_file_paths
from app.utils.fitness import LABDeltaESSIMFitnessEvaluator

if __name__ == "__main__":
    """
    For each emoji, try to remove it and see if that removal improves the fitness.
    """

    experiment_folders = get_subfolders(OUTPUT_DIR)
    experiment_folders.sort(key=lambda f: f.name)
    most_recent_experiment_folder = experiment_folders[-1]

    target_image_filename = "sunglasses.png"
    target_image = Image.open(TARGET_IMAGES_DIR / target_image_filename).convert("RGB")

    upscaling_factor = 1
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

    stored_individual_paths = get_file_paths(
        most_recent_experiment_folder, file_extensions=("pkl",)
    )
    stored_individual_paths.sort(key=lambda f: f.name)
    best_stored_individual_path = stored_individual_paths[-1]
    genotype = joblib.load(best_stored_individual_path)

    upscaled_emojies = get_emojies(size=upscaled_emoji_size[0])

    fitness_evaluator = LABDeltaESSIMFitnessEvaluator(target_image)

    image = generate_image_from_scratch(genotype, upscaled_image_size, upscaled_emojies)
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
        )
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
            most_recent_experiment_folder,
            best_stored_individual_path.stem + "_pruned.pkl",
        ),
    )

    image.save(
        os.path.join(
            most_recent_experiment_folder,
            best_stored_individual_path.stem + "_pruned.png",
        )
    )
    print("Done")
