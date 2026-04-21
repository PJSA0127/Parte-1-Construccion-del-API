# 🚀 Crypto Dashboard 

¡Bienvenido a la versión avanzada de la API de Criptomonedas! Este proyecto ha sido transformado de una API básica a un **Dashboard Interactivo completo** con análisis de mercado, conversor de divisas, gráficos históricos y sistema de alertas.

## 🌟 Nuevas Funcionalidades
- **Dashboard Interactivo:** Interfaz moderna construida con HTML5, CSS3 (Bootstrap 5) y jQuery.
- **Análisis Histórico (Gráficos):** Visualización de la evolución de precios de los últimos 7 días mediante gráficos de barras dinámicos (**Chart.js**).
- **Conversor de Divisas:** Calcula el valor de cualquier criptomoneda en USD, EUR o COP en tiempo real.
- **Análisis de Volatilidad:** Clasificación inteligente de activos en "Alta Volatilidad" (>5%) y "Baja Volatilidad" (<5%) basándose en el cambio de las últimas 24h.
- **Sistema de Alertas:** Interfaz para programar notificaciones de precio por correo electrónico (Configuración SMTP incluida).
- **Detalles Profesionales:** Modales informativos que muestran Ranking, Market Cap y Símbolo sin necesidad de leer JSON crudo.
- **Arquitectura Asíncrona:** Migración completa de `requests` a `httpx` para un rendimiento superior y no bloqueante.

## 🛠️ Tecnologías Utilizadas
- **Backend:** Python 3.10+, FastAPI, Uvicorn, HTTPX (Async), Pydantic.
- **Frontend:** JavaScript (ES6+), jQuery 3.6, Chart.js, Bootstrap 5, FontAwesome 6.
- **API Externa:** CoinGecko V3.

## 🚀 Guía de Ejecución

### 1. Preparar el Entorno (Backend)
Si no has creado el entorno virtual, sigue estos pasos en la terminal:

```powershell
# Crear entorno virtual
python -m venv venv

# Activar en Windows
.\venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt httpx
```

### 2. Ejecutar el Servidor (API)
Inicia la API para que el dashboard pueda consumir los datos:

```powershell
uvicorn app.main:app --reload
```
La API estará disponible en: `http://127.0.0.1:8000`  
Documentación interactiva: `http://127.0.0.1:8000/docs`

### 3. Ejecutar el Frontend
No necesitas un servidor web adicional. Simplemente abre el archivo principal en tu navegador:

```powershell
start index.html
```

## 📁 Estructura del Proyecto (Mejorada)
- `app/main.py`: Punto de entrada con soporte para CORS y archivos estáticos.
- `app/settings.py`: Configuración centralizada de la App y SMTP.
- `app/services/`: Lógica asíncrona de conexión con CoinGecko.
- `static/css/`: Estilos personalizados para una UI moderna.
- `static/js/`: Lógica de interactividad, gráficos y consumo de API.
- `index.html`: Estructura principal del Dashboard.

