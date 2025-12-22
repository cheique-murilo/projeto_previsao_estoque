class EstoqueManager:
    def __init__(self, estoque_df):
        self.estoque = estoque_df

    def aplicar_vendas(self, vendas_df, data):
        vendas_dia = vendas_df[vendas_df["data"] == data]
        agrupado = vendas_dia.groupby("produto")["vendido"].sum().reset_index()

        self.estoque = self.estoque.merge(agrupado, on="produto", how="left")
        self.estoque["vendido"] = self.estoque["vendido"].fillna(0)
        self.estoque["quantidade"] -= self.estoque["vendido"]
        self.estoque.drop(columns=["vendido"], inplace=True)

    def aplicar_compras(self, compras_df, data):
        compras_dia = compras_df[compras_df["data_entrega"] == data]

        if compras_dia.empty:
            return

        compras_agrupadas = compras_dia.groupby("produto")["quantidade"].sum().reset_index()
        compras_agrupadas = compras_agrupadas.rename(columns={"quantidade": "comprados"})

        self.estoque = self.estoque.merge(compras_agrupadas, on="produto", how="left")
        self.estoque["comprados"] = self.estoque["comprados"].fillna(0)
        self.estoque["quantidade"] += self.estoque["comprados"]
        self.estoque.drop(columns=["comprados"], inplace=True)

