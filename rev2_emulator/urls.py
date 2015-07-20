from django.conf.urls import include, url

urlpatterns = [
    url(r'^$', 'rev2_emulator.views.emulator_view', name='emulator_view'),
    url(r'^temperature-opentrv$', 'rev2_emulator.views.temperature_opentrv_view', name='temperature-opentrv'),
    url(r'^temperature-ds18b20$', 'rev2_emulator.views.temperature_ds18b20_view', name='temperature-ds18b20'),
    url(r'^switch$', 'rev2_emulator.views.switch_view', name='button'),
    url(r'^synchronising$', 'rev2_emulator.views.synchronising_view', name='synchronising'),
    url(r'^relative-humidity$', 'rev2_emulator.views.relative_humidity_view', name='relative-humidity'),
    url(r'^window$', 'rev2_emulator.views.window_view', name='window'),
    url(r'^last-updated-all$', 'rev2_emulator.views.last_updated_all_view', name='last-updated'),
    url(r'^last-updated-temperature$', 'rev2_emulator.views.last_updated_temperature_view', name='last-updated-temperature'),
    url(r'^get-statuses$', 'rev2_emulator.views.get_statuses', name='get-statuses'),
]
