class AssetIndividual:

    def __init__(self, assets=None, fitness=0.0):
        self.assets = assets if assets is not None else {}
        self.fitness = fitness

    def total_weight(self) -> float:
        return sum(self.assets.values())

    def adjust_weights(self):
        total = sum(self.assets.values())
        if total == 0:
            raise ValueError("Total weight is zero.")
        for key in self.assets:
            self.assets[key] /= total
