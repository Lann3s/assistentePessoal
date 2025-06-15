import datetime
import os.path
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def formatar_evento(evento):
    nome = evento.get('summary', 'Sem título')
    inicio = evento['start'].get('dateTime', evento['start'].get('date'))

    try:
        # Trata ISO datetime, com ou sem fuso horário
        if 'T' in inicio:
            dt = datetime.datetime.fromisoformat(inicio.replace('Z', '+00:00'))
            data_formatada = dt.strftime('%d/%m às %H:%M')
        else:
            # Caso seja só uma data (evento dia inteiro)
            dt = datetime.datetime.fromisoformat(inicio)
            data_formatada = dt.strftime('%d/%m (o dia todo)')
    except Exception:
        data_formatada = inicio  # fallback bruto

    return f"{nome} - {data_formatada}"


def get_token_path():
    # Usa pasta local do usuário (ex: C:\Users\usuario_legal\AppData\Roaming\AssistenteDiario)
    appdata = os.getenv("APPDATA")
    dir_path = os.path.join(appdata, "AssistenteDiario")
    os.makedirs(dir_path, exist_ok=True)
    return os.path.join(dir_path, "token.pkl")


def get_calendar_service():

    creds = None
    token_path = get_token_path()

    if os.path.exists(token_path):
        with open(token_path, 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open(token_path, 'wb') as token:
            pickle.dump(creds, token)

    from googleapiclient.discovery import build
    service = build('calendar', 'v3', credentials=creds)
    return service


def get_today_events(service):
    now = datetime.datetime.utcnow().isoformat() + 'Z'
    end = (datetime.datetime.utcnow() +
           datetime.timedelta(hours=24)).isoformat() + 'Z'
    events_result = service.events().list(
        calendarId='primary',
        timeMin=now,
        timeMax=end,
        singleEvents=True,
        orderBy='startTime'
    ).execute()
    return events_result.get('items', [])
