import streamlit as st  # biblioteca construir dashboards
import pandas as pd  # panda manipula os dados
import plotly.express as px  # construir os graficos

st.set_page_config(layout="wide")  # largura da pagina

df = pd.read_excel("dataset.xlsx")

df["Data_Pedido"] = pd.to_datetime(df["Data_Pedido"], dayfirst=True)  
# data_pedido nome da coluna esta no excel
df = df.sort_values("Data_Pedido")

# Month converte essas datas em um formato de string simplificado que combina o ano e o mês, ignorando o dia.
df["Month"] = df["Data_Pedido"].apply(lambda x: str(x.year) + "-" + str(x.month))
month = st.sidebar.selectbox("Mês", df["Month"].unique())

df_filtered = df[df["Month"] == month]


col1, col2 = st.columns(2)
col3, col4, col5 = st.columns(3)

fig_date = px.bar(
    df_filtered,
    x="Data_Pedido",
    y="Total_Vendas",
    color="Categoria",
    title="Faturamento Por Dia",
)
col1.plotly_chart(fig_date)

fig_prod = px.bar(
    df_filtered,
    x="Data_Pedido",
    y="SubCategoria",
    color="Categoria",
    title="Faturamento Por tipo de produto",
    orientation="h",
)
col2.plotly_chart(fig_prod)

# Agrupar e somar vendas por país, ordenando pelo total de vendas
city_total = (
    df_filtered.groupby("Pais")[["Total_Vendas"]]
    .sum()
    .reset_index()
    .sort_values("Total_Vendas", ascending=False)
)

# Criar gráfico de barras com cores diferenciadas
fig_city = px.bar(
    city_total,
    x="Pais",
    y="Total_Vendas",
    title="Faturamento Por País",
    color="Pais",
    color_discrete_sequence=px.colors.qualitative.Set2,  # Esquema de cores
)

# Personalizar o layout do gráfico
fig_city.update_layout(
    xaxis_title="País",
    yaxis_title="Faturamento Total (R$)",
    margin=dict(l=40, r=40, t=50, b=40),
    legend_title="Países",
)

# Exibir o gráfico no Streamlit
col3.plotly_chart(fig_city)


fig_kind = px.pie(
    df_filtered,
    values="Total_Vendas",
    names="Categoria",
    title="Produtos estão dando Lucros",
)
col4.plotly_chart(fig_kind)

df_filtered

# `streamlit run dashboards.py` run para rodda o codigo