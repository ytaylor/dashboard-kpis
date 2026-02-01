"""
Componentes del sidebar
"""
import streamlit as st
from config.settings import COLUMNAS


def mostrar_carga_archivo():
    """
    Muestra el componente de carga de archivo
    
    Returns:
        uploaded_file: Archivo subido o None
    """
    st.sidebar.header("Cargar datos")
    uploaded_file = st.sidebar.file_uploader("Sube tu archivo Excel", type=['xlsx', 'xls'])
    return uploaded_file


def mostrar_info_archivo(uploaded_file, df):
    """
    Muestra información básica del archivo cargado
    
    Args:
        uploaded_file: Archivo subido
        df: DataFrame cargado
    """
    st.sidebar.success(f"✅ Archivo cargado: {uploaded_file.name}")
    st.sidebar.info(f"Filas: {len(df)} | Columnas: {len(df.columns)}")


def mostrar_promociones(df):
    """
    Muestra las promociones encontradas en el sidebar
    
    Args:
        df: DataFrame con los datos
        
    Returns:
        list: Lista de promociones únicas
    """
    columna_promocion = COLUMNAS['promocion']
    promociones = df[columna_promocion].unique().tolist()
    
    st.sidebar.markdown("### 🎯 Promociones encontradas:")
    for promo in promociones:
        count = (df[columna_promocion] == promo).sum()
        st.sidebar.write(f"- {promo}: {count} registros")
    
    return promociones


def mostrar_modulos(df):
    """
    Muestra los módulos encontrados en el sidebar
    
    Args:
        df: DataFrame con los datos
        
    Returns:
        list: Lista de módulos únicos
    """
    columna_modulo = COLUMNAS['modulo']
    modulos = df[columna_modulo].unique().tolist()
    
    st.sidebar.markdown("### 📚 Módulos encontrados:")
    for modulo in modulos:
        count = (df[columna_modulo] == modulo).sum()
        st.sidebar.write(f"- {modulo}: {count} registros")
    
    return modulos


def mostrar_filtros(promociones, modulos=None, tiene_modulo=False):
    """
    Muestra los filtros de promoción y módulo
    
    Args:
        promociones: Lista de promociones disponibles
        modulos: Lista de módulos disponibles
        tiene_modulo: Si existe la columna de módulo
        
    Returns:
        tuple: (filtro_promocion, filtro_modulo)
    """
    st.sidebar.markdown("---")
    st.sidebar.header("Filtros")
    
    filtro_promocion = st.sidebar.multiselect(
        "Selecciona promoción(es)",
        options=promociones,
        default=promociones
    )
    
    filtro_modulo = None
    if tiene_modulo and modulos:
        filtro_modulo = st.sidebar.multiselect(
            "Selecciona módulo(s)",
            options=modulos,
            default=modulos
        )
    
    return filtro_promocion, filtro_modulo