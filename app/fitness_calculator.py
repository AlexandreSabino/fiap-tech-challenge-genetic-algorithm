from abc import abstractmethod, ABC
from pandas import DataFrame

from app.domains.individual import AssetIndividual
import numpy as np

RISK_FREE_RATE_ANNUAL = 0.045

class FitnessCalculator:

    @abstractmethod
    def initialize(self, df: DataFrame):
        pass

    @abstractmethod
    def execute(self, asset_individual: AssetIndividual, df: DataFrame) -> AssetIndividual:
        pass

class FitnessCalculatorBestReturnAndMinorVolatility(FitnessCalculator):

    def __init__(self, df: DataFrame):
        self.returns = df.pct_change().dropna()
        self.asset_order = df.columns
        self.total_returns_mean = self.returns.mean()
        self.cov_matrix_monthly = self.returns.cov()

    def execute(self,
                asset_individual: AssetIndividual,
                df: DataFrame,
                risk_free_rate=RISK_FREE_RATE_ANNUAL) -> AssetIndividual:

        portfolio_return, weights = self.calculate_return_monthly(asset_individual)
        portfolio_volatility = self.calcula_volatility_monthly(weights)

        portfolio_return_annual = portfolio_return * 12
        portfolio_volatility_annual = portfolio_volatility * np.sqrt(12)

        if portfolio_volatility == 0:
            sharpe_ratio = 0.0
        else:
            sharpe_ratio = (portfolio_return_annual - risk_free_rate) / portfolio_volatility_annual

        return AssetIndividual(assets=asset_individual.assets, fitness=sharpe_ratio)

    def calcula_volatility_monthly(self, weights):
        portfolio_volatility_monthly = np.sqrt(np.dot(weights.T, np.dot(self.cov_matrix_monthly, weights)))
        return portfolio_volatility_monthly

    def calculate_return_monthly(self, asset_individual: AssetIndividual):
        weights = np.array([asset_individual.assets.get(asset, 0) for asset in self.asset_order])
        portfolio_return_monthly = np.dot(self.total_returns_mean, weights)
        return portfolio_return_monthly, weights
