import argparse
import os
import random
import uuid

import arrow as arrow
from PIL import Image
from tqdm import tqdm

from app.generator.emoji import get_emojies
from app.generator.individual import Individual
from app.settings import TARGET_IMAGES_DIR, OUTPUT_DIR
from app.utils.argparse_sanity import positive_int
from app.utils.fitness import FITNESS_EVALUATORS
from app.utils.gif import make_gif

mutation_rate = 0.9999
elitism = 1

# Minimum relative fitness improvement required over the previous best before image is saved
save_improvement_threshold = 0.005


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument(
        "--starting-canvas",
        dest="starting_canvas",
        type=str,
        help="Path to an image to start with. If not specified, a white image will be used.",
        required=False,
        default=None,
    )
    arg_parser.add_argument(
        "--target",
        dest="target",
        type=str,
        help="Filename of target image. Should reside in data/target_images/",
        required=False,
        default="sunglasses2.png",
    )
    arg_parser.add_argument(
        "--fitness",
        dest="fitness",
        type=str,
        choices=FITNESS_EVALUATORS.keys(),
        help="Choose fitness evaluator. See fitness.py for more information.",
        required=False,
        default="LABDeltaESSIM",
    )
    arg_parser.add_argument(
        "-g",
        "--num-generations",
        dest="num_generations",
        type=positive_int,
        required=False,
        default=30000,
    )
    arg_parser.add_argument(
        "-p",
        "--population-size",
        dest="population_size",
        type=positive_int,
        required=False,
        default=4,
    )
    arg_parser.add_argument(
        "--width",
        dest="width",
        type=int,
        required=False,
        default=-1,
        help="If specified, resize the target image (and the starting canvas) to this width."
        " Otherwise, keep the original width.",
    )
    arg_parser.add_argument(
        "--height",
        dest="height",
        type=int,
        required=False,
        default=-1,
        help="If specified, resize the target image (and the starting canvas) to this height."
        " Otherwise, keep the original height.",
    )
    arg_parser.add_argument(
        "--emoji-size", dest="emoji_size", type=positive_int, required=False, default=16
    )
    args = arg_parser.parse_args()

    assert elitism < args.population_size

    experiment_id = "{}_{}".format(arrow.utcnow().format("YYYY-MM-DDTHHmm"), uuid.uuid4())

    target_image = Image.open(TARGET_IMAGES_DIR / args.target)
    should_resize = args.width >= 1 and args.height >= 1
    if should_resize:
        print("Resizing the target image to ({}, {})".format(args.width, args.height))
        target_image = target_image.resize((args.width, args.height), Image.LANCZOS)

    os.makedirs(OUTPUT_DIR / experiment_id, exist_ok=True)

    target_image.save(os.path.join(OUTPUT_DIR / experiment_id, "target.png"))

    target_image = target_image.convert("RGB")

    if args.starting_canvas is not None:
        starting_canvas = Image.open(args.starting_canvas).convert("RGB")
        if should_resize:
            starting_canvas = starting_canvas.resize((args.width, args.height), Image.LANCZOS)
        assert starting_canvas.size == target_image.size
        Individual.set_starting_canvas(starting_canvas)

    Individual.target_image = target_image
    Individual.emojies = get_emojies(args.emoji_size)
    Individual.max_num_emojies = args.num_generations
    print("Found {} emoji images".format(len(Individual.emojies)))

    fitness_evaluator_class = FITNESS_EVALUATORS[args.fitness]
    fitness_evaluator = fitness_evaluator_class(target_image)



    population = [Individual.get_random_individual() for _ in range(args.population_size)]

    last_saved_fitness = float("-inf")

    for i in tqdm(range(args.num_generations)):
        fitness_evaluator.evaluate_fitness(population)
        ordered_individuals = sorted(population, key=lambda i: i.fitness)
        fittest_individual = ordered_individuals[-1]
        if fittest_individual.fitness >= (1 + save_improvement_threshold) * last_saved_fitness:
            last_saved_fitness = fittest_individual.fitness
            print("\nFittest individual: {}".format(fittest_individual))
            fittest_individual.save(
                OUTPUT_DIR / experiment_id / "{:0>6}_{}.png".format(i, uuid.uuid4())
            )

        # Very simple parent selection: Select the 2 best individuals
        parents = ordered_individuals[-2:]
        new_population = []

        for i in range(elitism):
            good_parent = ordered_individuals[-(i + 1)].copy()
            new_population.append(good_parent)

        for i in range(args.population_size - elitism):
            random_parents = random.sample(parents, k=2)
            individual = random_parents[0].copy()

            if random.random() < mutation_rate:
                individual.apply_mutation()

            new_population.append(individual)

        population = new_population

    make_gif(OUTPUT_DIR / experiment_id)
