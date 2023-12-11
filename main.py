import requests
from loguru import logger
from datetime import datetime
import os 

# ===================== servicios APISOL-INTERNO =====================
APISOL_INTERNO = os.getenv("APISOL_INTERNO")
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


def api_server_get_request(url: str, params=None):
    """This API server_get_request is called for ApisolInterno only if need it
    you need to create a new one, does not throw Exception when EntityNotFound

    Args:
        url (str): url para hacer get
        params (_type_, optional): . Defaults to None.

    Raises:
        ValueError: Raise Exception if different from 422

    Returns:
        _type_: response if success
    """

    head = {"Content-Type": APPLICATION_JSON}
    request = requests.Request("GET", url, headers=head, params=params)
    prepped = HTTP_SESSION.prepare_request(request)
    response = HTTP_SESSION.send(prepped)
    logger.debug(f"-----url {url} --- params {params} Response :{response}")
    if response.status_code in [200, 201]:
        return response.json()
    elif response.status_code == 422:
        logger.debug(f"422 Unprocessable Entity *** Response :{response}")
        return None
    else:
        logger.error(f"Error conexion a APISol-Interno Response :{response}")
        return None


def main(date_start, date_end, status: int):
    date_start = datetime.strptime(date_start, DATE_FORMAT)
    date_end = datetime.strptime(date_end, DATE_FORMAT)

    params = {"date_start": date_start, "date_end": date_end}

    eventos_wh = api_server_get_request(
        url=APISOL_INTERNO + URL_QUERY_EVENTOS_BY_DATE.format(status), params=params
    )

    if not eventos_wh:
        return

    logger.info(
        f"---Total de eventos a completar {len(eventos_wh.get('data'))} --- "
    )

    for evento in eventos_wh.get("data"):
        id_solicitud = evento.get("id_solicitud")
        id_evento = evento.get("id_evento")

        try:
            response = api_server_get_request(
                url=APISOL_INTERNO + URL_EXEC_EVENTO_FASE_WH.format(id_solicitud, id_evento)
            )
            logger.info(
                f" --- id_solicitud {id_solicitud} id_evento {id_evento}  ----- response {response}"
            )
        except Exception as exc:
            logger.error(
                f" ---Error en mandar evento wh id_solicitud {id_solicitud} evento: {id_evento}   {exc}"
            )


if __name__ == "__main__":
    main(date_start=DATE_START, date_end=DATE_END, status=STATUS_FAILED)
