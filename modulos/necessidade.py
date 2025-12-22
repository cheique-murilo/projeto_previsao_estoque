class NecessidadeCompras:
    def __init__(self, estoque_df, compras_df, fornecedores_df):
        self.estoque = estoque_df
        self.compras = compras_df
        self.fornecedores = fornecedores_df

    def calcular(self, produto, demanda_prevista, dias_estoque_alvo=15):
        estoque_atual = float(self.estoque.loc[self.estoque["produto"] == produto, "quantidade"])

        compras_futuras = self.compras[
            (self.compras["produto"] == produto) &
            (self.compras["data_entrega"] > self.compras["data_entrega"].max())
        ]["quantidade"].sum()

        estoque_projetado = estoque_atual + compras_futuras
        estoque_alvo = demanda_prevista

        necessidade = max(estoque_alvo - estoque_projetado, 0)

        return necessidade
