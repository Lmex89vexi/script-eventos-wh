import requests
from loguru import logger
from datetime import datetime
import os

from api_server_request import api_server_get_request

# ===================== servicios APISOL-INTERNO =====================
APISOL_INTERNO = os.getenv("APISOL_INTERNO", "http://localhost:44365")
URL_QUERY_EVENTOS_BY_DATE = "/v1/solicitud/webhook/status/{}/"
URL_EXEC_EVENTO_FASE_WH = "/v1/solicitud/{}/webhook/{}/"
# ===================== servicios APISOL-INTERNO =====================

# ===================== PARAMS TO main ===============================
DATE_START = "2023-12-07 20:00:00"
DATE_END = "2023-12-11 12:00:29"
STATUS_FAILED = -1
# ===================== PARAMS TO main ===============================

# ===================== CONSTANTES ===============================
HTTP_SESSION = requests.Session()
APPLICATION_JSON = "application/json"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
# ===================== CONSTANTES ===============================



def main(date_start, date_end, status: int):
    date_start = datetime.strptime(date_start, DATE_FORMAT)
    date_end = datetime.strptime(date_end, DATE_FORMAT)

    params = {"date_start": date_start, "date_end": date_end}

    eventos_wh = api_server_get_request(
        url=APISOL_INTERNO + URL_QUERY_EVENTOS_BY_DATE.format(status), params=params
    )

    if not eventos_wh:
        return

    logger.info(f"---Total de eventos a completar {len(eventos_wh.get('data'))} --- ")

    for evento in eventos_wh.get("data"):
        id_solicitud = evento.get("id_solicitud")
        id_evento = evento.get("id_evento")
        id_fase = evento.get(
            "id_fase",
        )

        try:
            response = api_server_get_request(
                url=APISOL_INTERNO + URL_EXEC_EVENTO_FASE_WH.format(id_solicitud, id_fase)
            )
            logger.info(
                f" --- id_solicitud {id_solicitud} id_evento {id_evento} id_fase {id_fase} ----- response {response}"
            )
        except Exception as exc:
            logger.error(
                f" ---Error en mandar evento wh id_solicitud {id_solicitud} evento: {id_evento} id_fase {id_fase}   {exc}"
            )


if __name__ == "__main__":
    main(date_start=DATE_START, date_end=DATE_END, status=STATUS_FAILED)
