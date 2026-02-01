"""
Tab de Vista de Datos
"""
import streamlit as st
import pandas as pd
from datetime import datetime


def mostrar_tab_datos(df_filtrado):
    """
    Muestra el tab de vista de datos con búsqueda y descarga
    
    Args:
        df_filtrado: DataFrame filtrado
    """
    st.header("Vista de Datos")
    
    # Información general
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total de Filas", len(df_filtrado))
    
    with col2:
        st.metric("Total de Columnas", len(df_filtrado.columns))
    
    with col3:
        memoria_mb = df_filtrado.memory_usage(deep=True).sum() / 1024**2
        st.metric("Tamaño en Memoria", f"{memoria_mb:.2f} MB")
    
    st.markdown("---")
    
    # Búsqueda y filtrado
    st.subheader("🔍 Búsqueda en los Datos")
    
    col_busqueda, col_columna = st.columns([2, 1])
    
    with col_busqueda:
        busqueda = st.text_input(
            "Buscar en todas las columnas", 
            "", 
            placeholder="Escribe para buscar...",
            help="Busca texto en todas las columnas del DataFrame"
        )
    
    with col_columna:
        columnas_disponibles = ['Todas'] + df_filtrado.columns.tolist()
        columna_busqueda = st.selectbox(
            "Buscar en columna específica",
            columnas_disponibles,
            help="Selecciona una columna específica para buscar"
        )
    
    # Aplicar búsqueda
    df_mostrar = df_filtrado.copy()
    
    if busqueda:
        if columna_busqueda == 'Todas':
            # Buscar en todas las columnas
            mask = df_mostrar.astype(str).apply(
                lambda x: x.str.contains(busqueda, case=False, na=False)
            ).any(axis=1)
            df_mostrar = df_mostrar[mask]
        else:
            # Buscar en columna específica
            mask = df_mostrar[columna_busqueda].astype(str).str.contains(
                busqueda, case=False, na=False
            )
            df_mostrar = df_mostrar[mask]
        
        st.info(f"✅ Se encontraron {len(df_mostrar)} resultados para '{busqueda}'")
    
    # Opciones de visualización
    st.markdown("---")
    st.subheader("⚙️ Opciones de Visualización")
    
    col_opciones1, col_opciones2, col_opciones3 = st.columns(3)
    
    with col_opciones1:
        mostrar_index = st.checkbox("Mostrar índice", value=True)
    
    with col_opciones2:
        num_filas = st.number_input(
            "Número de filas a mostrar",
            min_value=10,
            max_value=len(df_mostrar),
            value=min(100, len(df_mostrar)),
            step=10
        )
    
    with col_opciones3:
        ordenar_por = st.selectbox(
            "Ordenar por columna",
            ['Sin ordenar'] + df_mostrar.columns.tolist()
        )
    
    # Aplicar ordenamiento
    if ordenar_por != 'Sin ordenar':
        orden_ascendente = st.radio(
            "Orden",
            ['Ascendente', 'Descendente'],
            horizontal=True
        )
        df_mostrar = df_mostrar.sort_values(
            by=ordenar_por,
            ascending=(orden_ascendente == 'Ascendente')
        )
    
    # Mostrar datos
    st.markdown("---")
    st.subheader("📋 Datos Filtrados")
    
    if mostrar_index:
        st.dataframe(df_mostrar.head(num_filas), use_container_width=True, height=400)
    else:
        st.dataframe(df_mostrar.head(num_filas).reset_index(drop=True), use_container_width=True, height=400)
    
    if len(df_mostrar) > num_filas:
        st.caption(f"Mostrando {num_filas} de {len(df_mostrar)} filas. Ajusta el número arriba para ver más.")
    
    # Información de columnas
    st.markdown("---")
    st.subheader("📊 Información de Columnas")
    
    info_columnas = []
    for col in df_mostrar.columns:
        info_columnas.append({
            'Columna': col,
            'Tipo': str(df_mostrar[col].dtype),
            'No Nulos': df_mostrar[col].notna().sum(),
            'Nulos': df_mostrar[col].isna().sum(),
            '% Nulos': f"{(df_mostrar[col].isna().sum() / len(df_mostrar) * 100):.2f}%",
            'Únicos': df_mostrar[col].nunique()
        })
    
    df_info = pd.DataFrame(info_columnas)
    st.dataframe(df_info, use_container_width=True)
    
    # Descarga de datos
    st.markdown("---")
    st.subheader("💾 Descargar Datos")
    
    col_desc1, col_desc2 = st.columns(2)
    
    with col_desc1:
        # Descargar como CSV
        csv = df_mostrar.to_csv(index=mostrar_index).encode('utf-8')
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        st.download_button(
            label="📥 Descargar como CSV",
            data=csv,
            file_name=f"datos_filtrados_{timestamp}.csv",
            mime="text/csv",
            help="Descarga los datos filtrados en formato CSV"
        )
    
    with col_desc2:
        # Descargar como Excel
        from io import BytesIO
        
        buffer = BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            df_mostrar.to_excel(writer, index=mostrar_index, sheet_name='Datos')
        
        st.download_button(
            label="📥 Descargar como Excel",
            data=buffer.getvalue(),
            file_name=f"datos_filtrados_{timestamp}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            help="Descarga los datos filtrados en formato Excel"
        )
    
    # Estadísticas rápidas
    st.markdown("---")
    st.subheader("📈 Estadísticas Rápidas")
    
    # Solo columnas numéricas
    numeric_cols = df_mostrar.select_dtypes(include=['number']).columns.tolist()
    
    if numeric_cols:
        col_stats = st.selectbox("Selecciona columna para ver estadísticas", numeric_cols, key='stats_col')
        
        col_stat1, col_stat2, col_stat3, col_stat4, col_stat5 = st.columns(5)
        
        with col_stat1:
            st.metric("Media", f"{df_mostrar[col_stats].mean():.2f}")
        
        with col_stat2:
            st.metric("Mediana", f"{df_mostrar[col_stats].median():.2f}")
        
        with col_stat3:
            st.metric("Desv. Est.", f"{df_mostrar[col_stats].std():.2f}")
        
        with col_stat4:
            st.metric("Mínimo", f"{df_mostrar[col_stats].min():.2f}")
        
        with col_stat5:
            st.metric("Máximo", f"{df_mostrar[col_stats].max():.2f}")
        
        # Histograma
        import plotly.express as px
        
        fig_hist = px.histogram(
            df_mostrar,
            x=col_stats,
            title=f'Distribución de {col_stats}',
            nbins=30,
            marginal='box'
        )
        st.plotly_chart(fig_hist, use_container_width=True)
    else:
        st.info("No hay columnas numéricas para mostrar estadísticas")