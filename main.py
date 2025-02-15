import os, locale, json, argparse
from google.oauth2 import service_account
from googleapiclient.discovery import build
from reportlab.lib.pagesizes import letter, landscape
from reportlab.pdfgen import canvas
from datetime import datetime
from calendar import monthrange

with open("config.json", "r") as f:
    config = json.load(f)

SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]
SERVICE_ACCOUNT_FILE = os.path.dirname(__file__) + config["app"]["credential_file"]  # Ruta al archivo JSON de credenciales

def obtener_eventos(calendar_id, año, mes):
    creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build("calendar", "v3", credentials=creds)
    primer_dia = datetime(año, mes, 1).isoformat() + "Z"  # Primer día del mes
    ultimo_dia = datetime(año, mes, monthrange(año, mes)[1]).isoformat() + "Z"  # Último día del mes

    eventos_resultado = service.events().list(
        calendarId=calendar_id,  # Usar el calendarId específico
        timeMin=primer_dia,
        timeMax=ultimo_dia,
        singleEvents=True,
        orderBy="startTime"
    ).execute()

    return eventos_resultado.get("items", [])

def generar_pdf_calendario(eventos, año, mes):
    meses = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
    nombre_mes =meses[mes-1]
    archivo_pdf = f'calendario{nombre_mes}.pdf'
    # Cambiar a orientación horizontal
    c = canvas.Canvas(f"calendario {nombre_mes}.pdf", pagesize=landscape(letter))

    # Obtener el mes y año actual
    locale.setlocale(locale.LC_TIME, 'es_CL.utf8')

    # Obtener el número de días en el mes y el día de la semana en que comienza
    num_dias = monthrange(año, mes)[1]
    primer_dia_semana = monthrange(año, mes)[0]  # 0 = Lunes, 6 = Domingo

    # Configuración de la cuadrícula
    ancho_celda = 110  # Aumentar el ancho de las celdas para orientación horizontal
    alto_celda = 120   # Aumentar el alto de las celdas
    margen_x = 10
    margen_y = 590     # Ajustar el margen vertical para orientación horizontal
    espacio_entre_celdas = 2

    # Dibujar el título del mes
    c.setFont("Helvetica", 7)
    c.drawString(margen_x, margen_y, f"Calendario de {nombre_mes} {año}")
    margen_y -= 10

    # Dibujar los días de la semana
    dias_semana = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]
    for i, dia in enumerate(dias_semana):
        x = margen_x + i * (ancho_celda + espacio_entre_celdas)
        c.drawString(x, margen_y, dia)
    margen_y -= 10

    # Dibujar la cuadrícula del calendario
    x_inicial = margen_x
    y_inicial = margen_y
    dia_actual = 1

    for semana in range(6):  # Máximo 6 semanas en un mes
        for dia_semana in range(7):  # 7 días por semana
            if (semana == 0 and dia_semana < primer_dia_semana) or dia_actual > num_dias:
                # Celda vacía si no corresponde a un día del mes
                pass
            else:
                # Dibujar el número del día
                x = x_inicial + dia_semana * (ancho_celda + espacio_entre_celdas)
                y = y_inicial - semana * (alto_celda + espacio_entre_celdas)
                c.drawString(x + 5, y - 15, str(dia_actual))

                # Mostrar los eventos del día
                eventos_dia = [
                    evento for evento in eventos
                    if datetime.fromisoformat(evento["start"].get("dateTime", evento["start"].get("date"))).day == dia_actual
                ]
                y_evento = y - 30  # Posición inicial para los eventos
                for evento in eventos_dia:
                    nombre = evento.get("summary", "Sin título")
                    descripcion = evento.get("description", "")
                    inicio = evento["start"].get("dateTime", evento["start"].get("date"))
                    hora_evento = datetime.fromisoformat(inicio).strftime("%H:%M") if "T" in inicio else "Todo el día"

                    
                    # Mostrar el nombre del evento
                    c.drawString(x + 5, y_evento, f"{hora_evento} - {nombre[:20]}")  # Mostrar más caracteres en orientación horizontal
                    y_evento -= 12  # Espacio para la descripción

                    # Dividir la descripción en varias líneas
                    lineas_descripcion = descripcion.split("\n")
                    for linea in lineas_descripcion:
                        c.drawString(x + 5, y_evento, linea)
                        y_evento -= 12  # Espacio para la siguiente línea

                dia_actual += 1

    c.save()
    print(f"PDF generado: {archivo_pdf}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generar un PDF con eventos de Google Calendar.")
    parser.add_argument("year", type=int, help="Año del calendario (ej. 2025)")
    parser.add_argument("month", type=int, help="Mes del calendario (ej. 2 para febrero)")
    args = parser.parse_args()
    year = args.year
    month = args.month
    eventos = obtener_eventos(config["app"]["calendar_id"], year, month)
    if eventos:
        generar_pdf_calendario(eventos, year, month)
    else:
        print("No hay eventos para este mes.")