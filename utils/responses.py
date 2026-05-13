"""Standard API response format for consistent JSON responses."""
from rest_framework.response import Response
from rest_framework import status as http_status


def ok(data=None, **meta) -> Response:
    """Standard success response."""
    payload = {'success': True}
    if data is not None:
        payload['data'] = data
    if meta:
        payload['meta'] = meta
    return Response(payload, status=http_status.HTTP_200_OK)


def created(data=None, message: str = '') -> Response:
    """Standard 201 created response."""
    payload = {'success': True}
    if message:
        payload['message'] = message
    if data is not None:
        payload['data'] = data
    return Response(payload, status=http_status.HTTP_201_CREATED)


def error(message: str, errors=None, status_code: int = 400) -> Response:
    """Standard error response."""
    payload = {
        'success': False,
        'error': message,
    }
    if errors is not None:
        payload['errors'] = errors
    return Response(payload, status=status_code)
