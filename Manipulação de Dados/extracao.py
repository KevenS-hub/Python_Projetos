import pandas as pd
from datetime import date
from datetime import datetime as dt

df_selic = pd.read_json("https://api.bcb.gov.br/dados/serie/bcdata.sgs.11/dados?formato=json")

print(df_selic.info())

df_selic.drop_duplicates(keep='last', inplace=True)

data_extracao = date.today()

df_selic['data_extracao'] = data_extracao
df_selic['responsavel'] = "Autora"
df_selic['responsavel'] = df_selic['responsavel'].str.upper()

df_selic['data'] = pd.to_datetime(df_selic['data'], dayfirst=True)
df_selic['data_extracao'] = df_selic['data_extracao'].astype('datetime64[ns]')

print(df_selic.info())

df_selic.sort_values(by='data', ascending=False, inplace=True)
df_selic.reset_index(drop=True, inplace=True)
print(df_selic.head())

lista_novo_indice = [f'selic_{indice}' for indice in df_selic.index]
print(lista_novo_indice[:5])

df_selic.set_index(keys=[lista_novo_indice], inplace=True)
df_selic.head()

print(df_selic['valor'].idxmin())
print(df_selic['valor'].idxmax())

df_selic.loc['selic_0']
df_selic.loc[['selic_0', 'selic_4', 'selic_200']]
df_selic.loc[:'selic_5']
df_selic.loc[['selic_0', 'selic_4', 'selic_200'], ['valor', 'data_extracao']]

df_selic.iloc[:5]

teste2 = df_selic['valor'] < 0.01
print(type(teste2))
teste2[:5]

teste2 = df_selic['data'] >= pd.to_datetime('2020-01-01')

print(type(teste2))
teste2[:5]

teste3 = (df_selic['valor'] < 0.01) & (df_selic['data'] >= pd.to_datetime('2020-01-01'))
teste4 = (df_selic['valor'] < 0.01) | (df_selic['data'] >= pd.to_datetime('2020-01-01'))

print("Resultado do AND: \n")
print(teste3[:3])

print("Resultado do OR: \n")
print(teste4[:3])

filtro1 = df_selic['valor'] < 0.01
df_selic.loc[filtro1]

data1 = pd.to_datetime('2020-01-01')
data2 = pd.to_datetime('2020-01-31')

filtro_janeiro_2020 = (df_selic['data'] >= data1) & (df_selic['data'] <= data2)

df_janeiro_2020 = df_selic.loc[filtro_janeiro_2020]
df_janeiro_2020.head()

data1v9 = pd.to_datetime('2019-01-01')
data2v9 = pd.to_datetime('2019-01-31')

filtro_janeiro_2019 = (df_selic['data'] >= data1v9) & (df_selic['data'] <= data2v9)
df_janeiro_2019 = df_selic.loc[filtro_janeiro_2019]
print(df_janeiro_2019.head())

print('Mínimo geral = ', df_selic['valor'].min())
print('Mínimo janeiro de 2019 = ', df_janeiro_2019['valor'].min())
print('Mínimo janeiro de 2020 = ', df_janeiro_2020['valor'].min(), '\n')

print('Máximo geral = ', df_selic['valor'].max())
print('Máximo janeiro de 2019 = ', df_janeiro_2019['valor'].max())
print('Máximo janeiro de 2020 = ', df_janeiro_2020['valor'].max(), '\n')

print('Média geral = ', df_selic['valor'].mean())
print('Média de janeiro de 2019 = ', df_janeiro_2019['valor'].mean())
print('Média de janeiro de 2020 = ', df_janeiro_2020['valor'].mean(), '\n')

#fim do teste de extração de dados
