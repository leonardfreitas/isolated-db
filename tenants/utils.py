from django.db import connection


def hostname_from_request(request):
    # split on `:` to remove port
    return request.get_host().split(":")[0].lower()


def tenant_db_from_request(request):
    hostname = hostname_from_request(request)
    tenants_map = get_tenants_map()
    if tenants_map.get(hostname, False):
        return tenants_map.get(hostname)
    else:
        return False


def get_tenants_map():
    return {"thor.localhost": "thor", "potter.localhost": "potter"}
