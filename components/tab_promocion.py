"""
Tab de Análisis por Promoción
"""
import streamlit as st
import pandas as pd
import plotly.express as px
from config.settings import COLUMNAS, COLOR_SCALES
from utils.calculations import (
    calcular_porcentajes, 
    calcular_porcentajes_con_filtro,
    calcular_estadisticas_por_grupo,
    necesita_filtro_modulo
)
from utils.data_processor import obtener_columnas_numericas, obtener_columnas_categoricas


def mostrar_tab_promocion(df_filtrado, columnas_excluir):
    """
    Muestra el tab de análisis por promoción
    
    Args:
        df_filtrado: DataFrame filtrado
        columnas_excluir: Columnas a excluir del análisis
    """
    st.header("Análisis Detallado por Promoción")
    
    columna_promocion = COLUMNAS['promocion']
    
    # Análisis numérico
    numeric_columns = obtener_columnas_numericas(df_filtrado, columnas_excluir)
    
    if numeric_columns:
        col_analizar = st.selectbox("Selecciona columna numérica para analizar", numeric_columns, key='promo_col')
        
        stats_por_promocion = calcular_estadisticas_por_grupo(df_filtrado, col_analizar, columna_promocion)
        stats_por_promocion.columns = ['Promoción', 'Media', 'Mediana', 'Máximo', 'Mínimo', 'Cantidad']
        
        st.subheader(f"📈 Estadísticas de '{col_analizar}' por Promoción")
        st.dataframe(stats_por_promocion, use_container_width=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig1 = px.bar(
                stats_por_promocion, 
                x='Promoción', 
                y='Media',
                title=f'Media de {col_analizar} por Promoción',
                color='Media',
                color_continuous_scale=COLOR_SCALES['media']
            )
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            fig2 = px.bar(
                stats_por_promocion, 
                x='Promoción', 
                y='Mediana',
                title=f'Mediana de {col_analizar} por Promoción',
                color='Mediana',
                color_continuous_scale=COLOR_SCALES['mediana']
            )
            st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("No hay columnas numéricas para analizar")
    
    # Análisis categórico
    st.subheader("📝 Análisis de Columnas Categóricas por Promoción")
    
    categorical_cols = obtener_columnas_categoricas(df_filtrado, columnas_excluir)
    
    if categorical_cols:
        col_categorica = st.selectbox("Selecciona columna categórica", categorical_cols, key='promo_cat')
        
        # Verificar si es una columna de porcentaje
        columna_expectativas = COLUMNAS['expectativas']
        columna_recomendacion = COLUMNAS['recomendacion']
        es_columna_porcentaje = col_categorica in [columna_expectativas, columna_recomendacion]
        
        if es_columna_porcentaje:
            # Verificar si necesita filtro especial
            necesita_filtro, valor_modulo, descripcion = necesita_filtro_modulo(col_categorica)
            
            if necesita_filtro and COLUMNAS['modulo'] in df_filtrado.columns:
                st.info(f"ℹ️ {descripcion}")
                
                porcentajes, df_usado = calcular_porcentajes_con_filtro(
                    df_filtrado, 
                    col_categorica, 
                    columna_promocion, 
                    'Promoción',
                    filtro_modulo=valor_modulo
                )
                
                if porcentajes is not None:
                    st.caption(f"📊 Analizando {len(df_usado)} registros del {valor_modulo}")
                    _mostrar_analisis_porcentajes(porcentajes, col_categorica, valor_modulo)
                else:
                    st.warning(f"⚠️ No hay datos disponibles para {valor_modulo}")
            else:
                porcentajes = calcular_porcentajes(df_filtrado, col_categorica, columna_promocion, 'Promoción')
                if porcentajes is not None:
                    _mostrar_analisis_porcentajes(porcentajes, col_categorica)
        else:
            # Mostrar en conteos normales
            _mostrar_analisis_conteos(df_filtrado, col_categorica, columna_promocion)


def _mostrar_analisis_porcentajes(porcentajes, col_categorica, modulo_filtrado=None):
    """Muestra análisis de porcentajes"""
    titulo_extra = f" - {modulo_filtrado}" if modulo_filtrado else ""
    
    st.subheader(f"📊 Distribución de '{col_categorica}' (% dentro de cada promoción){titulo_extra}")
    
    tabla_pct = porcentajes.pivot(
        index='Promoción', 
        columns=col_categorica, 
        values='Porcentaje'
    ).fillna(0)
    tabla_pct['TOTAL'] = tabla_pct.sum(axis=1)
    
    st.dataframe(tabla_pct.style.format("{:.2f}%"), use_container_width=True)
    st.caption("💡 Cada fila debe sumar 100% (porcentaje dentro de cada promoción)")
    
    try:
        fig_cat = px.bar(
            porcentajes,
            x='Promoción',
            y='Porcentaje',
            color=col_categorica,
            title=f'Distribución de {col_categorica} por Promoción (%)' + titulo_extra,
            text='Porcentaje',
            barmode='stack'
        )
        fig_cat.update_traces(texttemplate='%{text:.1f}%', textposition='inside')
        fig_cat.update_layout(yaxis_title="Porcentaje (%)", yaxis_range=[0, 100])
        st.plotly_chart(fig_cat, use_container_width=True)
    except Exception as e:
        st.warning(f"⚠️ No se pudo generar el gráfico: {str(e)}")


def _mostrar_analisis_conteos(df_filtrado, col_categorica, columna_promocion):
    """Muestra análisis de conteos"""
    crosstab = pd.crosstab(df_filtrado[columna_promocion], df_filtrado[col_categorica])
    st.dataframe(crosstab, use_container_width=True)
    
    try:
        crosstab_reset = crosstab.reset_index()
        value_columns = crosstab.columns.tolist()
        
        if len(value_columns) > 0:
            fig_cat = px.bar(
                crosstab_reset, 
                x=columna_promocion,
                y=value_columns,
                title=f'Distribución de {col_categorica} por Promoción',
                barmode='stack'
            )
            st.plotly_chart(fig_cat, use_container_width=True)
        else:
            st.warning("⚠️ No hay suficientes datos para generar el gráfico")
    except Exception as e:
        st.warning(f"⚠️ No se pudo generar el gráfico: {str(e)}")
        st.info("La tabla de datos sigue siendo visible arriba.")