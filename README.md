# fiap-tech-challenge-genetic-algorithm

### Desafio
O desafio consiste em projetar, implementar e testar um sistema que
utilize Algoritmos Genéticos para otimizar uma função ou resolver um problema
complexo de otimização. Você pode escolher problemas como otimização de
rotas, alocação de recursos e design de redes neurais.

### Descrição do problema:
Otimizar os pesos de uma carteira de investimentos com ativos nacionais e 
internacionais. 
A melhor carteira é aquela que tem o maior retorno ajustado ao risco, ou seja,
o maior retorno com menos volatlidade (nesse caso estamos considerando que ricos é igual a volatilidade).
Foi utilizado o índice de SHARPE para mensurar esse indicador.

Índice de Sharpe = (Retorno do Investimento - Taxa Livre de Risco) / Desvio Padrão de volatilidade

Restrições:
- Cada ativo deve ter no minimo 2% de representatividade (peso) na carteira.
- Cada ativo deve ter no máximo 50% de representatividade (peso) na carteira.
- Todo o cálculo deve ser feito em dolares, os ativos brasileiros devem ser convertidos para dolares.
- Serão utilizados apenas os seguintes ativos:
  1. BOVA11.SA - ETF que representa o índice das maiores empresas do Brasil.
  2. SMAL11.SA - ETF que representa o índice das empresas com menor valor de mercado do Brasil.
  3. XFIX11.SA - ETF que representa o índice de fundos imobiliários. 
  4. IMAB11.SA - ETF de renda fixa brasileiro.
  5. IVV - ETF que representa o índice das 500 maiores empresas dos EUA.
  6. IAU - ETF de ouro.
  7. TLT - ETF de titulos de 10 anos do governo americano. 
  8. BIL - ETF de titulos de 3 anos do governo americano.
  9. BTC-USD - Maior criptomoeda do mundo.

## Estratégias:

- <b>Coleta de dados para os cálculos:</b> Foi utilizado a biblicoteca yfinance, para obter os dados de preço de cada ativo e 
cotação do dolar.

- <b>Geração da população inicial:</b> Como estratégia de hot start, foi adicionado a população inicial
a carteira maior retorno possivel e a carteira com a menor volatilidade, os demais 
indivíduos foram gerados de maneira aleatória.

- <b>Função de parada:</b> O algoritimo para após atingir X gerações.

- <b>Cáculo do fitness:</b> o fitness é o indice de SHARPE.
Índice de Sharpe = (Retorno do Investimento - Taxa Livre de Risco) / Desvio Padrão de volatilidade

- <b>Seleção:</b> A função seleciona aleátoriamente 5 indíviduos e faz uma disputa entre eles,
o maior fitness é escolhido, esse processo é executado para 2x para selecionar o parent1 e parent2 e passa-los para função de crossover.
Também é adicionado na lista o melhor indíviduo da geração anterior (elitismo).

- <b>Crossover:</b> A função segue os seguintes passos: </br>
  1. Sorteia aleátoriamente um determinado numero de ativos.
  2. Sorteia aleátoriamente os ativos dentro da carteira.
  3. Inverte os pesos entre os parents.
  4. Faz um shuffle da lista de ativos e redistribui os pesos para garantir que a soma dê 100%.

- <b>Mutação:</b> Para 10% da população é sorteado de forma aleátoria um numero entre -5% e 5%, esse valor 
é subtraido (ou somado dependendo se o sorteio foi positivo ou negativo) de cada ativo. O excedente ou faltante é redistribuido de forma 
aleátoria no final.

Para visualização dos dados foi utilizado a biblioteca streamlit.