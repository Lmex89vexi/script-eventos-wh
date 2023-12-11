import requests
from loguru import logger

# ===================== CONSTANTES ===============================
HTTP_SESSION = requests.Session()
APPLICATION_JSON = "application/json"
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
