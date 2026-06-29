# SmartPriority AI 

La aplicación está desarrollada con **Python + CustomTkinter**, utiliza una interfaz moderna tipo SaaS empresarial y se conecta a **PostgreSQL** para consultar usuarios, tickets, reportes, actividad, análisis IA y configuración SLA.

## Características principales

- Inicio de sesión conectado a PostgreSQL.
- Panel principal con KPIs reales desde la base de datos.
- Gestión de incidencias con búsqueda, filtros y registro de nuevos tickets.
- Análisis IA simulado mediante reglas y palabras clave.
- Clasificación automática por prioridad.
- Derivación inteligente por área y equipo sugerido.
- Métricas SLA y vencimiento de atención.
- Reportes con analíticas visuales.
- Configuración de reglas IA y SLA.
- Logo integrado en login, sidebar e ícono de ventana.

## Tecnologías utilizadas

- Python
- CustomTkinter
- PostgreSQL
- psycopg2-binary
- python-dotenv
- Pillow

## Instalación

Desde la carpeta principal del proyecto:

```bash
pip install -r requirements.txt
```

## Configuración de PostgreSQL

Primero crea la base de datos:

```sql
CREATE DATABASE smartpriority_ai;
```

Luego abre la base `smartpriority_ai` en pgAdmin o en tu gestor PostgreSQL y ejecuta:

```text
app/database/schema.sql
```

Ese archivo crea las tablas, relaciones, vistas, índices y datos iniciales.

## Configuración del archivo .env

Copia el archivo `.env.example` y renómbralo a `.env`:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=smartpriority_ai
DB_USER=postgres
DB_PASSWORD=tu_contraseña
```

Reemplaza `tu_contraseña` por la contraseña real de tu usuario PostgreSQL.

## Ejecutar el proyecto

```bash
python main.py
```

## Usuario demo

```text
Correo: admin@empresa.com
Contraseña: 123456
```

## Flujo del sistema

```text
Inicio de sesión
↓
Panel principal
↓
Registro de incidencia
↓
Análisis IA y NLP
↓
Clasificación automática
↓
Derivación inteligente
↓
Validación del operador
↓
Atención técnica
↓
Cierre del ticket
```
