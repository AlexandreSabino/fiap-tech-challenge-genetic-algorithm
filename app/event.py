from app.domains.individual import AssetIndividual
from abc import abstractmethod

class Event:

    @abstractmethod
    def on_change_generation(self, generation: int, best_individual: AssetIndividual):
        pass