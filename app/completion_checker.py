from abc import abstractmethod

class CompletionChecker:

    @abstractmethod
    def is_completed(self, counter: int, best_fitness: float) -> bool:
        pass

# MAX_COUNTER = 5000
MAX_COUNTER = 200

class CompletionCheckerCounter(CompletionChecker):

    def is_completed(self, counter: int, best_fitness: float) -> bool:
        return counter >= MAX_COUNTER