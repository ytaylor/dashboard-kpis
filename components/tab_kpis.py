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
   # _mostrar_resumen_promocion(df_filtrado)
    
    # Resumen por módulo (si existe)
    # if tiene_modulo:
    #     _mostrar_resumen_modulo(df_filtrado)
    #     _mostrar_matriz_promocion_modulo(df_filtrado)
    
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
            # buscar la columna con este valor: Valora de forma global el equipo docente 
            index_columna = df_filtrado.columns .get_loc('Valora de forma global el equipo docente') if 'Valora de forma global el equipo docente' in df_filtrado.columns else 89
            primera_col_numerica = numeric_cols[index_columna]
            media = df_filtrado[primera_col_numerica].mean()
            st.metric(f"Media {primera_col_numerica}", f"{media:,.2f}")
        else:
            st.metric("Columnas Numéricas", len(numeric_cols))

def _mostrar_analisis_satisfaccion(df_filtrado, tiene_modulo):
    """Muestra el análisis de satisfacción (expectativas y recomendación)"""
    columna_promocion = COLUMNAS['promocion']
    columna_modulo = COLUMNAS['modulo']
    columna_expectativas = COLUMNAS['expectativas']
    columna_recomendacion = COLUMNAS['recomendacion']
    
    # ========== EXPECTATIVAS (SOLO MÓDULO 4) ==========
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
            
            if porcentajes is not None and len(df_usado) > 0:
                # Mostrar cuántos registros se están usando
                st.caption(f"📊 Analizando {len(df_usado)} registros del {valor_modulo}")
                
                # Por Promoción
                st.markdown("**Por Promoción:**")
                _mostrar_grafico_porcentajes(
                    porcentajes, 
                    columna_expectativas,
                    f'Cumplimiento de Expectativas por Promoción - {valor_modulo} (%)'
                )
                
                # Por Módulo (dentro del Módulo 4)
                if tiene_modulo and columna_modulo in df_usado.columns:
                    st.markdown("---")
                    st.markdown("**Por Módulo:**")
                    
                    porcentajes_modulo, _ = calcular_porcentajes_con_filtro(
                        df_filtrado,
                        columna_expectativas,
                        columna_modulo,
                        'Módulo',
                        filtro_modulo=valor_modulo
                    )
                    
                    if porcentajes_modulo is not None:
                        _mostrar_grafico_porcentajes(
                            porcentajes_modulo,
                            columna_expectativas,
                            f'Cumplimiento de Expectativas por Módulo - {valor_modulo} (%)'
                        )
            else:
                st.warning(f"⚠️ No hay datos disponibles para {valor_modulo}")
        else:
            # Si no tiene módulo, calcular normalmente
            _mostrar_grafico_porcentajes_simple(
                df_filtrado, 
                columna_expectativas, 
                columna_promocion, 
                'Cumplimiento de Expectativas por Promoción (%)'
            )
    
    # ========== RECOMENDACIÓN (SOLO MÓDULO 4 - IGUAL QUE EXPECTATIVAS) ==========
    if columna_recomendacion in df_filtrado.columns:
        st.subheader("💚 Recomendación de Adalab")
        
        # Verificar si necesita filtro especial
        necesita_filtro, valor_modulo, descripcion = necesita_filtro_modulo(columna_recomendacion)
        
        if necesita_filtro and tiene_modulo:
            # Mostrar advertencia
            st.info(f"ℹ️ {descripcion}")
            
            # Calcular con filtro de módulo
            porcentajes, df_usado = calcular_porcentajes_con_filtro(
                df_filtrado, 
                columna_recomendacion, 
                columna_promocion, 
                'Promoción',
                filtro_modulo=valor_modulo
            )
            
            if porcentajes is not None and len(df_usado) > 0:
                # Mostrar cuántos registros se están usando
                st.caption(f"📊 Analizando {len(df_usado)} registros del {valor_modulo}")
                
                # Por Promoción
                st.markdown("**Por Promoción:**")
                _mostrar_grafico_porcentajes(
                    porcentajes, 
                    columna_recomendacion,
                    f'Recomendación de Adalab por Promoción - {valor_modulo} (%)'
                )
                
                # Por Módulo (dentro del Módulo 4)
                if tiene_modulo and columna_modulo in df_usado.columns:
                    st.markdown("---")
                    st.markdown("**Por Módulo:**")
                    
                    porcentajes_modulo, _ = calcular_porcentajes_con_filtro(
                        df_filtrado,
                        columna_recomendacion,
                        columna_modulo,
                        'Módulo',
                        filtro_modulo=valor_modulo
                    )
                    
                    if porcentajes_modulo is not None:
                        _mostrar_grafico_porcentajes(
                            porcentajes_modulo,
                            columna_recomendacion,
                            f'Recomendación de Adalab por Módulo - {valor_modulo} (%)'
                        )
            else:
                st.warning(f"⚠️ No hay datos disponibles para {valor_modulo}")
        else:
            # Si no tiene módulo, calcular normalmente
            _mostrar_grafico_porcentajes_simple(
                df_filtrado, 
                columna_recomendacion, 
                columna_promocion,
                'Recomendación de Adalab por Promoción (%)'
            )

def _mostrar_grafico_porcentajes_simple(df_filtrado, columna, grupo_col, titulo):
    """Muestra gráfico y tabla de porcentajes (sin filtro especial)"""
    porcentajes = calcular_porcentajes(df_filtrado, columna, grupo_col, 'Promoción')
    
    if porcentajes is not None:
        _mostrar_grafico_porcentajes(porcentajes, columna, titulo)

def _mostrar_grafico_porcentajes(porcentajes_df, columna_analizada, titulo):
    """
    Muestra gráfico de barras con porcentajes
    
    Args:
        porcentajes_df: DataFrame con columnas [Grupo, Respuesta, Porcentaje]
        columna_analizada: Nombre de la columna analizada
        titulo: Título del gráfico
    """
    if porcentajes_df is None or len(porcentajes_df) == 0:
        st.warning("⚠️ No hay datos suficientes para mostrar el gráfico")
        return
    
    try:
        # Identificar la columna de grupo (primera columna que no sea la analizada ni métricas)
        columnas_posibles = [col for col in porcentajes_df.columns 
                            if col not in [columna_analizada, 'Cantidad', 'Total', 'Porcentaje']]
        
        if not columnas_posibles:
            st.error("❌ No se pudo identificar la columna de agrupación")
            st.dataframe(porcentajes_df)
            return
        
        columna_grupo = columnas_posibles[0]
        
        # Verificar que las columnas necesarias existen
        if columna_grupo not in porcentajes_df.columns:
            st.error(f"❌ La columna '{columna_grupo}' no existe en los datos")
            st.dataframe(porcentajes_df)
            return
        
        if columna_analizada not in porcentajes_df.columns:
            st.error(f"❌ La columna '{columna_analizada}' no existe en los datos")
            st.dataframe(porcentajes_df)
            return
        
        # Crear gráfico de barras agrupadas
        fig = px.bar(
            porcentajes_df,
            x=columna_grupo,
            y='Porcentaje',
            color=columna_analizada,
            title=titulo,
            text='Porcentaje',
            barmode='group',
            color_discrete_sequence=px.colors.sequential.Blues
        )
        
        # Formato del texto en las barras
        fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        
        # Ajustar layout
        fig.update_layout(
            xaxis_title=columna_grupo,
            yaxis_title='Porcentaje (%)',
            yaxis_range=[0, max(porcentajes_df['Porcentaje'].max() * 1.1, 100)],
            showlegend=True,
            legend_title=columna_analizada,
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)
        # Mostrar tabla de datos
        with st.expander("📊 Ver datos detallados"):
        # Identificar columna de grupo y columna de respuesta
            columnas_posibles = [col for col in porcentajes_df.columns 
                                if col not in ['Cantidad', 'Total', 'Porcentaje']]
            
            if len(columnas_posibles) >= 2:
                columna_grupo = columnas_posibles[0]  # Ej: 'Promoción' o 'Módulo'
                columna_respuesta = columnas_posibles[1]  # Ej: '¿Recomendarías Adalab?'
                
                # PIVOT: Convertir respuestas en columnas
                df_pivot = porcentajes_df.pivot(
                    index=columna_grupo,
                    columns=columna_respuesta,
                    values='Porcentaje'
                ).reset_index()
                
                # Renombrar columnas para agregar " (%)"
                nuevos_nombres = {col: f"{col} (%)" for col in df_pivot.columns if col != columna_grupo}
                df_pivot = df_pivot.rename(columns=nuevos_nombres)
                
                # Formatear porcentajes
                for col in df_pivot.columns:
                    if '(%)' in col:
                        df_pivot[col] = df_pivot[col].apply(lambda x: f"{x:.2f}%" if pd.notna(x) else "-")
                
                st.dataframe(df_pivot, use_container_width=True)
            else:
                # Fallback: mostrar tabla original si no se puede pivotar
                df_mostrar = porcentajes_df.copy()
                df_mostrar['Porcentaje'] = df_mostrar['Porcentaje'].apply(lambda x: f"{x:.2f}%")
                st.dataframe(df_mostrar, use_container_width=True)
            
    except Exception as e:
        st.error(f"❌ Error al crear el gráfico: {str(e)}")
        st.info("Mostrando solo la tabla de datos:")
        st.dataframe(porcentajes_df, use_container_width=True)