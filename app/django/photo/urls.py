"""Set urls for registration."""
from pumpwood_viewutils.routers import PumpWoodRouter
from django.conf.urls import url
from photo import rest


pumpwoodrouter = PumpWoodRouter()
pumpwoodrouter.register(viewset=rest.RestDescriptionImage)

urlpatterns = [
]

urlpatterns += pumpwoodrouter.urls
