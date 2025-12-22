
from prophet import Prophet

class PrevisaoDemanda:
    def __init__(self, vendas_df):
        self.vendas = vendas_df

    def prever(self, produto, dias=10):
        df = self.vendas[self.vendas["produto"] == produto]
        df = df.groupby("data")["vendido"].sum().reset_index()
        df = df.rename(columns={"data": "ds", "vendido": "y"})

        if len(df) < 2:
            return df["y"].mean() * dias

        modelo = Prophet(weekly_seasonality=True, yearly_seasonality=True)
        modelo.fit(df)

        futuro = modelo.make_future_dataframe(periods=dias)
        previsao = modelo.predict(futuro)

        return previsao.tail(dias)["yhat"].clip(lower=0).sum()

