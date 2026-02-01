# procesamiento de datos y limpieza
"""
Funciones para procesamiento de datos
"""
import pandas as pd
from config.settings import COLUMNAS, COLUMNAS_ELIMINAR


def cargar_y_limpiar_datos(uploaded_file):
    """
    Carga el archivo Excel y elimina columnas no deseadas
    
    Args:
        uploaded_file: Archivo subido por el usuario
        
    Returns:
        pd.DataFrame: DataFrame limpio
    """
    df = pd.read_excel(uploaded_file)
    df = df.drop(columns=[col for col in COLUMNAS_ELIMINAR if col in df.columns], errors='ignore')
    return df


def validar_columnas(df):
    """
    Valida que existan las columnas necesarias
    
    Args:
        df: DataFrame a validar
        
    Returns:
        tuple: (es_valido, mensaje_error, tiene_modulo)
    """
    columna_promocion = COLUMNAS['promocion']
    
    if columna_promocion not in df.columns:
        return False, f"❌ No se encontró la columna '{columna_promocion}' en el Excel", False
    
    tiene_modulo = COLUMNAS['modulo'] in df.columns
    
    return True, None, tiene_modulo


def crear_columnas_agrupacion(df, tiene_modulo):
    """
    Crea columnas auxiliares para agrupación
    
    Args:
        df: DataFrame original
        tiene_modulo: Si existe la columna de módulo
        
    Returns:
        tuple: (df_modificado, columnas_agrupacion, columnas_excluir)
    """
    columna_promocion = COLUMNAS['promocion']
    columna_modulo = COLUMNAS['modulo']
    
    if tiene_modulo:
        df['_Agrupacion'] = df[columna_promocion].astype(str) + ' - ' + df[columna_modulo].astype(str)
        columnas_agrupacion = [columna_promocion, columna_modulo]
        columnas_excluir = [columna_promocion, columna_modulo, '_Agrupacion']
    else:
        df['_Agrupacion'] = df[columna_promocion].astype(str)
        columnas_agrupacion = [columna_promocion]
        columnas_excluir = [columna_promocion, '_Agrupacion']
    
    return df, columnas_agrupacion, columnas_excluir


def aplicar_filtros(df, filtro_promocion, filtro_modulo=None, tiene_modulo=False):
    """
    Aplica filtros de promoción y módulo al DataFrame
    
    Args:
        df: DataFrame original
        filtro_promocion: Lista de promociones seleccionadas
        filtro_modulo: Lista de módulos seleccionados
        tiene_modulo: Si existe la columna de módulo
        
    Returns:
        pd.DataFrame: DataFrame filtrado
    """
    df_filtrado = df.copy()
    
    columna_promocion = COLUMNAS['promocion']
    columna_modulo = COLUMNAS['modulo']
    
    if filtro_promocion:
        df_filtrado = df_filtrado[df_filtrado[columna_promocion].isin(filtro_promocion)]
    
    if tiene_modulo and filtro_modulo:
        df_filtrado = df_filtrado[df_filtrado[columna_modulo].isin(filtro_modulo)]
    
    return df_filtrado


def obtener_columnas_numericas(df, columnas_excluir):
    """
    Obtiene las columnas numéricas excluyendo las de agrupación
    
    Args:
        df: DataFrame
        columnas_excluir: Lista de columnas a excluir
        
    Returns:
        list: Lista de nombres de columnas numéricas
    """
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    return [col for col in numeric_cols if col not in columnas_excluir]


def obtener_columnas_categoricas(df, columnas_excluir):
    """
    Obtiene las columnas categóricas excluyendo las de agrupación
    
    Args:
        df: DataFrame
        columnas_excluir: Lista de columnas a excluir
        
    Returns:
        list: Lista de nombres de columnas categóricas
    """
    categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
    return [col for col in categorical_cols if col not in columnas_excluir]