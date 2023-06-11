import pandas as pd
import numpy as np
import math
import json

#limpieza de datos
def clean_data(df_superstore):
    df_superstore['Sales'] = df_superstore['Sales'].str.replace(",", ".", regex=False).astype("float")
    df_superstore['Profit'] = df_superstore['Profit'].str.replace(",", ".", regex=False).astype("float")
    return df_superstore

#dataframe para gráfico de barras
def bar_data(df_bar):
    df_bar = df_bar.groupby('Category').agg(Ventas=('Sales', 'sum'), Ganancia=('Profit', 'sum')).sort_values('Ventas', ascending=False).reset_index()
    return df_bar

#dataframe para gráfico de líneas
def click_data(df_click):
    df_click['Anio'] = pd.to_datetime(df_click['Order Date'], format='%d/%m/%Y').dt.strftime('%Y-%m')
    df_click = df_click.groupby(['Anio', 'Category']).agg(Ventas=('Sales', 'sum'), Ganancia=('Profit', 'sum')).pivot_table(index='Anio', columns='Category', values=['Ventas', 'Ganancia'])
    return df_click

#dataframe para gráfico de headmap
def hot_map(df_hot_map):
    df_hot_map['Order Date'] = pd.to_datetime(df_hot_map['Order Date'], format='%d/%m/%Y')
    df_hot_map['Anio'] = df_hot_map['Order Date'].dt.year.astype(str)
    df_hot_map = df_hot_map.groupby(['Anio', 'Customer Name']).agg(Sales_sum=('Sales', 'sum')).reset_index()
    return df_hot_map

#dataframe para gráfico de barras Q
def bar_Q(df_bar_q):
    df_bar_q['Fecha'] = pd.to_datetime(df_bar_q['Order Date'], format='%d/%m/%Y')
    df_bar_q = df_bar_q.groupby(pd.Grouper(key='Fecha', freq='Q')).agg(Ventas=('Sales', 'sum')).reset_index()
    df_bar_q['Ventas'] = df_bar_q['Ventas'].round(0)
    df_bar_q['Trimestre'] = df_bar_q['Fecha'].dt.quarter
    return df_bar_q

#dataframe para gráfico de barras productos
def top_3(df_top_3):
    df_top_3 = df_top_3.groupby(['Product Name']).agg(conteo_ventas=('Sales', 'count'))
    df_top_3 = df_top_3.sort_values(['conteo_ventas'], ascending=[False]).reset_index()
    df_top_3 = df_top_3.set_index('Product Name')
    return df_top_3