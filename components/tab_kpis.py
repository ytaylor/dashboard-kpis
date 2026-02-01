"""
Tab de KPIs Principales
"""
import streamlit as st
import pandas as pd
import plotly.express as px
from config.settings import COLUMNAS, COLOR_SCALES, FILTROS_ESPECIALES
from utils.calculations import calcular_porcentajes, calcular_porcentajes_con_filtro, necesita_filtro_modulo


def mostrar_tab_kpis(df_filtrado, tiene_modulo, columnas_excluir):
    """
    Muestra el tab de KPIs principales
    
    Args:
        df_filtrado: DataFrame filtrado
        tiene_modulo: Si existe la columna de módulo
        columnas_excluir: Columnas a excluir del análisis
    """
    st.header("KPIs Principales")
    
    # Métricas principales
    _mostrar_metricas_principales(df_filtrado, tiene_modulo, columnas_excluir)
    
    # Resumen por promoción
    _mostrar_resumen_promocion(df_filtrado)
    
    # Resumen por módulo (si existe)
    if tiene_modulo:
        _mostrar_resumen_modulo(df_filtrado)
        _mostrar_matriz_promocion_modulo(df_filtrado)
    
    # Análisis de satisfacción
    st.markdown("---")
    st.header("📊 Análisis de Satisfacción por Promoción")
    _mostrar_analisis_satisfaccion(df_filtrado, tiene_modulo)


def _mostrar_metricas_principales(df_filtrado, tiene_modulo, columnas_excluir):
    """Muestra las métricas principales en columnas"""
    columna_promocion = COLUMNAS['promocion']
    columna_modulo = COLUMNAS['modulo']
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Registros", len(df_filtrado))
    
    with col2:
        st.metric("Promociones", df_filtrado[columna_promocion].nunique())
    
    with col3:
        if tiene_modulo:
            st.metric("Módulos", df_filtrado[columna_modulo].nunique())
        else:
            st.metric("Columnas Analizadas", len(df_filtrado.columns))
    
    numeric_cols = df_filtrado.select_dtypes(include=['number']).columns
    numeric_cols = [col for col in numeric_cols if col not in columnas_excluir]
    
    with col4:
        if len(numeric_cols) > 0:
            primera_col_numerica = numeric_cols[0]
            media = df_filtrado[primera_col_numerica].mean()
            st.metric(f"Media {primera_col_numerica}", f"{media:,.2f}")
        else:
            st.metric("Columnas Numéricas", len(numeric_cols))


def _mostrar_resumen_promocion(df_filtrado):
    """Muestra el resumen por promoción"""
    columna_promocion = COLUMNAS['promocion']
    
    st.subheader("📊 Resumen por Promoción")
    
    resumen_promocion = df_filtrado.groupby(columna_promocion).size().reset_index(name='Cantidad')
    resumen_promocion.columns = ['Promoción', 'Cantidad de Registros']
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_promo = px.bar(
            resumen_promocion, 
            x='Promoción', 
            y='Cantidad de Registros',
            title='Registros por Promoción',
            color='Cantidad de Registros',
            color_continuous_scale=COLOR_SCALES['promocion']
        )
        st.plotly_chart(fig_promo, use_container_width=True)
    
    with col2:
        st.dataframe(resumen_promocion, use_container_width=True, height=300)


def _mostrar_resumen_modulo(df_filtrado):
    """Muestra el resumen por módulo"""
    columna_modulo = COLUMNAS['modulo']
    
    st.subheader("📚 Resumen por Módulo")
    
    resumen_modulo = df_filtrado.groupby(columna_modulo).size().reset_index(name='Cantidad')
    resumen_modulo.columns = ['Módulo', 'Cantidad de Registros']
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_modulo = px.bar(
            resumen_modulo, 
            x='Módulo', 
            y='Cantidad de Registros',
            title='Registros por Módulo',
            color='Cantidad de Registros',
            color_continuous_scale=COLOR_SCALES['modulo']
        )
        st.plotly_chart(fig_modulo, use_container_width=True)
    
    with col2:
        st.dataframe(resumen_modulo, use_container_width=True, height=300)


def _mostrar_matriz_promocion_modulo(df_filtrado):
    """Muestra la matriz de promoción x módulo"""
    columna_promocion = COLUMNAS['promocion']
    columna_modulo = COLUMNAS['modulo']
    
    st.subheader("🔀 Matriz: Promoción x Módulo")
    
    matriz = pd.crosstab(df_filtrado[columna_promocion], df_filtrado[columna_modulo])
    st.dataframe(matriz, use_container_width=True)
    
    # Heatmap
    fig_heatmap = px.imshow(
        matriz,
        labels=dict(x="Módulo", y="Promoción", color="Cantidad"),
        title="Mapa de Calor: Promoción x Módulo",
        color_continuous_scale=COLOR_SCALES['heatmap'],
        text_auto=True
    )
    st.plotly_chart(fig_heatmap, use_container_width=True)


def _mostrar_analisis_satisfaccion(df_filtrado, tiene_modulo):
    """Muestra el análisis de satisfacción (expectativas y recomendación)"""
    columna_promocion = COLUMNAS['promocion']
    columna_expectativas = COLUMNAS['expectativas']
    columna_recomendacion = COLUMNAS['recomendacion']
    
    # Expectativas (SOLO MÓDULO 4)
    if columna_expectativas in df_filtrado.columns:
        st.subheader("✨ Cumplimiento de Expectativas")
        
        # Verificar si necesita filtro especial
        necesita_filtro, valor_modulo, descripcion = necesita_filtro_modulo(columna_expectativas)
        
        if necesita_filtro and tiene_modulo:
            # Mostrar advertencia
            st.info(f"ℹ️ {descripcion}")
            
            # Calcular con filtro de módulo
            porcentajes, df_usado = calcular_porcentajes_con_filtro(
                df_filtrado, 
                columna_expectativas, 
                columna_promocion, 
                'Promoción',
                filtro_modulo=valor_modulo
            )
            
            if porcentajes is not None:
                # Mostrar cuántos registros se están usando
                st.caption(f"📊 Analizando {len(df_usado)} registros del {valor_modulo}")
                
                _mostrar_grafico_porcentajes(
                    porcentajes, 
                    columna_expectativas,
                    f'Cumplimiento de Expectativas por Promoción - {valor_modulo} (%)'
                )
            else:
                st.warning(f"⚠️ No hay datos disponibles para {valor_modulo}")
        else:
            # Calcular normalmente (sin filtro)
            _mostrar_grafico_porcentajes_simple(df_filtrado, columna_expectativas, columna_promocion, 
                                         'Cumplimiento de Expectativas por Promoción (%)')
    
    # Recomendación (TODOS LOS MÓDULOS)
    if columna_recomendacion in df_filtrado.columns:
        st.subheader("💚 Recomendación de Adalab")
        _mostrar_grafico_porcentajes_simple(df_filtrado, columna_recomendacion, columna_promocion,
                                     'Recomendación de Adalab por Promoción (%)')


def _mostrar_grafico_porcentajes_simple(df_filtrado, columna, grupo_col, titulo):
    """Muestra gráfico y tabla de porcentajes (sin filtro especial)"""
    porcentajes = calcular_porcentajes(df_filtrado, columna, grupo_col, 'Promoción')
    
    if porcentajes is not None:
        _mostrar_grafico_porcentajes(porcentajes, columna, titulo)


def _mostrar_grafico_porcentajes(porcentajes, columna, titulo):
    """Muestra el gráfico y tabla de porcentajes"""
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.bar(
            porcentajes,
            x='Promoción',
            y='Porcentaje',
            color=columna,
            title=titulo,
            text='Porcentaje',
            barmode='stack'
        )
        fig.update_traces(texttemplate='%{text:.1f}%', textposition='inside')
        fig.update_layout(yaxis_title="Porcentaje (%)", yaxis_range=[0, 100])
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        tabla = porcentajes.pivot(
            index='Promoción', 
            columns=columna, 
            values='Porcentaje'
        ).fillna(0)
        tabla['TOTAL'] = tabla.sum(axis=1)
        st.dataframe(tabla.style.format("{:.2f}%"), use_container_width=True)
        st.caption("💡 Cada fila debe sumar 100% (porcentaje dentro de cada promoción)")