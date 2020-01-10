import threading
from django.http import HttpResponse
from uuid import uuid4

from django.db import connections
from .utils import tenant_db_from_request

THREAD_LOCAL = threading.local()


class TenantMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        db = tenant_db_from_request(request)
        if db:
            setattr(THREAD_LOCAL, "DB", db)
            response = self.get_response(request)
            return response
        else:
            return HttpResponse('database not found', status=404)


def get_current_db_name():
    return getattr(THREAD_LOCAL, "DB", None)


def set_db_for_router(db):
    setattr(THREAD_LOCAL, "DB", db)
