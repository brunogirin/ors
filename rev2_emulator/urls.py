from django.conf.urls import include, url

urlpatterns = [
    url(r'^$', 'rev2_emulator.views.emulator_view', name='emulator_view'),
]
