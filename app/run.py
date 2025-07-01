from app.completion_checker import CompletionCheckerCounter
from app.fitness_calculator import FitnessCalculatorBestReturnAndMinorVolatility
from app.genetic_algorithm_flow import GeneticAlgorithmFlow
from app.population_generator import PopulationGeneratorWithHotStart

genetic_algorithm_flow = GeneticAlgorithmFlow(
    PopulationGeneratorWithHotStart(),
    FitnessCalculatorBestReturnAndMinorVolatility(),
    CompletionCheckerCounter()
)

genetic_algorithm_flow.run()