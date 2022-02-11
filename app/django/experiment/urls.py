"""Set urls for registration."""
from pumpwood_viewutils.routers import PumpWoodRouter
from django.conf.urls import url
from experiment import rest


pumpwoodrouter = PumpWoodRouter()
pumpwoodrouter.register(viewset=rest.RestDescriptionExperimentTeam)

urlpatterns = [
]

urlpatterns += pumpwoodrouter.urls
