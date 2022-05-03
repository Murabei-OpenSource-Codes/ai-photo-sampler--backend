"""View for photo end-point."""
import base64
import datetime
from pumpwood_djangoviews.views import PumpWoodRestService
from experiment.serializers import DescriptionExperimentTeamSerializer
from experiment.models import DescriptionExperimentTeam
from rest_framework.response import Response
from pumpwood_communication.exceptions import PumpWoodForbidden
from core.singletons import (
    storage_object, microservice, microservice__no_login)


class RestDescriptionExperimentTeam(PumpWoodRestService):
    endpoint_description = "Experiment Teams"
    notes = "Team to peform an experiment photo collection."

    service_model = DescriptionExperimentTeam
    serializer = DescriptionExperimentTeamSerializer

    storage_object = storage_object
    microservice = microservice

    file_fields = {
        'file': ["jpeg", "jpg"]}
    list_fields = [
        "pk", "model_class", "description", "notes", "dimensions",
        "created_by", "created_at"]

    foreign_keys = {
        "created_by": {"model_class": "User", "many": False},
    }
