############################################################
### Filtro e classificação por condições ###################
############################################################

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# carregar database total (excel nesse caso)

df = pd.read_excel('database.xlsx')

# cliente devendo mais de $ 500

clientes_quita = df[df['saldo em cc'] <= -500]
clientes_quita = clientes_quita.sort_values(by="saldo em cc", ascending=True)


## 1 relação de clientes para ação de cobrança

clientes_cobranca = clientes_quita[clientes_quita['valor em aplicacoes curto prazo'] == 0]
del clientes_cobranca['moradia']
del clientes_cobranca['Estado civil']
del clientes_cobranca['renda']
del clientes_cobranca['valor em aplicacoes curto prazo']
del clientes_cobranca['valor em aplicacoes longo prazo']

## 2 levantar o saldo após utilização das aplicações de curto prazo caírem na conta dos cliente

clientes_saldo_quit = clientes_quita[clientes_quita['valor em aplicacoes curto prazo'] != 0]
clientes_saldo_quit['valor com liquidez antecipada']=clientes_saldo_quit['valor em aplicacoes curto prazo']*0.9
clientes_saldo_quit['saldo final'] = clientes_saldo_quit['valor com liquidez antecipada'] + clientes_saldo_quit['saldo em cc']
clientes_saldo_quit = clientes_saldo_quit.sort_values(by="saldo final", ascending=False)
del clientes_saldo_quit['moradia']
del clientes_saldo_quit['renda']
del clientes_saldo_quit['idade']
del clientes_saldo_quit['Estado civil']
del clientes_saldo_quit['valor em aplicacoes longo prazo']


## 3 montar relação de clientes para oferta de seguro "casais"

df_saldo_min = df[df['saldo em cc'] > -500]
casados = df_saldo_min[df_saldo_min['Estado civil'] == 'casado']
elegiveis_casados = casados[casados['idade'].between(35,75)]

elegiveis_casados = elegiveis_casados.sort_values(by="idade", ascending=False)
del elegiveis_casados['moradia']
del elegiveis_casados['valor em aplicacoes curto prazo']
del elegiveis_casados['valor em aplicacoes longo prazo']
del elegiveis_casados['renda']

sns.set_style('dark')
sns.histplot(elegiveis_casados['idade'],
             fill=False,
             element='step',
             legend='clientes elegiveis seguro pessoal').set_title('Distribuição Clientes elegíveis para seguro residencial')


## 4 montar relação de clientes para oferta de seguro residencial

seguro = df_saldo_min[df_saldo_min['moradia'] == 'propria']
elegiveis_seguro = seguro[seguro['idade'] > 25]
del elegiveis_seguro['valor em aplicacoes curto prazo']
del elegiveis_seguro['valor em aplicacoes longo prazo']
del elegiveis_seguro['Estado civil']
del elegiveis_seguro['renda']


## 5 calcular valor para o banco do empréstimo e valor a ser liberado

df_saldo_min['valor cred']=df_saldo_min['valor em aplicacoes longo prazo']*0.9
del df_saldo_min['valor em aplicacoes curto prazo']
del df_saldo_min['Estado civil']
del df_saldo_min['idade']
del df_saldo_min['moradia']
del df_saldo_min['renda']

clientes_cobranca.to_excel("clientes_cobranca.xlsx")
clientes_saldo_quit.to_excel("clientes_apos_apli_curt_pzo.xlsx")
elegiveis_casados.to_excel("oferta_casados.xlsx")
elegiveis_seguro.to_excel("oferta_seguro.xlsx")
df_saldo_min.to_excel("oferta_credito.xlsx")



