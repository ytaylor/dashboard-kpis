"""
Tab de Análisis por Módulo
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


def mostrar_tab_modulo(df_filtrado, columnas_excluir):
    """
    Muestra el tab de análisis por módulo
    
    Args:
        df_filtrado: DataFrame filtrado
        columnas_excluir: Columnas a excluir del análisis
    """
    st.header("Análisis Detallado por Módulo")
    
    columna_modulo = COLUMNAS['modulo']
    
    # Verificar que existe la columna de módulo
    if columna_modulo not in df_filtrado.columns:
        st.warning("⚠️ No se encontró la columna de módulo en los datos")
        return
    
    # Análisis numérico
    numeric_columns = obtener_columnas_numericas(df_filtrado, columnas_excluir)
    
    if numeric_columns:
        col_analizar = st.selectbox("Selecciona columna numérica para analizar", numeric_columns, key='modulo_col')
        
        stats_por_modulo = calcular_estadisticas_por_grupo(df_filtrado, col_analizar, columna_modulo)
        stats_por_modulo.columns = ['Módulo', 'Media', 'Mediana', 'Máximo', 'Mínimo', 'Cantidad']
        
        st.subheader(f"📈 Estadísticas de '{col_analizar}' por Módulo")
        st.dataframe(stats_por_modulo, use_container_width=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig1 = px.bar(
                stats_por_modulo, 
                x='Módulo', 
                y='Media',
                title=f'Media de {col_analizar} por Módulo',
                color='Media',
                color_continuous_scale=COLOR_SCALES['modulo_media']
            )
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            fig2 = px.bar(
                stats_por_modulo, 
                x='Módulo', 
                y='Mediana',
                title=f'Mediana de {col_analizar} por Módulo',
                color='Mediana',
                color_continuous_scale=COLOR_SCALES['modulo_mediana']
            )
            st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("No hay columnas numéricas para analizar")
    
    # Análisis categórico
    st.subheader("📝 Análisis de Columnas Categóricas por Módulo")
    
    categorical_cols = obtener_columnas_categoricas(df_filtrado, columnas_excluir)
    
    if categorical_cols:
        col_categorica = st.selectbox("Selecciona columna categórica", categorical_cols, key='modulo_cat')
        
        # Verificar si es una columna de porcentaje
        columna_expectativas = COLUMNAS['expectativas']
        columna_recomendacion = COLUMNAS['recomendacion']
        es_columna_porcentaje = col_categorica in [columna_expectativas, columna_recomendacion]
        
        if es_columna_porcentaje:
            # Verificar si necesita filtro especial
            necesita_filtro, valor_modulo, descripcion = necesita_filtro_modulo(col_categorica)
            
            if necesita_filtro:
                st.info(f"ℹ️ {descripcion}")
                
                # Filtrar solo el módulo específico
                df_modulo_especifico = df_filtrado[df_filtrado[columna_modulo] == valor_modulo]
                
                if len(df_modulo_especifico) > 0:
                    st.caption(f"📊 Analizando {len(df_modulo_especifico)} registros del {valor_modulo}")
                    
                    # Calcular porcentajes dentro del módulo específico
                    porcentajes = calcular_porcentajes(df_modulo_especifico, col_categorica, columna_modulo, 'Módulo')
                    
                    if porcentajes is not None:
                        _mostrar_analisis_porcentajes(porcentajes, col_categorica, valor_modulo)
                    else:
                        st.warning(f"⚠️ No hay datos suficientes para analizar")
                else:
                    st.warning(f"⚠️ No hay datos disponibles para {valor_modulo}")
            else:
                # Calcular normalmente para todos los módulos
                porcentajes = calcular_porcentajes(df_filtrado, col_categorica, columna_modulo, 'Módulo')
                if porcentajes is not None:
                    _mostrar_analisis_porcentajes(porcentajes, col_categorica)
        else:
            # Mostrar en conteos normales
            _mostrar_analisis_conteos(df_filtrado, col_categorica, columna_modulo)
    
    # Análisis combinado: Promoción x Módulo
    st.markdown("---")
    st.subheader("🔀 Análisis Combinado: Promoción x Módulo")
    _mostrar_analisis_combinado(df_filtrado, columnas_excluir)


def _mostrar_analisis_porcentajes(porcentajes, col_categorica, modulo_filtrado=None):
    """Muestra análisis de porcentajes"""
    titulo_extra = f" - Solo {modulo_filtrado}" if modulo_filtrado else ""
    
    st.subheader(f"📊 Distribución de '{col_categorica}' (% dentro de cada módulo){titulo_extra}")
    
    tabla_pct = porcentajes.pivot(
        index='Módulo', 
        columns=col_categorica, 
        values='Porcentaje'
    ).fillna(0)
    tabla_pct['TOTAL'] = tabla_pct.sum(axis=1)
    
    st.dataframe(tabla_pct.style.format("{:.2f}%"), use_container_width=True)
    st.caption("💡 Cada fila debe sumar 100% (porcentaje dentro de cada módulo)")
    
    try:
        fig_cat = px.bar(
            porcentajes,
            x='Módulo',
            y='Porcentaje',
            color=col_categorica,
            title=f'Distribución de {col_categorica} por Módulo (%)' + titulo_extra,
            text='Porcentaje',
            barmode='stack'
        )
        fig_cat.update_traces(texttemplate='%{text:.1f}%', textposition='inside')
        fig_cat.update_layout(yaxis_title="Porcentaje (%)", yaxis_range=[0, 100])
        st.plotly_chart(fig_cat, use_container_width=True)
    except Exception as e:
        st.warning(f"⚠️ No se pudo generar el gráfico: {str(e)}")


def _mostrar_analisis_conteos(df_filtrado, col_categorica, columna_modulo):
    """Muestra análisis de conteos"""
    crosstab = pd.crosstab(df_filtrado[columna_modulo], df_filtrado[col_categorica])
    st.dataframe(crosstab, use_container_width=True)
    
    try:
        crosstab_reset = crosstab.reset_index()
        value_columns = crosstab.columns.tolist()
        
        if len(value_columns) > 0:
            fig_cat = px.bar(
                crosstab_reset, 
                x=columna_modulo,
                y=value_columns,
                title=f'Distribución de {col_categorica} por Módulo',
                barmode='stack'
            )
            st.plotly_chart(fig_cat, use_container_width=True)
        else:
            st.warning("⚠️ No hay suficientes datos para generar el gráfico")
    except Exception as e:
        st.warning(f"⚠️ No se pudo generar el gráfico: {str(e)}")
        st.info("La tabla de datos sigue siendo visible arriba.")


def _mostrar_analisis_combinado(df_filtrado, columnas_excluir):
    """Muestra análisis combinado de promoción x módulo"""
    from utils.calculations import calcular_estadisticas_combinado
    
    columna_promocion = COLUMNAS['promocion']
    columna_modulo = COLUMNAS['modulo']
    
    numeric_columns = obtener_columnas_numericas(df_filtrado, columnas_excluir)
    
    if numeric_columns:
        col_analizar_comb = st.selectbox(
            "Selecciona columna numérica para análisis combinado", 
            numeric_columns, 
            key='modulo_comb'
        )
        
        stats_combinado = calcular_estadisticas_combinado(
            df_filtrado, 
            col_analizar_comb, 
            [columna_promocion, columna_modulo]
        )
        stats_combinado.columns = ['Promoción', 'Módulo', 'Media', 'Mediana', 'Cantidad']
        
        st.subheader(f"📊 Estadísticas de '{col_analizar_comb}' por Promoción y Módulo")
        st.dataframe(stats_combinado, use_container_width=True)
        
        # Gráfico de barras agrupadas
        fig_comb = px.bar(
            stats_combinado,
            x='Promoción',
            y='Media',
            color='Módulo',
            title=f'Media de {col_analizar_comb} por Promoción y Módulo',
            barmode='group',
            text='Media'
        )
        fig_comb.update_traces(texttemplate='%{text:.2f}', textposition='outside')
        st.plotly_chart(fig_comb, use_container_width=True)
        
        # Heatmap de medias
        pivot_media = stats_combinado.pivot(
            index='Promoción',
            columns='Módulo',
            values='Media'
        )
        
        fig_heatmap = px.imshow(
            pivot_media,
            labels=dict(x="Módulo", y="Promoción", color="Media"),
            title=f"Mapa de Calor: Media de {col_analizar_comb}",
            color_continuous_scale=COLOR_SCALES['heatmap'],
            text_auto='.2f'
        )
        st.plotly_chart(fig_heatmap, use_container_width=True)
    else:
        st.info("No hay columnas numéricas para análisis combinado")