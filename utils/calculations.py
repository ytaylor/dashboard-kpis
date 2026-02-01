"""
Funciones para cálculos y estadísticas
"""
import pandas as pd
from config.settings import COLUMNAS, FILTROS_ESPECIALES


def calcular_porcentajes(df_data, columna, grupo_col, nombre_grupo='Grupo'):
    """
    Calcula porcentajes de respuestas DENTRO de cada grupo
    
    Args:
        df_data: DataFrame con los datos
        columna: Columna a analizar
        grupo_col: Columna por la que agrupar
        nombre_grupo: Nombre para la columna de grupo en el resultado
        
    Returns:
        pd.DataFrame: DataFrame con porcentajes por grupo
    """
    if columna not in df_data.columns:
        return None
    
    # Contar respuestas por grupo
    conteo = df_data.groupby([grupo_col, columna]).size().reset_index(name='Cantidad')
    
    # Calcular total por grupo
    total_por_grupo = df_data.groupby(grupo_col).size().reset_index(name='Total')
    
    # Merge y calcular porcentaje DENTRO de cada grupo
    resultado = conteo.merge(total_por_grupo, on=grupo_col)
    resultado['Porcentaje'] = (resultado['Cantidad'] / resultado['Total'] * 100).round(2)
    
    # Renombrar la columna de grupo DESPUÉS de todos los cálculos
    resultado = resultado.rename(columns={grupo_col: nombre_grupo})
    
    return resultado


def calcular_porcentajes_con_filtro(df_data, columna, grupo_col, nombre_grupo='Grupo', filtro_modulo=None):
    """
    Calcula porcentajes de respuestas DENTRO de cada grupo, 
    aplicando un filtro de módulo si es necesario
    
    Args:
        df_data: DataFrame con los datos
        columna: Columna a analizar
        grupo_col: Columna por la que agrupar
        nombre_grupo: Nombre para la columna de grupo en el resultado
        filtro_modulo: Valor del módulo para filtrar (ej: 'Módulo 4')
        
    Returns:
        tuple: (DataFrame con porcentajes, DataFrame filtrado usado)
    """
    if columna not in df_data.columns:
        return None, None
    
    # Aplicar filtro de módulo si existe
    df_filtrado = df_data.copy()
    if filtro_modulo and COLUMNAS['modulo'] in df_data.columns:
        df_filtrado = df_filtrado[df_filtrado[COLUMNAS['modulo']] == filtro_modulo]
    
    # Si no hay datos después del filtro, retornar None
    if len(df_filtrado) == 0:
        return None, None
    
    # Contar respuestas por grupo
    conteo = df_filtrado.groupby([grupo_col, columna]).size().reset_index(name='Cantidad')
    
    # Calcular total por grupo
    total_por_grupo = df_filtrado.groupby(grupo_col).size().reset_index(name='Total')
    
    # Merge y calcular porcentaje DENTRO de cada grupo
    resultado = conteo.merge(total_por_grupo, on=grupo_col)
    resultado['Porcentaje'] = (resultado['Cantidad'] / resultado['Total'] * 100).round(2)
    
    # Renombrar la columna de grupo DESPUÉS de todos los cálculos
    resultado = resultado.rename(columns={grupo_col: nombre_grupo})
    
    return resultado, df_filtrado


def calcular_porcentajes_combinado(df_data, columna, grupo_cols, nombres_grupos=['Grupo1', 'Grupo2']):
    """
    Calcula porcentajes de respuestas DENTRO de cada combinación de grupos
    
    Args:
        df_data: DataFrame con los datos
        columna: Columna a analizar
        grupo_cols: Lista de columnas por las que agrupar
        nombres_grupos: Nombres para las columnas de grupo en el resultado
        
    Returns:
        pd.DataFrame: DataFrame con porcentajes por combinación de grupos
    """
    if columna not in df_data.columns:
        return None
    
    # Contar respuestas por grupos
    conteo = df_data.groupby(grupo_cols + [columna]).size().reset_index(name='Cantidad')
    
    # Calcular total por combinación de grupos
    total_por_grupo = df_data.groupby(grupo_cols).size().reset_index(name='Total')
    
    # Merge y calcular porcentaje DENTRO de cada combinación
    resultado = conteo.merge(total_por_grupo, on=grupo_cols)
    resultado['Porcentaje'] = (resultado['Cantidad'] / resultado['Total'] * 100).round(2)
    
    # Renombrar las columnas de grupo DESPUÉS de todos los cálculos
    rename_dict = {grupo_cols[i]: nombres_grupos[i] for i in range(len(grupo_cols))}
    resultado = resultado.rename(columns=rename_dict)
    
    return resultado


def calcular_estadisticas_por_grupo(df, columna_analizar, grupo_col):
    """
    Calcula estadísticas descriptivas por grupo
    
    Args:
        df: DataFrame con los datos
        columna_analizar: Columna numérica a analizar
        grupo_col: Columna por la que agrupar
        
    Returns:
        pd.DataFrame: DataFrame con estadísticas por grupo
    """
    stats = df.groupby(grupo_col)[columna_analizar].agg([
        ('Media', 'mean'),
        ('Mediana', 'median'),
        ('Máximo', 'max'),
        ('Mínimo', 'min'),
        ('Cantidad', 'count')
    ]).reset_index()
    
    return stats


def calcular_estadisticas_combinado(df, columna_analizar, grupo_cols):
    """
    Calcula estadísticas descriptivas por combinación de grupos
    
    Args:
        df: DataFrame con los datos
        columna_analizar: Columna numérica a analizar
        grupo_cols: Lista de columnas por las que agrupar
        
    Returns:
        pd.DataFrame: DataFrame con estadísticas por combinación
    """
    stats = df.groupby(grupo_cols)[columna_analizar].agg([
        ('Media', 'mean'),
        ('Mediana', 'median'),
        ('Cantidad', 'count')
    ]).reset_index()
    
    return stats


def necesita_filtro_modulo(columna):
    """
    Verifica si una columna necesita filtro de módulo especial
    
    Args:
        columna: Nombre de la columna a verificar
        
    Returns:
        tuple: (necesita_filtro, valor_modulo, descripcion)
    """
    for key, config in FILTROS_ESPECIALES.items():
        if COLUMNAS.get(key) == columna:
            return True, config.get('modulo'), config.get('descripcion')
    
    return False, None, None