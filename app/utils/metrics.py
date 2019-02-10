import numpy as np
from colour import delta_E
from skimage.color import rgb2lab


class MSEFitnessEvaluator:
    @staticmethod
    def calculate_mse(image_a, image_b):
        """
        Calculate the total mean squared error between the pixels of two images
        The two images must have the same shape.
        :param image_a: 2D numpy array with float-like data type
        :param image_b: 2D numpy array with float-like data type
        :return: mse
        """
        err = np.sum((image_a - image_b) ** 2)
        # err /= float(image_a.shape[0] * image_a.shape[1])
        return err


class RGBMSEFitnessEvaluator(MSEFitnessEvaluator):
    """
    Significantly faster than the LAB-based methods, but is a poor model of human color
    perception
    """
    def __init__(self, target_image_pil):
        self.target_image_np = np.array(target_image_pil)

    def evaluate_fitness(self, individuals):
        for individual in individuals:
            fitness_value = 1 / (
                1
                + self.calculate_mse(
                    self.target_image_np, np.array(individual.genotype)
                )
            )
            individual.set_fitness(fitness_value)


class LABMSEFitnessEvaluator(MSEFitnessEvaluator):
    """
    Slower than RGBMSEFitnessEvaluator, but closer to human color perception
    """
    def __init__(self, target_image_pil):
        self.target_image_np_lab = rgb2lab(np.array(target_image_pil))

    def evaluate_fitness(self, individuals):
        for individual in individuals:
            fitness_value = 1 / (
                1
                + self.calculate_mse(
                    self.target_image_np_lab, rgb2lab(np.array(individual.genotype))
                )
            )
            individual.set_fitness(fitness_value)


class LABDeltaEFitnessEvaluator:
    """
    Slower than LABMSEFitnessEvaluator, but closer to human color perception
    """
    def __init__(self, target_image_pil):
        self.target_image_np_lab = rgb2lab(np.array(target_image_pil))

    def evaluate_fitness(self, individuals):
        for individual in individuals:
            fitness_value = 1 / (
                1
                + np.sum(
                    delta_E(
                        self.target_image_np_lab, rgb2lab(np.array(individual.genotype))
                    )
                )
            )
            individual.set_fitness(fitness_value)


FITNESS_EVALUATORS = {
    "RGBMSE": RGBMSEFitnessEvaluator,
    "LABMSE": LABMSEFitnessEvaluator,
    "LABDeltaE": LABDeltaEFitnessEvaluator,
}
