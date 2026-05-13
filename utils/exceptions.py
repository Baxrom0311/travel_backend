"""Custom exception handler for consistent JSON error responses."""
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status


def custom_exception_handler(exc, context):
    """
    Barcha DRF xatolarini bir xil JSON formatida qaytaradi:
    {
        "success": false,
        "status_code": 404,
        "error": "Not found.",
        "detail": ...
    }
    """
    response = exception_handler(exc, context)

    if response is not None:
        response.data = {
            'success':     False,
            'status_code': response.status_code,
            'error':       str(exc),
            'detail':      response.data,
        }

    return response
