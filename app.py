import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# Configuración de la página
st.set_page_config(page_title="Dashboard KPIs", layout="wide")

# Título
st.title("📊 Dashboard de KPIs")

# Sidebar para cargar archivo
st.sidebar.header("Cargar datos")
uploaded_file = st.sidebar.file_uploader("Sube tu archivo Excel", type=['xlsx', 'xls'])

if uploaded_file is not None:
    # Leer el archivo Excel
    df = pd.read_excel(uploaded_file)
    
    # Mostrar información básica
    st.sidebar.success(f"✅ Archivo cargado: {uploaded_file.name}")
    st.sidebar.info(f"Filas: {len(df)} | Columnas: {len(df.columns)}")
    
    # Tabs para organizar el contenido
    tab1, tab2, tab3 = st.tabs(["📈 KPIs Principales", "📊 Análisis", "📋 Datos"])
    
    with tab1:
        st.header("KPIs Principales")
        
        # Ejemplo de métricas (ajusta según tus columnas)
        col1, col2, col3, col4 = st.columns(4)
        
        # Aquí calculas tus KPIs - ejemplo genérico:
        if len(df.select_dtypes(include=['number']).columns) > 0:
            numeric_cols = df.select_dtypes(include=['number']).columns
            
            with col1:
                st.metric("Total Registros", len(df))
            
            with col2:
                if len(numeric_cols) > 0:
                    st.metric(f"Suma {numeric_cols[0]}", f"{df[numeric_cols[0]].sum():,.0f}")
            
            with col3:
                if len(numeric_cols) > 1:
                    st.metric(f"Promedio {numeric_cols[1]}", f"{df[numeric_cols[1]].mean():,.2f}")
            
            with col4:
                if len(numeric_cols) > 0:
                    st.metric(f"Máximo {numeric_cols[0]}", f"{df[numeric_cols[0]].max():,.0f}")
    
    with tab2:
        st.header("Análisis Detallado")
        
        # Selector de columnas para graficar
        numeric_columns = df.select_dtypes(include=['number']).columns.tolist()
        
        if numeric_columns:
            col1, col2 = st.columns(2)
            
            with col1:
                selected_col = st.selectbox("Selecciona columna para gráfico", numeric_columns)
                
                # Gráfico de barras
                fig = px.bar(df.head(20), y=selected_col, title=f"Top 20 - {selected_col}")
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                if len(numeric_columns) > 1:
                    selected_col2 = st.selectbox("Selecciona otra columna", numeric_columns, index=1)
                    
                    # Gráfico de línea
                    fig2 = px.line(df.head(20), y=selected_col2, title=f"Tendencia - {selected_col2}")
                    st.plotly_chart(fig2, use_container_width=True)
        
        # Estadísticas descriptivas
        st.subheader("Estadísticas Descriptivas")
        st.dataframe(df.describe(), use_container_width=True)
    
    with tab3:
        st.header("Vista de Datos")
        
        # Filtros
        st.subheader("Filtrar datos")
        
        # Mostrar datos con opción de búsqueda
        search = st.text_input("🔍 Buscar en los datos")
        
        if search:
            mask = df.astype(str).apply(lambda x: x.str.contains(search, case=False, na=False)).any(axis=1)
            filtered_df = df[mask]
        else:
            filtered_df = df
        
        st.dataframe(filtered_df, use_container_width=True, height=400)
        
        # Botón para descargar datos procesados
        csv = filtered_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Descargar datos filtrados (CSV)",
            data=csv,
            file_name=f"kpis_procesados_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )

else:
    st.info("👈 Por favor, sube un archivo Excel desde la barra lateral para comenzar")
    
    # Instrucciones
    st.markdown("""
    ### 📝 Instrucciones:
    1. Sube tu archivo Excel usando el botón en la barra lateral
    2. Los KPIs se calcularán automáticamente
    3. Explora las diferentes pestañas para ver análisis y datos
    
    ### 🎯 Características:
    - ✅ Carga automática de datos
    - ✅ KPIs calculados en tiempo real
    - ✅ Gráficos interactivos
    - ✅ Filtrado y búsqueda de datos
    - ✅ Descarga de resultados procesados
    """)