"""
Configuración y constantes del dashboard
"""

# Configuración de la página
PAGE_CONFIG = {
    'page_title': 'Dashboard KPIs',
    'layout': 'wide'
}

# Columnas del Excel
COLUMNAS = {
    'promocion': 'Por favor, elige la promoción a la que perteneces',
    'modulo': 'Por favor, elige el módulo que vas a valorar',
    'expectativas': '¿Ha cumplido el Bootcamp de Data Analytics de Adalab tus expectativas?',
    'expectativas_IA': '¿Los contenidos de los talleres han cumplido tus expectativas?',
    'expectativas PW': '¿Ha cumplido el Bootcamp de programación web de Adalab tus expectativas?',
    'recomendacion': '¿Recomendarías Adalab a otras mujeres?', 
    "recomendacion_IA": '¿Recomendarías estos talleres a otras alumnas?'
}

# Columnas a eliminar automáticamente
COLUMNAS_ELIMINAR = ['Submitted At', 'Token']

# NUEVO: Configuración de filtros especiales por pregunta
FILTROS_ESPECIALES = {
    'expectativas': {
        'modulo': 'Módulo 4',  # Solo calcular para Módulo 4
        'descripcion': 'Esta pregunta se calcula solo para el Módulo 4'
    }, 
    # Se pueden agregar más preguntas con filtros especiales aquí
    "recomendacion": {
        'modulo': 'Módulo 4',  # No hay filtro especial
        'descripcion': 'Esta pregunta se calcula solo para el Módulo 4'
    },
    "expectativas_IA": {
        'modulo': None,  # No hay filtro especial
        'descripcion': 'Esta pregunta se calcula para todos los módulos'
    },
    "expectativas_PW": {
          'modulo': 'Módulo 4',  # No hay filtro especial
        'descripcion': 'Esta pregunta se calcula solo para el Módulo 4'
    }
}

# Tipos de agregación disponibles
AGREGACIONES = {
    "Media": 'mean',
    "Mediana": 'median',
    "Máximo": 'max',
    "Mínimo": 'min',
    "Conteo": 'count'
}

# Escalas de colores para gráficos
COLOR_SCALES = {
    'promocion': 'Blues',
    'modulo': 'Greens',
    'heatmap': 'YlOrRd',
    'media': 'Viridis',
    'mediana': 'Plasma',
    'modulo_media': 'Teal',
    'modulo_mediana': 'Mint'
}