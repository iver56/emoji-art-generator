import random

from PIL import Image


class Individual:
    emojies = None
    target_image = None
    starting_canvas = None

    @staticmethod
    def set_starting_canvas(starting_canvas):
        """
        Use this function to set the initial image for the initial individuals
        :return:
        """
        Individual.starting_canvas = starting_canvas

    def __init__(self, genotype, fitness=None):
        self.genotype = genotype
        self.fitness = fitness

    def apply_mutation(self):
        emoji = random.choice(Individual.emojies)
        x = random.randint(-31, Individual.target_image.width - 1)
        y = random.randint(-31, Individual.target_image.height - 1)

        self.genotype.paste(emoji, box=(x, y), mask=emoji)

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
        return Individual(genotype=self.genotype.copy(), fitness=self.fitness)
