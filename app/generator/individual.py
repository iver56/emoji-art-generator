import random

import joblib
import numpy as np
from PIL import Image


class Individual:
    emojies = None
    target_image = None
    starting_canvas = None
    max_num_emojies = 30000

    @staticmethod
    def set_starting_canvas(starting_canvas):
        """
        Use this function to set the initial image for the initial individuals
        :return:
        """
        Individual.starting_canvas = starting_canvas

    def __init__(self, phenotype, fitness=None, genotype=None, current_emoji_index=0):
        self.phenotype = phenotype  # Pillow image
        self.fitness = fitness
        if genotype is None:
            # emoji_index, x, y
            self.genotype = np.zeros((Individual.max_num_emojies, 3), dtype=np.uint16)
        else:
            self.genotype = genotype
        self.current_emoji_index = current_emoji_index

    def apply_mutation(self):
        emoji_index = random.randrange(len(Individual.emojies))
        emoji = Individual.emojies[emoji_index]
        x = random.randint(-31, Individual.target_image.width - 1)
        y = random.randint(-31, Individual.target_image.height - 1)

        self.phenotype.paste(emoji, box=(x, y), mask=emoji)
        self.genotype[self.current_emoji_index, 0] = emoji_index
        self.genotype[self.current_emoji_index, 1] = x
        self.genotype[self.current_emoji_index, 2] = y
        self.current_emoji_index += 1

    def set_fitness(self, fitness):
        self.fitness = fitness

    @staticmethod
    def get_random_individual():
        if Individual.starting_canvas:
            return Individual(Individual.starting_canvas.copy())
        else:
            candidate_image = Image.new(
                mode=Individual.target_image.mode,
                size=Individual.target_image.size,
                color=(255, 255, 255),
            )
            return Individual(candidate_image)

    def __str__(self):
        return "Individual(fitness={:.12f})".format(self.fitness)

    def copy(self):
        individual = Individual(
            phenotype=self.phenotype.copy(),
            fitness=self.fitness,
            genotype=np.copy(self.genotype),
            current_emoji_index=self.current_emoji_index
        )
        return individual

    def save(self, file_path):
        self.phenotype.save(file_path.with_suffix(".png"))
        joblib.dump(self.genotype, file_path.with_suffix('.pkl'))

    @staticmethod
    def generate_individual_from_genotype(self, genotype):
        individual = Individual.get_random_individual()
        # TODO
