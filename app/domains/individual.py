import random

class AssetIndividual:

    def __init__(self, assets=None, fitness=0.0):
        self.assets = assets if assets is not None else {}
        self.fitness = fitness

    def total_weight(self) -> float:
        return sum(self.assets.values())

    def adjust_weights(self, min_percentage: float, max_percentage: float):
        for asset in self.assets:
            weight = self.assets[asset]
            if weight < min_percentage:
                self.assets[asset] = min_percentage
            elif weight > max_percentage:
                self.assets[asset] = max_percentage

        residual_weight = 1 - self.total_weight()

        shuffle_assets = list(self.assets.keys())
        random.shuffle(shuffle_assets)

        assets_pending = len(shuffle_assets)
        for asset in shuffle_assets:
            unit_residual = residual_weight / assets_pending
            new_weight = unit_residual + self.assets[asset]
            self.assets[asset] = min(max_percentage, max(new_weight, min_percentage))
            residual_weight = 1 - self.total_weight()
            if residual_weight == 0.0:
                break
            assets_pending = assets_pending - 1

        for asset in shuffle_assets:
            new_weight = residual_weight + self.assets[asset]
            self.assets[asset] = min(max_percentage, max(new_weight, min_percentage))
            residual_weight = 1 - self.total_weight()
            if residual_weight == 0.0:
                break