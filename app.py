import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title='DatArtistas: ICFESViz',
                   layout='wide', page_icon="logoMIAD.jpg")
@st.cache_data
def cargar_datos():
    df = pd.read_csv("Base_visualizacion_icfes.csv")
    return df

df = cargar_datos()

@st.cache_data
def hacer_heatmap(df: pd.DataFrame, x: str, y: str):
    data = (
        df.reset_index()[[x,y, 'index']]
            .groupby([x,y])
            .count()
            .reset_index()
            .pivot(x,y, "index")
            .fillna(0)
    )

    fig = px.imshow(
        data,
        color_continuous_scale="Blues",
        aspect="auto",
        title=f"Heatmap {x} vs {y}"
    )

    fig.update_traces(
        hovertemplate = "<b><i>" +
        x +"</b></i>: %{y} <br> <b><i>" +
        y + "</b></i>: %{x} <br> <b><i>"
        + "</b></i><b><i>Conteo de la interacción entre variables: </b></i> %{z} <extra></extra>"


    )

    return fig

st.sidebar.image("logoMIAD.jpg")

columnas=[x for x in list(df.columns) if x not in ['Unnamed: 0',
                                                   'COLE_COD_DANE',
                                                   'Cod_Municipio',
                                                   'Cod_Departamento',
                                                   'Nombre_Colegio', 'Municipio']]

eje1heatmap = st.sidebar.selectbox(label="Opción 1 heatmap", options=columnas)

columnas2 = columnas.copy()
columnas2.pop(columnas.index(eje1heatmap))
eje2heatmap = st.sidebar.selectbox(label="Opción 2 heatmap", options=columnas2)


col1, col2 = st.columns(2)


columnas3 = columnas.copy()

seleccionbar = st.sidebar.selectbox(label="Selecciona la variable a visualizar en el barchart", options=columnas3)



@st.cache_data
def barchart(df, x):
    data = (df.reset_index()
    .groupby([x])
    .nunique()
    .reset_index()
    .sort_values(by='index', ascending=True)[[x, 'index']].copy())
    string = f"Cantidad de cada nivel de {x}"
    data=  data.rename(columns= {'index': string})
    fig= px.bar(data, y=x, x=string, orientation='h')
    return fig


col1.header(f"Gráfico de barras de {seleccionbar}")
col1.plotly_chart(barchart(df, seleccionbar), use_container_width=True)
col2.header(f"Heampat de {eje1heatmap} vs {eje2heatmap}")
col2.plotly_chart(hacer_heatmap(df,eje1heatmap, eje2heatmap), use_container_width=True)
'''

import base64

@st.cache_data
def cargar_pdf():

    with open("ejemplo.pdf", "rb") as file:
        pdf64=base64.b64encode(file.read()).decode('utf-8')

    pdf_text=f'<embed src="data:application/pdf;base64,{pdf64}" type="application/pdf"' \
             f' width= "1200" height="600">'
    return pdf_text
pdf_show = cargar_pdf()

st.header("Documentación: ")
st.markdown("### PDF de los datos originales: ")

st.markdown(pdf_show, unsafe_allow_html=True)'''
