from django.conf import settings
import hashlib

def md5(data_string):
    obj = hashlib.md5(settings.SECRET_KEY.encode('utf-8'))
    obj.update(data_string.encode('utf-8'))
   # dddd滚滚滚1111
    return obj.hexdigest()


