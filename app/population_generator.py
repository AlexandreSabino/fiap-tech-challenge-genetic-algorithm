import random
from abc import abstractmethod
from copy import deepcopy
from typing import List

import pandas as pd
from pandas import DataFrame

from app.domains.individual import AssetIndividual

import numpy as np
import copy
import math

# Regras:
# - Todos os ativos devem estar presentes na carteira.
# - Cada ativo deve ter no minimo 5%.
# - Um Ativo deve ter no maximo 45%.

POPULATION_SIZE = 100

MIN_PERCENTAGE = 0.05
MAX_PERCENTAGE = 0.45

MUTATION_RATE = 0.1
MUTATION_INTENSITY = 0.05


class PopulationGenerator:

    @abstractmethod
    def initial(self, df) -> List[AssetIndividual]:
        pass

    @abstractmethod
    def crossover_with_mutation(self, population: List[AssetIndividual], best_individual: AssetIndividual) -> List[
        AssetIndividual]:
        pass


def calculate_best_returns(df: DataFrame) -> AssetIndividual:
    initial_prices = df.iloc[0]
    final_prices = df.iloc[-1]

    returns = (final_prices / initial_prices - 1)
    returns_df = pd.DataFrame(returns).sort_values(by=0, ascending=True)

    total_return = returns.sum() if returns.sum() != 0 else 0.000000001
    weights = {}
    residual_weight = 1.0
    assets_pending = len(df.columns)

    for _, row in returns_df.iterrows():
        max_value = min(MAX_PERCENTAGE, residual_weight / assets_pending)
        weight_value = max(row.values[0] / total_return, MIN_PERCENTAGE)
        weight_value = min(weight_value, max_value)
        weights[row.name] = weight_value
        residual_weight -= weight_value
        assets_pending -= 1

    if residual_weight > 0.0:
        returns_df = returns_df.sort_values(by=0, ascending=False)
        for _, row in returns_df.iterrows():
            new_weight = residual_weight + weights[row.name]
            residual = new_weight - MAX_PERCENTAGE
            weights[row.name] = min(MAX_PERCENTAGE, new_weight)
            residual_weight = residual
            if residual_weight <= 0.0:
                break

    individual = AssetIndividual(assets=weights)
    individual.adjust_weights(MIN_PERCENTAGE, MAX_PERCENTAGE)
    return individual


def calculate_minor_volatility(df: DataFrame) -> AssetIndividual:
    returns = df.pct_change().dropna()
    volatility_inverse = 1 / returns.std()
    volatility_inverse_df = pd.DataFrame(volatility_inverse).sort_values(by=0, ascending=True)

    total_volatility_inverse = volatility_inverse.sum()
    weights = {}
    residual_weight = 1.0
    assets_pending = len(df.columns)

    for _, row in volatility_inverse_df.iterrows():
        max_value = min(MAX_PERCENTAGE, residual_weight / assets_pending)
        weight_value = max(row.values[0] / total_volatility_inverse, MIN_PERCENTAGE)
        weight_value = min(weight_value, max_value)
        weights[row.name] = weight_value
        residual_weight -= weight_value
        assets_pending -= 1

    if residual_weight > 0.0:
        volatility_inverse_df = volatility_inverse_df.sort_values(by=0, ascending=False)
        for _, row in volatility_inverse_df.iterrows():
            new_weight = residual_weight + weights[row.name]
            residual = new_weight - MAX_PERCENTAGE
            weights[row.name] = min(MAX_PERCENTAGE, new_weight)
            residual_weight = residual
            if residual_weight <= 0.0:
                break

    individual = AssetIndividual(assets=weights)
    individual.adjust_weights(MIN_PERCENTAGE, MAX_PERCENTAGE)
    return individual


def generate_random(df: DataFrame, size) -> List[AssetIndividual]:
    all_individuals: List[AssetIndividual] = []
    for i in range(size):
        residual_weight = 1.0
        individual = {}
        assets_pending = len(df.columns)
        for col in df.columns:
            max_value = min(MAX_PERCENTAGE, residual_weight / assets_pending)
            weight = np.random.uniform(low=MIN_PERCENTAGE, high=max_value, size=1)[0]
            residual_weight -= weight
            individual[col] = weight
            assets_pending -= 1

        asset_individual = AssetIndividual(assets=individual)
        asset_individual.adjust_weights(MIN_PERCENTAGE, MAX_PERCENTAGE)
        all_individuals.append(asset_individual)

    return all_individuals


def apply_crossover(parent1: AssetIndividual, parent2: AssetIndividual):
    all_assets = list(parent1.assets.keys())
    assets_to_exchange = random.randint(1, len(all_assets))
    # assets = random.choices(all_assets, k=assets_to_exchange)
    assets = random.choices(all_assets, k=2)

    child1 = copy.deepcopy(parent1)
    child2 = copy.deepcopy(parent2)

    for asset in assets:
        child1, child2 = exchange_asset(asset, child1, child2)

    return child1, child2


def exchange_asset(asset, parent1, parent2):
    w1 = parent1.assets[asset]
    w2 = parent2.assets[asset]
    child1 = copy.deepcopy(parent1)
    child2 = copy.deepcopy(parent2)
    child1.assets[asset] = w2
    child2.assets[asset] = w1
    child1.fitness = 0
    child2.fitness = 0

    child1.adjust_weights(MIN_PERCENTAGE, MAX_PERCENTAGE)
    child2.adjust_weights(MIN_PERCENTAGE, MAX_PERCENTAGE)
    return child1, child2


def apply_mutation(individual: AssetIndividual):
    if random.random() <= MUTATION_RATE:
        mutation_rate = random.uniform(-MUTATION_INTENSITY, MUTATION_INTENSITY)
        if mutation_rate != 0.0:
            for asset in individual.assets:
                weight = individual.assets[asset] + mutation_rate
                individual.assets[asset] = weight

            individual.adjust_weights(MIN_PERCENTAGE, MAX_PERCENTAGE)


def select_by_tournament(population: List[AssetIndividual], k: int = 5) -> AssetIndividual:
    tournament_contenders = random.sample(population, k)
    winner = max(tournament_contenders, key=lambda individual: individual.fitness)
    return winner


def check(individual: AssetIndividual):
    for asset in individual.assets:
        w = individual.assets[asset]
        if w < MIN_PERCENTAGE or w > MAX_PERCENTAGE or math.isnan(w):
            print("ACHEI w < MIN_PERCENTAGE or w > MAX_PERCENTAGE or math.isnan(w)")

    if abs(1 - individual.total_weight()) > 0.0001:
        print(" individual.total_weight() != 1")


class PopulationGeneratorWithHotStart(PopulationGenerator):

    def initial(self, df) -> List[AssetIndividual]:
        all_individuals: List[AssetIndividual] = [calculate_best_returns(df), calculate_minor_volatility(df)]
        all_individuals += generate_random(df, POPULATION_SIZE - len(all_individuals))
        return all_individuals

    def crossover_with_mutation(self, population: List[AssetIndividual], best_individual: AssetIndividual) -> List[
        AssetIndividual]:
        new_population = [copy.deepcopy(best_individual)]  # elitism
        length = len(new_population)

        while len(new_population) < POPULATION_SIZE - length:
            parent1 = select_by_tournament(population)
            parent2 = select_by_tournament(population)

            new_individual_1, new_individual_2 = apply_crossover(parent1, parent2)
            apply_mutation(new_individual_1)
            apply_mutation(new_individual_2)

            new_population.append(new_individual_1)
            new_population.append(new_individual_2)

            check(new_individual_1)
            check(new_individual_2)

        return new_population
