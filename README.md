# Google Calendar to PDF Generator

Este proyecto permite obtener eventos de un calendario de Google y generar un archivo PDF con la información.

## Requisitos

- Python 3.8+
- Una cuenta de Google con acceso a Google Calendar
- Un archivo de credenciales JSON para autenticación

## Instalación

1. Clona este repositorio:
   ```sh
   git clone https://github.com/teck007/google-calendar-to-pdf.git
   cd google-calendar-to-pdf
   ```

2. Crea un entorno virtual y actívalo:
   ```sh
   python -m venv venv
   source venv/bin/activate  # En Windows usa: venv\Scripts\activate
   ```

3. Instala las dependencias:
   ```sh
   pip install -r requirements.txt
   ```

## Configuración

1. Agrega tu archivo de credenciales JSON en la carpeta del proyecto y actualiza `config.json` con la ruta del archivo.
2. En `config.json`, configura el ID del calendario que deseas consultar.

Formato de `config.json`:
```json
{
  "app": {
    "credential_file": "ruta/al/archivo-de-credenciales.json",
    "calendar_id": "tu_calendario_id"
  }
}
```

## Uso

Ejecuta el script pasando el año y mes como parámetros:
```sh
python main.py 2025 02
```
Esto generará un archivo PDF con los eventos del mes especificado.