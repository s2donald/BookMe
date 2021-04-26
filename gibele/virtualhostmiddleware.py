from django.conf import settings



virtual_hosts = {
    "hh5l.gibele.com:8000":"calendarapp.urls",
    "eurocharged-automotive.gibele.com:8000":"products.urls",
    "biz.bookme.com:8000":"businessadmin.urls",
    "biz.shopme.com:8000":"productadmin.urls",
    "shopme.com:8000":"products.urls",
    "bookme.com:8000":"calendarapp.urls",
    "marketplace.bookme.com:8000":"gibele.urls",
    "marketplace.bookme.to":"gibele.urls",
    "marketplace.gibele.com:8000":"gibele.urls",
    "biz.bookme.to":"businessadmin.urls",
    "biz.shopme.to":"productadmin.urls",
    "shopme.to":"products.urls",
    "bookme.to":"calendarapp.urls",
}

class VirtualHostMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        host = request.get_host()
        request.urlconf = virtual_hosts.get(host)
        domain = host.split('.')[1]
        tdl = host.split('.')[2]
        if settings.DEBUG:
            tdls = tdl.split(':')[0]
        else:
            tdls = tdl
        settings.DOMAIN_NAME = domain + '.' + tdls
        settings.PARENT_HOST = domain + '.' + tdl
        settings.SESSION_COOKIE_DOMAIN= domain + '.' + tdls
        # print(settings.DOMAIN_NAME)
        #Now we check if the domain comes from 
        if not (request.urlconf):
            subdomain = host.split('.')[0]
            myurl = domain + '.' + tdl
            request.urlconf = virtual_hosts.get(myurl)
        response = self.get_response(request)
        return response