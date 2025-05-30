import os
import uuid
from datetime import datetime, timedelta


def generate_and_save_ics(name: str, date: str, time: str, service: str):
    # Pasta onde os arquivos .ics estão armazenados
    ics_folder = 'ics_file'

    # Cria a pasta se não existir
    if not os.path.exists(ics_folder):
        os.makedirs(ics_folder)

    # 🔥 Limpa arquivos .ics da pasta correta
    for filename in os.listdir(ics_folder):
        if filename.endswith('.ics'):
            os.remove(os.path.join(ics_folder, filename))

    # 🔥 Verificação adicional: limpa .ics que estejam na raiz (opcional)
    for filename in os.listdir('.'):
        if filename.endswith('.ics'):
            os.remove(filename)

    # Dados do evento
    event_uid = str(uuid.uuid4())
    dt_start = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
    dt_end = dt_start + timedelta(hours=1)

    dtstamp = dt_start.strftime("%Y%m%dT%H%M%SZ")
    dtstart = dt_start.strftime("%Y%m%dT%H%M%SZ")
    dtend = dt_end.strftime("%Y%m%dT%H%M%SZ")

    ics_content = f"""
        BEGIN:VCALENDAR
        VERSION:2.0
        PRODID:-//The Barrio Barber//EN
        BEGIN:VEVENT
        UID:{event_uid}
        DTSTAMP:{dtstamp}
        DTSTART:{dtstart}
        DTEND:{dtend}
        SUMMARY:{service} at The Barrio Barber
        DESCRIPTION:Your appointment is confirmed at The Barrio Barber with {name}.
        LOCATION:The Barrio Barber - Your Location Address
        END:VEVENT
        END:VCALENDAR
    """

    # Nome e caminho do arquivo
    filename = f"{event_uid}.ics"
    filepath = os.path.join(ics_folder, filename)

    # Salvar o arquivo .ics na pasta correta
    with open(filepath, 'w') as f:
        f.write(ics_content.strip())

    return filepath
