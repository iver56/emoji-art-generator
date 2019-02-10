import argparse
import os
import random
import uuid

import arrow as arrow
from PIL import Image
from tqdm import tqdm

from app.generator.emoji import emojies
from app.settings import TARGET_IMAGES_DIR, OUTPUT_DIR
from app.utils.gif import make_gif
from app.utils.metrics import FITNESS_EVALUATORS

population_size = 3
num_generations = 500000
mutation_rate = 0.99
crossover_rate = 0.0
elitism = 1

# Minimum relative fitness improvement required over the previous best before image is saved
save_improvement_threshold = 0.005

assert elitism < population_size


class Individual:
    def __init__(self, genotype, fitness=None):
        self.genotype = genotype
        self.fitness = fitness

    def apply_mutation(self):
        emoji = random.choice(emojies)
        x = random.randint(-31, target_image.width - 1)
        y = random.randint(-31, target_image.height - 1)

        self.genotype.paste(emoji, box=(x, y), mask=emoji)

    def apply_crossover(self, other_individual):
        pass

    def set_fitness(self, fitness):
        self.fitness = fitness

    @staticmethod
    def get_random_individual():
        candidate_image = Image.new(
            mode=target_image.mode, size=target_image.size, color=(255, 255, 255)
        )
        return Individual(candidate_image)

    def __str__(self):
        return "Individual(fitness={:.12f})".format(self.fitness)

    def copy(self):
        return Individual(genotype=self.genotype.copy(), fitness=self.fitness)


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument(
        "--fitness",
        dest="fitness",
        type=str,
        choices=FITNESS_EVALUATORS.keys(),
        help="Select fitness evaluator. RGBMSE is fast, but far from human color perception."
        " LABMSE is slow, but closer to human color perception",
        required=False,
        default="LABMSE",
    )
    args = arg_parser.parse_args()

    experiment_id = "{}_{}".format(
        arrow.utcnow().format("YYYY-MM-DDTHHmm"), uuid.uuid4()
    )
    target_image = Image.open(TARGET_IMAGES_DIR / "sunglasses.png").convert("RGB")
    print("Found {} emoji images".format(len(emojies)))

    fitness_evaluator_class = FITNESS_EVALUATORS[args.fitness]
    fitness_evaluator = fitness_evaluator_class(target_image)

    os.makedirs(OUTPUT_DIR / experiment_id, exist_ok=True)

    population = [Individual.get_random_individual() for _ in range(population_size)]

    last_saved_fitness = float("-inf")

    for i in tqdm(range(num_generations)):
        fitness_evaluator.evaluate_fitness(population)
        ordered_individuals = sorted(population, key=lambda i: i.fitness)
        fittest_individual = ordered_individuals[-1]
        if (
            fittest_individual.fitness
            >= (1 + save_improvement_threshold) * last_saved_fitness
        ):
            last_saved_fitness = fittest_individual.fitness
            print("\nFittest individual: {}".format(fittest_individual))
            fittest_individual.genotype.save(
                OUTPUT_DIR / experiment_id / "{:0>6}_{}.png".format(i, uuid.uuid4())
            )

        # Very simple parent selection: Select the 2 best individuals
        parents = ordered_individuals[-2:]
        new_population = []

        for i in range(elitism):
            good_parent = ordered_individuals[-(i + 1)].copy()
            new_population.append(good_parent)

        for i in range(population_size - elitism):
            random_parents = random.sample(parents, k=2)
            individual = random_parents[0].copy()
            if random.random() < crossover_rate:
                individual.apply_crossover(random_parents[1])

            if random.random() < mutation_rate:
                individual.apply_mutation()

            new_population.append(individual)

        population = new_population
