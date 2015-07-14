from django.conf.urls import include, url

urlpatterns = [
    url(r'^$', 'api.views.api_documentation', name='api_documentation'),
    url(r'^house-codes$', 'api.views.house_codes', name='house_code'),
    url(r'^valve/house-code$', 'api.views.valve_view', name='valve_view'),
]
