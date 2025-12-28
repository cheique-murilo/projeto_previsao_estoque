import pandas as pd

from modulos.consumo import ConsumoMedio
from modulos.previsao import PrevisaoDemanda
from modulos.necessidade import NecessidadeCompras
from modulos.estoque import EstoqueManager

# ============================================================
# 1. CARREGAR DADOS
# ============================================================

estoque = pd.read_csv("dados/estoque.csv")
vendas = pd.read_csv("dados/vendas.csv", parse_dates=["Data"])
compras = pd.read_csv("dados/compras.csv", parse_dates=["Data_Entrega"])
fornecedores = pd.read_csv("dados/fornecedores.csv")

# Normalizar nomes das colunas
estoque.columns = estoque.columns.str.lower()
vendas.columns = vendas.columns.str.lower()
compras.columns = compras.columns.str.lower()
fornecedores.columns = fornecedores.columns.str.lower()

ultima_data = vendas["data"].max()

# ============================================================
# 2. INSTANCIAR CLASSES
# ============================================================

consumo = ConsumoMedio(vendas)
previsao = PrevisaoDemanda(vendas)
necessidade = NecessidadeCompras(estoque, compras, fornecedores)
estoque_manager = EstoqueManager(estoque)

# ============================================================
# 3. RELATÓRIO DE CONSUMO MÉDIO (7/30/90 DIAS)
# ============================================================

consumo_relatorio = []

for produto in estoque["produto"]:
    consumo_7 = consumo.consumo(produto, 7)
    consumo_30 = consumo.consumo(produto, 30)
    consumo_90 = consumo.consumo(produto, 90)
    tendencia = consumo.tendencia(produto)

    consumo_relatorio.append([
        produto,
        round(consumo_7, 2),
        round(consumo_30, 2),
        round(consumo_90, 2),
        tendencia
    ])

df_consumo = pd.DataFrame(consumo_relatorio, columns=[
    "Produto", "Consumo_7", "Consumo_30", "Consumo_90", "Tendencia"
])

df_consumo.to_csv("consumo_medio.csv", index=False,  decimal=",")
print("📊 Relatório de consumo médio gerado: data/consumo_medio.csv")

# ============================================================
# 4. ATUALIZAR ESTOQUE (VENDAS + COMPRAS)
# ============================================================

estoque_manager.aplicar_vendas(vendas, ultima_data)
estoque_manager.aplicar_compras(compras, ultima_data)

estoque_atualizado = estoque_manager.estoque
estoque_atualizado.to_csv("estoque_atualizado.csv", index=False, decimal=",")
print("📦 Estoque atualizado salvo em: data/estoque_atualizado.csv")

# ============================================================
# 5. PREVISÃO DE DEMANDA + NECESSIDADE DE COMPRAS
# ============================================================

resultados = []

for produto in estoque_atualizado["produto"]:
    demanda_prevista = previsao.prever(produto, dias=10)
    qtd_comprar = necessidade.calcular(produto, demanda_prevista)

    resultados.append([
        produto,
        round(demanda_prevista, 2),
        round(qtd_comprar, 2)
    ])

df_necessidade = pd.DataFrame(resultados, columns=[
    "Produto", "Demanda_10_Dias", "Quantidade_Sugerida"
])

df_necessidade.to_csv("necessidade_compras.csv", index=False, decimal=",")
print("🛒 Necessidade de compras gerada: data/necessidade_compras.csv")

print("\n✅ Pipeline completo executado com sucesso!")

