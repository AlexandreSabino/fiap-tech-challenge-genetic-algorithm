from pandas.core.interchange.dataframe_protocol import DataFrame

from app.completion_checker import CompletionChecker
from app.domains.individual import AssetIndividual
from app.event import Event
from app.fitness_calculator import FitnessCalculator
from app.population_generator import PopulationGenerator
from typing import List

def sort_population(individual_fitness: List[AssetIndividual]) -> List[AssetIndividual]:
    return sorted(individual_fitness, key=lambda individual: individual.fitness, reverse=True)

class GeneticAlgorithmFlow:

    def __init__(self,
                 population_generator: PopulationGenerator,
                 fitness_calculator: FitnessCalculator,
                 completion_checker: CompletionChecker,
                 event: Event):
        self.population_generator = population_generator
        self.fitness_calculator = fitness_calculator
        self.completion_checker = completion_checker
        self.event = event

    def run(self, df: DataFrame) -> AssetIndividual:
        population = self.population_generator.initial(df)
        counter = 0
        best_fitness = 0.0
        best_individual = None

        while not self.completion_checker.is_completed(counter, best_fitness):
            population_with_fitness = [self.fitness_calculator.execute(individual, df) for individual in population]
            population_ordered = sort_population(population_with_fitness)

            if population_ordered[0].fitness > best_fitness:
                best_fitness = population_ordered[0].fitness
                best_individual = population_ordered[0]
                print(f'best_fitness: {best_fitness} round: {counter} best_individual: {best_individual.assets}')

            population = self.population_generator.crossover_with_mutation(population_ordered, best_individual)
            counter += 1
            if counter % 10 == 0:
                print(f'Round: {counter}')

            self.event.on_change_generation(counter, best_individual)

        print(f'FINAL RESULT: best_fitness: {best_fitness} best_individual: {best_individual.assets}')
        return best_individual
