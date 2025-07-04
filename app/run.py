from app.completion_checker import CompletionCheckerCounter
from app.domains.individual import AssetIndividual
from app.event import Event
import streamlit as st
import pandas as pd
import plotly.express as px
from app.fitness_calculator import FitnessCalculatorBestReturnAndMinorVolatility, FitnessCalculator
from app.genetic_algorithm_flow import GeneticAlgorithmFlow
from app.population_generator import PopulationGeneratorWithHotStart
from completion_checker import MAX_COUNTER
from app.collect_prices import collect_prices
from app.population_generator import POPULATION_SIZE

st.set_page_config(layout="wide")
st.title("Genetic Algorithm")

progress = st.progress(0, text=None, width="stretch")

st.markdown("---")
placeholder = st.empty()


class EventStreamlit(Event):

    def __init__(self):
        self.fitness_history = []

    def on_change_generation(self, generation: int, best_individual: AssetIndividual):
        current_fitness = best_individual.fitness
        self.fitness_history.append({'Geração': generation, 'Fitness': round(current_fitness, 3)})

        df_pie = pd.DataFrame(best_individual.assets.items(), columns=['Ativo', 'Percentual'])
        df_line = pd.DataFrame(self.fitness_history)

        progress.progress(generation / MAX_COUNTER, text=None, width="stretch")

        with placeholder.container():
            col1, col2 = st.columns(2)

            with col1:
                st.header("Melhor Portfólio")
                fig_pie = px.pie(df_pie,
                                 names='Ativo',
                                 values='Percentual',
                                 title=f"Composição na Geração {generation} - Best fitness: {best_individual.fitness:.5f} Carteiras analisadas: {generation*POPULATION_SIZE}",
                                 hole=0.3)
                fig_pie.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig_pie, use_container_width=True, key=f"pie_chart_{generation}")

            with col2:
                st.header("Evolução do Fitness")
                fig_line = px.line(df_line,
                                   x='Geração',
                                   y='Fitness',
                                   title="Fitness do Melhor Indivíduo por Geração",
                                   markers=True)

                if len(self.fitness_history) > 1:
                    fitness_values = df_line['Fitness']
                    min_val = fitness_values.min()
                    max_val = fitness_values.max()
                    padding = (max_val - min_val) * 0.1
                    if padding == 0:
                        padding = 0.0001
                    fig_line.update_yaxes(
                        range=[min_val - padding, max_val + padding],
                        tickformat=".5f"
                    )
                st.plotly_chart(fig_line, use_container_width=True, key=f"line_chart_{generation}")


df = collect_prices().dropna()
fitness_calculator = FitnessCalculatorBestReturnAndMinorVolatility(df)

genetic_algorithm_flow = GeneticAlgorithmFlow(
    PopulationGeneratorWithHotStart(),
    fitness_calculator,
    CompletionCheckerCounter(),
    EventStreamlit()
)

best_individual = genetic_algorithm_flow.run(df)

placeholder.empty()

initial_prices = df.iloc[0]
final_prices = df.iloc[-1]

st.header(f"Melhor Carteira Encontrada - Periodo: {initial_prices.name.strftime("%d/%m/%Y")} até {final_prices.name.strftime("%d/%m/%Y")}")

portfolio_return_monthly, weights = fitness_calculator.calculate_return_monthly(best_individual)
portfolio_volatility_monthly = fitness_calculator.calcula_volatility_monthly(weights)

col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Fitness Final", value=f"{best_individual.fitness:.5f}")
with col2:
    st.metric(label="Retorno Esperado Mensal", value=f"{portfolio_return_monthly:.2%}")
with col3:
    st.metric(label="Volatilidade Mensal (Risco)", value=f"{portfolio_volatility_monthly:.2%}")

st.markdown("---")

st.subheader("Composição Final da Carteira")
df_final = pd.DataFrame(best_individual.assets.items(), columns=['Ativo', 'Percentual'])

fig_final = px.pie(df_final,
                   names='Ativo',
                   values='Percentual',
                   title="Distribuição dos Ativos na Carteira Otimizada",
                   hole=0.3)
fig_final.update_traces(textposition='inside', textinfo='percent+label')

st.plotly_chart(fig_final, use_container_width=True)

st.subheader("Pesos Exatos")
st.dataframe(df_final.style.format({"Percentual": "{:.2%}"}))
