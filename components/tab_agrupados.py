"""
Tab de Datos Agrupados
"""
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from config.settings import COLUMNAS, AGREGACIONES, COLOR_SCALES
from utils.data_processor import obtener_columnas_numericas


def mostrar_tab_agrupados(df_filtrado, tiene_modulo, columnas_excluir):
    """
    Muestra el tab de datos agrupados con opciones de agregación
    
    Args:
        df_filtrado: DataFrame filtrado
        tiene_modulo: Si existe la columna de módulo
        columnas_excluir: Columnas a excluir del análisis
    """
    st.header("Datos Agrupados")
    
    columna_promocion = COLUMNAS['promocion']
    columna_modulo = COLUMNAS['modulo']
    
    # Opciones de agrupación
    st.subheader("⚙️ Configuración de Agrupación")
    
    col_config1, col_config2 = st.columns(2)
    
    with col_config1:
        # Seleccionar por qué agrupar
        opciones_agrupacion = ['Promoción']
        if tiene_modulo:
            opciones_agrupacion.append('Módulo')
            opciones_agrupacion.append('Promoción + Módulo')
        
        tipo_agrupacion = st.selectbox(
            "Agrupar por",
            opciones_agrupacion,
            help="Selecciona cómo quieres agrupar los datos"
        )
    
    with col_config2:
        # Seleccionar tipo de agregación
        tipo_agregacion = st.selectbox(
            "Tipo de agregación",
            list(AGREGACIONES.keys()),
            help="Selecciona qué operación aplicar a los datos numéricos"
        )
    
    # Determinar columnas de agrupación
    if tipo_agrupacion == 'Promoción':
        columnas_grupo = [columna_promocion]
        nombre_grupo = 'Promoción'
    elif tipo_agrupacion == 'Módulo':
        columnas_grupo = [columna_modulo]
        nombre_grupo = 'Módulo'
    else:  # Promoción + Módulo
        columnas_grupo = [columna_promocion, columna_modulo]
        nombre_grupo = 'Promoción + Módulo'
    
    # Obtener columnas numéricas
    numeric_cols = obtener_columnas_numericas(df_filtrado, columnas_excluir)
    
    if not numeric_cols:
        st.warning("⚠️ No hay columnas numéricas para agrupar")
        return
    
    # Seleccionar columnas a agregar
    st.markdown("---")
    st.subheader("📊 Selección de Columnas")
    
    columnas_seleccionadas = st.multiselect(
        "Selecciona las columnas numéricas a agregar",
        numeric_cols,
        default=numeric_cols[:3] if len(numeric_cols) >= 3 else numeric_cols,
        help="Puedes seleccionar múltiples columnas"
    )
    
    if not columnas_seleccionadas:
        st.info("👆 Selecciona al menos una columna para continuar")
        return
    
    # Realizar agrupación
    st.markdown("---")
    st.subheader(f"📈 Resultados Agrupados por {nombre_grupo}")
    
    try:
        # Aplicar agregación
        funcion_agregacion = AGREGACIONES[tipo_agregacion]
        
        df_agrupado = df_filtrado.groupby(columnas_grupo)[columnas_seleccionadas].agg(
            funcion_agregacion
        ).reset_index()
        
        # Renombrar columnas para claridad
        nuevos_nombres = {}
        for col in columnas_seleccionadas:
            nuevos_nombres[col] = f"{col} ({tipo_agregacion})"
        df_agrupado = df_agrupado.rename(columns=nuevos_nombres)
        
        # Mostrar tabla
        st.dataframe(df_agrupado, use_container_width=True, height=400)
        
        # Estadísticas de la agrupación
        col_stat1, col_stat2, col_stat3 = st.columns(3)
        
        with col_stat1:
            st.metric("Grupos Totales", len(df_agrupado))
        
        with col_stat2:
            st.metric("Columnas Agregadas", len(columnas_seleccionadas))
        
        with col_stat3:
            st.metric("Tipo de Agregación", tipo_agregacion)
        
        # Descargar datos agrupados
        st.markdown("---")
        st.subheader("💾 Descargar Datos Agrupados")
        
        col_desc1, col_desc2 = st.columns(2)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre_base = f"datos_agrupados_{tipo_agrupacion.replace(' + ', '_')}_{tipo_agregacion}_{timestamp}"
        
        with col_desc1:
            # Descargar como CSV
            csv = df_agrupado.to_csv(index=False).encode('utf-8')
            
            st.download_button(
                label="📥 Descargar como CSV",
                data=csv,
                file_name=f"{nombre_base}.csv",
                mime="text/csv",
                help="Descarga los datos agrupados en formato CSV"
            )
        
        with col_desc2:
            # Descargar como Excel
            from io import BytesIO
            
            buffer = BytesIO()
            with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                df_agrupado.to_excel(writer, index=False, sheet_name='Datos Agrupados')
            
            st.download_button(
                label="📥 Descargar como Excel",
                data=buffer.getvalue(),
                file_name=f"{nombre_base}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                help="Descarga los datos agrupados en formato Excel"
            )
        
        # Resumen de la descarga
        st.caption(f"📊 Archivo incluye {len(df_agrupado)} grupos y {len(df_agrupado.columns)} columnas")
        
    except Exception as e:
        st.error(f"❌ Error al agrupar datos: {str(e)}")
        st.info("Verifica que las columnas seleccionadas sean compatibles con la agregación elegida")