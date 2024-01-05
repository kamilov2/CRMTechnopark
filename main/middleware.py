import hashlib
from django.http import HttpResponseForbidden

class UniqueDeviceMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        device_info = f"{request.META.get('HTTP_USER_AGENT')}_{request.META.get('REMOTE_ADDR')}"
        device_id = hashlib.sha256(device_info.encode()).hexdigest()
        print(device_id)
        if not request.COOKIES.get('device_id'):
        
            request.COOKIES['device_id'] = device_id

        request.device_id = device_id
        response = self.get_response(request)
        response.set_cookie('device_id', device_id)

        return response


class BlockOtherDevicesMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        allowed_device_id = '34e7b7c9a656aeec548596a30749c98bd2ca2191ca297517cb6b2d8227480a4a'
        current_device_id = getattr(request, 'device_id', None)

        if current_device_id != allowed_device_id:
            return HttpResponseForbidden("Доступ запрещен .")

        response = self.get_response(request)
        return response
