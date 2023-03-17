from django.test import TestCase
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import APIException
from rest_framework import status
from rest_framework.response import Response

# Create your tests here.

class BadRequest(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _('Bad request.')
    default_code = 'bad_request'

def to_success(data=None, message=None, status_code=status.HTTP_200_OK):
    return {
        "status_code": status_code,
        "message": message,
        "data": data,
    }


def http_response(data=None, message=None, status_code=status.HTTP_200_OK):
    return Response(
        {
            "status_code": status_code,
            "message": message,
            "data": data,
        },
        status_code,
    )