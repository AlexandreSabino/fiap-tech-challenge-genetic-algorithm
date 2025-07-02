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
        sorted_assets = sorted(self.assets.items(), key=lambda item: item[1]) if residual_weight > 0 else sorted(
            self.assets.items(), key=lambda item: item[1], reverse=True)

        for asset in sorted_assets:
            new_weight = residual_weight + asset[1]
            self.assets[asset[0]] = min(max_percentage, max(new_weight, min_percentage))
            residual_weight = 1 - self.total_weight()
            if residual_weight == 0.0:
                break
