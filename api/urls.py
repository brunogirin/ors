from django.conf.urls import include, url

urlpatterns = [
    url(r'^$', 'api.views.api_documentation', name='api_documentation'),
    url(r'^house-codes$', 'api.views.house_codes', name='house_code'),
    url(r'^valve/(?P<house_code>.*)$', 'api.views.valve_view', name='valve_view'),
    url(r'^led/(?P<house_code>.*)$', 'api.views.led_view', name='led_view'),
    url(r'^debug$', 'api.views.debug_view', name='debug_view'),
    url(r'^status/(?P<house_code>.*)$', 'api.views.status_view', name='status_view'),
]
