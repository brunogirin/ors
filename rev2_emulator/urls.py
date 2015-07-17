from django.conf.urls import include, url

urlpatterns = [
    url(r'^$', 'rev2_emulator.views.emulator_view', name='emulator_view'),
    url(r'^temperature-opentrv$', 'rev2_emulator.views.temperature_opentrv_view', name='temperature-opentrv'),
    url(r'^ds18b20-temperature$', 'rev2_emulator.views.ds18b20_temperature_view', name='ds18b20-temperature'),
    url(r'^button$', 'rev2_emulator.views.button_view', name='button'),
    url(r'^led$', 'rev2_emulator.views.led_view', name='led'),
    url(r'^synchronising$', 'rev2_emulator.views.synchronising_view', name='synchronising'),
    url(r'^relative-humidity$', 'rev2_emulator.views.relative_humidity_view', name='relative-humidity'),
    url(r'^window$', 'rev2_emulator.views.window_view', name='window'),
    url(r'^last-updated$', 'rev2_emulator.views.last_updated_view', name='last-updated'),
    url(r'^last-updated-temperatures$', 'rev2_emulator.views.last_updated_temperatures_view', name='last-updated-temperatures'),
    url(r'^get-statuses$', 'rev2_emulator.views.get_statuses', name='get-statuses'),
]
