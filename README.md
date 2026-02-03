# 📊 Dashboard de KPIs

Este es un dashboard interactivo construido con Streamlit para el análisis de KPIs a partir de encuestas de satisfacción. La aplicación permite a los usuarios subir un archivo Excel y visualiza automáticamente los datos a través de métricas y gráficos interactivos, facilitando la interpretación de los resultados por promoción y módulo.

## 🚀 Características Principales

-   **Carga de Archivos Flexible**: Sube tus datos en formato `.xlsx`.
-   **Procesamiento Automático**: Limpieza y validación de datos al instante.
-   **Agrupación Inteligente**: Agrupa los datos por promoción y, si está disponible, por módulo.
-   **Visualización de KPIs**: Métricas clave como total de respuestas, número de promociones/módulos, y medias de satisfacción.
-   **Análisis de Satisfacción**: Gráficos de barras que desglosan el cumplimiento de expectativas y la recomendaciones.
-   **Filtros Dinámicos**: Filtra los datos por promoción y/o módulo para un análisis más granular.
-   **Navegación por Pestañas**:
    -   `📈 KPIs Principales`: Vista general de los indicadores más importantes.
    -   `📊 Análisis por Promoción`: Métricas y gráficos agregados por promoción.
    -   `📚 Análisis por Módulo`: Métricas y gráficos agregados por módulo (si aplica).
    -   `📋 Datos`: Tabla con los datos filtrados.
    -   `🔢 Datos Agrupados`: Tabla con los datos agrupados y listos para descargar.
-   **Gráficos Interactivos**: Creados con Plotly para una mejor exploración de los datos.

## 🛠️ Instalación

Para ejecutar este proyecto localmente, sigue estos pasos:

1.  **Clona el repositorio:**
    ```bash
    git clone https://github.com/ytaylor/dashboard-kpis.git
    cd dashboard-kpis
    ```

2.  **Crea y activa un entorno virtual** (recomendado):
    ```bash
    python -m venv venv
    source venv/bin/activate  # En Windows usa `venv\Scripts\activate`
    ```

3.  **Instala las dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

## 🏃‍♀️ Cómo Empezar

Una vez instaladas las dependencias, puedes iniciar la aplicación con el siguiente comando:

```bash
streamlit run app.py
```

La aplicación se abrirá en tu navegador web. Simplemente arrastra y suelta o selecciona tu archivo Excel para comenzar el análisis.

### Formato del Archivo Excel

El archivo Excel debe contener al menos una columna llamada `Promoción`. Opcionalmente, puede incluir una columna `Módulo` para un análisis más detallado. Las columnas `Submitted At` y `Token` serán eliminadas automáticamente si existen.

## 📁 Estructura del Proyecto

```
/dashboard-kpis
├── app.py                  # Aplicación principal de Streamlit
├── requirements.txt        # Dependencias del proyecto
├── .gitignore              # Archivos ignorados por Git
├── README.md               # Este archivo
│
├── components/             # Módulos de la interfaz de usuario (sidebar, tabs)
│   ├── sidebar.py
│   └── tab_kpis.py
│   └── ...
│
├── config/                 # Configuraciones del proyecto
│   └── settings.py
│
└── utils/                  # Funciones de utilidad (procesamiento de datos, cálculos)
    ├── data_processor.py
    └── calculations.py
```

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Si tienes alguna idea o sugerencia para mejorar la aplicación, por favor abre un *issue* o envía un *pull request*.
