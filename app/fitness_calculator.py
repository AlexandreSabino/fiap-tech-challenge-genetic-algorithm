from abc import abstractmethod
from pandas import DataFrame

from app.domains.individual import AssetIndividual
import numpy as np

RISK_FREE_RATE_ANNUAL = 0.045
risk_free_rate_monthly_standard = RISK_FREE_RATE_ANNUAL / 12.0
HIGH_VOLATILITY_PENALTY_RATE = 1.4


class FitnessCalculator:

    @abstractmethod
    def initialize(self, df: DataFrame):
        pass

    @abstractmethod
    def execute(self, asset_individual: AssetIndividual, df: DataFrame) -> AssetIndividual:
        pass


class FitnessCalculatorBestReturnAndMinorVolatility(FitnessCalculator):

    def __init__(self):
        self.asset_order = None
        self.returns = None
        self.returns_mean = None

    def initialize(self, df: DataFrame):
        self.returns = df.pct_change().dropna()
        self.asset_order = df.columns
        self.returns_mean = self.returns.mean()

    def execute(self,
                asset_individual: AssetIndividual,
                df: DataFrame,
                risk_free_rate_monthly=risk_free_rate_monthly_standard) -> AssetIndividual:

        weights = np.array([asset_individual.assets.get(asset, 0) for asset in self.asset_order])
        portfolio_return_monthly = np.dot(self.returns_mean, weights)

        cov_matrix_monthly = self.returns.cov()

        portfolio_volatility_monthly = np.sqrt(np.dot(weights.T, np.dot(cov_matrix_monthly, weights)))

        if portfolio_volatility_monthly == 0:
            sharpe_ratio_monthly = 0.0
        else:
            sharpe_ratio_monthly = (portfolio_return_monthly - risk_free_rate_monthly) / portfolio_volatility_monthly ** HIGH_VOLATILITY_PENALTY_RATE

        fitness = sharpe_ratio_monthly

        return AssetIndividual(assets=asset_individual.assets, fitness=fitness)
