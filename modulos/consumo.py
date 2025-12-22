import pandas as pd
from sklearn.linear_model import LinearRegression

class ConsumoMedio:
    def __init__(self, vendas_df):
        self.vendas = vendas_df

    def consumo(self, produto, dias):
        limite = self.vendas["data"].max() - pd.Timedelta(days=dias)
        df = self.vendas[
            (self.vendas["produto"] == produto) &
            (self.vendas["data"] >= limite)
        ]
        return df["vendido"].sum() / dias if len(df) else 0

    def tendencia(self, produto):
        df = self.vendas[self.vendas["produto"] == produto]
        if len(df) < 3:
            return "Estável"

        df = df.sort_values("data")
        df["dia"] = (df["data"] - df["data"].min()).dt.days

        modelo = LinearRegression()
        modelo.fit(df[["dia"]], df["vendido"])
        slope = modelo.coef_[0]

        if slope > 0.1:
            return "Subindo"
        elif slope < -0.1:
            return "Caindo"
        return "Estável"
