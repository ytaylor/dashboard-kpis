"""
Dashboard de KPIs - Aplicación Principal
"""
import streamlit as st
from config.settings import PAGE_CONFIG, COLUMNAS
from utils.data_processor import (
    cargar_y_limpiar_datos, 
    validar_columnas, 
    crear_columnas_agrupacion,
    aplicar_filtros
)
from components.sidebar import (
    mostrar_carga_archivo,
    mostrar_info_archivo,
    mostrar_promociones,
    mostrar_modulos,
    mostrar_filtros
)
from components.tab_kpis import mostrar_tab_kpis
from components.tab_promocion import mostrar_tab_promocion
from components.tab_modulo import mostrar_tab_modulo
from components.tab_datos import mostrar_tab_datos
from components.tab_agrupados import mostrar_tab_agrupados


# Configuración de la página
st.set_page_config(**PAGE_CONFIG)

# Título
st.title("📊 Dashboard de KPIs")

# Sidebar - Carga de archivo
uploaded_file = mostrar_carga_archivo()

if uploaded_file is not None:
    # Cargar y procesar datos
    df = cargar_y_limpiar_datos(uploaded_file)
    
    # Validar columnas
    es_valido, mensaje_error, tiene_modulo = validar_columnas(df)
    
    if not es_valido:
        st.error(mensaje_error)
        st.stop()
    
    # Crear columnas de agrupación
    df, columnas_agrupacion, columnas_excluir = crear_columnas_agrupacion(df, tiene_modulo)
    
    # Mostrar información en sidebar
    mostrar_info_archivo(uploaded_file, df)
    
    if tiene_modulo:
        st.sidebar.success("✅ Agrupando por Promoción y Módulo")
    else:
        st.sidebar.info("ℹ️ Agrupando solo por Promoción")
    
    # Mostrar promociones y módulos
    promociones = mostrar_promociones(df)
    modulos = mostrar_modulos(df) if tiene_modulo else None
    
    # Filtros
    filtro_promocion, filtro_modulo = mostrar_filtros(promociones, modulos, tiene_modulo)
    
    # Aplicar filtros
    df_filtrado = aplicar_filtros(df, filtro_promocion, filtro_modulo, tiene_modulo)
    
    # Crear tabs
    if tiene_modulo:
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📈 KPIs Principales", 
            "📊 Análisis por Promoción", 
            "📚 Análisis por Módulo",
            "📋 Datos", 
            "🔢 Datos Agrupados"
        ])
        
        with tab1:
            mostrar_tab_kpis(df_filtrado, tiene_modulo, columnas_excluir)
        
        with tab2:
            mostrar_tab_promocion(df_filtrado, columnas_excluir)
        
        with tab3:
            mostrar_tab_modulo(df_filtrado, columnas_excluir)
        
        with tab4:
            mostrar_tab_datos(df_filtrado)
        
        with tab5:
            mostrar_tab_agrupados(df_filtrado, tiene_modulo, columnas_excluir)
    else:
        tab1, tab2, tab4, tab5 = st.tabs([
            "📈 KPIs Principales", 
            "📊 Análisis por Promoción", 
            "📋 Datos", 
            "🔢 Datos Agrupados"
        ])
        
        with tab1:
            mostrar_tab_kpis(df_filtrado, tiene_modulo, columnas_excluir)
        
        with tab2:
            mostrar_tab_promocion(df_filtrado, columnas_excluir)
        
        with tab4:
            mostrar_tab_datos(df_filtrado)
        
        with tab5:
            mostrar_tab_agrupados(df_filtrado, tiene_modulo, columnas_excluir)

else:
    # Mensaje inicial
    st.info("👈 Por favor, sube un archivo Excel desde la barra lateral para comenzar")
    
    st.markdown("""
    ### 📝 Instrucciones:
    1. Sube tu archivo Excel usando el botón en la barra lateral
    2. El sistema automáticamente:
       - ✅ Eliminará las columnas "Submitted At" y "Token"
       - ✅ Usará la columna de promoción como índice
       - ✅ Agrupará por módulo (si existe)
       - ✅ **Calculará porcentajes DENTRO de cada promoción/módulo**
    3. Explora las diferentes pestañas para ver análisis y datos
    
    ### 🎯 Características:
    - ✅ Procesamiento automático de datos
    - ✅ Agrupación por Promoción y Módulo
    - ✅ KPIs calculados por grupo (Media y Mediana)
    - ✅ **Análisis de satisfacción en porcentajes POR PROMOCIÓN**
    - ✅ Gráficos interactivos
    - ✅ Filtrado dinámico
    - ✅ Descarga de resultados
    """)