import streamlit as st
from streamlit_echarts import st_echarts
from streamlit_echarts import JsCode
import pandas as pd
import altair as alt
import numpy as np
import math
import json
import functions as f

def main():

    df_superstore = pd.read_csv("./dataset/superstore.csv",sep=";")

    df_superstore_clean = f.clean_data(df_superstore.copy()) # Limpieza de dataframe

    df_options = f.bar_data(df_superstore_clean.copy()) # Gráfico de barras

    df_clicked_label = f.click_data(df_superstore_clean.copy()) # Gráfico de lineas

    df_heatmap_cartesian = f.hot_map(df_superstore_clean.copy()) # Gráfico de headmap
    

    ###Logaritmo para Headmap
    df_grouped = df_heatmap_cartesian.groupby("Customer Name")["Sales_sum"].sum()
    df_sorted = df_grouped.sort_values(ascending=False)
    top_5_customers = df_sorted.head(5)
    top_5_customers_names = top_5_customers.index.tolist()

    df_filtered_customer = df_heatmap_cartesian[df_heatmap_cartesian["Customer Name"].isin(top_5_customers_names)]

    anios_list = sorted(set(df_filtered_customer["Anio"]))
    anios_list.append("Total")

    pivot_table = df_filtered_customer.pivot_table(index="Customer Name", columns="Anio", values="Sales_sum", aggfunc="sum", fill_value=0)
    pivot_table["Total"] = pivot_table.sum(axis=1)

    pivot_table = pivot_table.sort_values(by="Total", ascending=False)
    desglosado_df = pd.DataFrame(pivot_table.to_records())

    data = []
    for customer_idx, customer in enumerate(top_5_customers_names):
        for year_idx, year in enumerate(range(2014, 2018)):
            sales = desglosado_df.loc[desglosado_df["Customer Name"] == customer, str(year)].values[0]
            data.append([customer_idx, year_idx, round(sales)])
        total_sales = pivot_table.loc[customer, "Total"]
        data.append([customer_idx, len(range(2014, 2018)), round(total_sales)])  # Agregar el total al final de cada cliente
    
    
    df_q = f.bar_Q(df_superstore_clean.copy()) # Gráfico de barras Q1,Q2,Q3,Q4

    ###Logaritmo para barras Q1,Q2,Q3,Q4
    pivot_table = df_q.pivot_table(values="Ventas", index=df_q["Fecha"].dt.year, columns="Trimestre", aggfunc="sum")
    matriz_q = [["Anio", "Q1", "Q2", "Q3", "Q4"]]

    for index, row in pivot_table.iterrows():
        fila = [str(index)]
        fila.extend(row)
        matriz_q.append(fila)

    
    df_bar_top_3 = f.top_3(df_superstore_clean.copy()) # Gráfico de barras productos

    ###Logaritmo para barras productos
    top_3_products = df_bar_top_3.head(3)
    matriz_top_3 = [["Producto", "No. Ventas"]]
    for index_top_3, row_3 in top_3_products.iterrows():
        fila_3 = [str(index_top_3)]
        fila_3.extend(row_3.values.tolist())
        matriz_top_3.append(fila_3)


    head.markdown("<h3 style='text-align: center;'>Ventas y Ganancia X Categoría de Productos 🛍️</h3>", unsafe_allow_html=True)
    head.text("➡️ Mueve el mouse encima de las barras para obtener más información.")

    with col3:
        head2.divider()
        
        st.markdown("<h3 style='text-align: center;'>Top 5 - clientes valiosos 👏</h3>", unsafe_allow_html=True)
        st.text("➡️ Clientes que más rentabilidad ha dejado a la empresa x año.")

        data = [[d[1], d[0], d[2] if d[2] != 0 else "-"] for d in data]

        heatmap_d = {
            "tooltip": {"position": "top"},
            "grid": {"height": "50%", "top": "10%", "left": "30%"},
            "xAxis": {"type": "category", "data": anios_list, "splitArea": {"show": True}},
            "yAxis": {"type": "category", "data": top_5_customers_names, "splitArea": {"show": True}},
            "visualMap": {
                "min": 0,
                "max": 30000,
                "calculable": True,
                "orient": "horizontal",
                "left": "center",
                "bottom": "15%",
                "color": ["#AB5A35", "#FFDBAA"],  # Personaliza los colores de la escala
            },
            "series": [
                {
                    "type": "heatmap",
                    "data": data,
                    "label": {
                        "show": True,
                        "formatter": JsCode("function(params) { return params.value[2].toLocaleString('en-US'); }").js_code,
                    },
                    "emphasis": {"itemStyle": {"shadowBlur": 10, "shadowColor": "rgba(0, 0, 0, 0.5)"}},
                }
            ],
        }

        st_echarts(heatmap_d, height="500px", width="100%")

    with col4:
        st.markdown("<h3 style='text-align: center;'>Top 3 - Productos más vendidos 💣</h3>", unsafe_allow_html=True)
        st.text("➡️ Productos con más cantidad de ventas en toda la historia.")

        top_3_bar = {
            "dataset": {
                "source": matriz_top_3
            },
            "xAxis": {
                "type": "category",
            },
            "yAxis": {
                "type": "value",
                "min": 40, 
                "max": 50,
                "name": "No. de ventas",
            },
            "series": [
                {
                "type": "bar",
                "showBackground": True,
                "backgroundStyle": {
                    "color": "rgba(180, 180, 180, 0.2)"
                },
                
                "label": {
                    "show": True,
                    "position": "top"
                },
                "itemStyle": {
                    "color": JsCode("function(params) {var colors = ['#F5847F', '#AB57A3', '#FFDBAA']; return colors[params.dataIndex];}").js_code,
                }
                }
                
            ]
        }

        st_echarts(top_3_bar, height="500px", width="100%")

    with st.container():
        head3.divider()
        
        st.markdown("<h3 style='text-align: center;'>Trimestre con más Ventas 🍰</h3>", unsafe_allow_html=True)
        st.text("➡️ Cada trimestre se representa como Q.")

        option_q = {
            "legend": {},
            "tooltip": {},
            "dataset": {
                "source": matriz_q
            },
            "xAxis": { "type": "category" },
            "yAxis": {},
            
            "series": [{ "type": "bar",
                        "label": {
                            "show": True,
                            "position": "top",
                            "formatter": JsCode("function(params) { return params.value[1].toLocaleString('en-US'); }").js_code,
                        },
                        "itemStyle": {"color": "#B167FC"}, 
                        }, 
                       { "type": "bar",
                        "label": {
                            "show": True,
                            "position": "top",
                            "formatter": JsCode("function(params) { return params.value[2].toLocaleString('en-US'); }").js_code,
                        }, 
                        "itemStyle": {"color": "#F772EC"},
                        }, 
                       { "type": "bar",
                        "label": {
                            "show": True,
                            "position": "top",
                            "formatter": JsCode("function(params) { return params.value[3].toLocaleString('en-US'); }").js_code,
                        },
                        "itemStyle": {"color": "#E05C93"},
                         },
                 
                       { "type": "bar",
                        "label": {
                            "show": True,
                            "position": "top",
                            "formatter": JsCode("function(params) { return params.value[4].toLocaleString('en-US'); }").js_code,
                        }, 
                        "itemStyle": {"color": "#FC6B67"},
                        }]
        }
        st_echarts(option_q, height="400px", width="100%")
   
    with col1:
        options = {
            "tooltip": {"trigger": "axis", "axisPointer": {"type": "shadow"}},
            "legend": {
                "data": ["Ventas", "Ganancia"]
            },
            "grid": {"left": "3%", "right": "4%", "bottom": "3%", "containLabel": True},
            "yAxis": {"type": "value"},
            "xAxis": {
                "type": "category",
                "data": df_options["Category"].values.tolist(),
            },
            "series": [
                {
                    "name": "Ventas",
                    "type": "bar",
                    "stack": "Total",
                    "label": {"show": True, 
                              "position": "inside",
                              "formatter": JsCode("function(params) { return params.value.toLocaleString('en-US'); }").js_code,
                              },
                    "emphasis": {"focus": "series"},
                    "data": df_options["Ventas"].values.round(0).tolist(),
                    "itemStyle": {"color": "#AB57A3"},
                },
                {
                    "name": "Ganancia",
                    "type": "bar",
                    "stack": "SubTotal",
                    "label": {"show": True, 
                              "position": "inside",
                              "formatter": JsCode("function(params) { return params.value.toLocaleString('en-US'); }").js_code,
                              },
                    "emphasis": {"focus": "series"},
                    "data": df_options["Ganancia"].values.round(0).tolist(),
                    "itemStyle": {"color": "#F772EB"},
                    "barGap": "-100%",                
                }                
            ],
        }
        
            
        clicked_label = st_echarts(
            options=options,
            events={"mouseover": "function(params) {return params.name}"},
            height="400px",
            key="global",
            width="100%"
        )

        if clicked_label is None:
            return
            
    with col2:
        st.divider()

        filtered_df = df_clicked_label["Ventas", clicked_label].round(0).sort_index()
        filtered_df_g = df_clicked_label["Ganancia", clicked_label].round(0).sort_index()
        
        
        line_options = {
            "legend": {
                "data": ["Ventas", "Ganancia"],
                "top": "bottom"
            },
            "title": {"text": f"Exploración de {{a|{clicked_label}}} a lo largo del tiempo 📅",
                "left": "center",
                "textStyle": {
                    "fontSize": "17",
                    "rich": {
                        "a": {
                            "fontSize": "17",
                            "color": "#AB57A3",
                            "fontWeight": "bold",
                        },
                    },
                },
            },
            "xAxis": {
                "type": "category",
                "axisTick": {"alignWithLabel": True},
                "data": filtered_df.index.values.tolist(),
            },
            "yAxis": {"type": "value"},
            "tooltip": {"trigger": "axis"},
            "series": [
                {
                    "name":"Ventas",
                    "data": filtered_df.tolist(),
                    "type": "line",
                    "smooth": True,
                    "itemStyle": {"color": "#AB57A3"},
                    "lineStyle": {"color": "#AB57A3"},
                    
                },
                {
                    "name":"Ganancia",
                    "data": filtered_df_g.tolist(),
                    "type": "line",
                    "smooth": True,
                    "itemStyle": {"color": "#F772EB"},
                    "lineStyle": {"color": "#F772EB"},
                }
            ],
        }

                                
        clicked_label = st_echarts(line_options, key="detail", width="100%")
    

if __name__ == "__main__":
    st.set_page_config(
    page_title="Dashboard Super Store",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded")

    st.markdown("<h1 style='text-align: center;'>Dashboard Super Store 📊</h1>", unsafe_allow_html=True)

    head = st.container()
    col1, col2 = st.columns([4,3])
    head2 = st.container()
    col3, col4 = st.columns([3,3])
    head3 = st.container()
    col5, col6 = st.columns([7,1])
    main()