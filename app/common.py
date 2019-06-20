from aiohttp.web import middleware, json_response
from jsonschema import validate, ValidationError


class ApiError(Exception):
    """
    Базовый класс для возврата ошибок из API
    Перехватывается в middleware для сериализации
    """

    def __init__(self, status_code: int, message: str = None):
        self.status_code = status_code
        self.message = message


@middleware
async def error_middleware(request, handler):
    """
    Миддлваря для обработки ошибок Api
    """
    try:
        return await handler(request)
    except ApiError as e:
        return json_response({
            'success': False,
            'error': e.message
        }, status=e.status_code)


def validate_data(data, schema: dict):
    """
    Проверяет входящие данные с помощью json schema
    Возвращает ошибку, если валидация не прошла
    """
    try:
        validate(data, schema)
    except ValidationError as e:
        raise ApiError(400, str(e))
