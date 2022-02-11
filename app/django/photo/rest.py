"""View for photo end-point."""
import base64
from django.utils import timezone
from pumpwood_viewutils.views import PumpWoodRestService
from photo.serializers import SerializerDescriptionImage
from photo.models import DescriptionImage
from rest_framework.response import Response
from pumpwood_communication.exceptions import PumpWoodForbidden
from core.singletons import (
    storage_object, microservice, microservice__no_login)


class RestDescriptionImage(PumpWoodRestService):
    endpoint_description = "Images"
    notes = "Images sampled using app or web site"

    service_model = DescriptionImage
    serializer = SerializerDescriptionImage

    storage_object = storage_object
    microservice = microservice

    file_fields = {
        'file': ["jpeg", "jpg"]}
    list_fields = [
        "pk", "model_class", "hash", "app_label", "description", "notes",
        "dimentions", "file", "image_created_at", "image_uploaded_at",
        "image_created_by", "obj_created_at", "obj_created_by_id", "team_id",
        "inactive"]

    foreign_keys = {
        "team_id": {"model_class": "DescriptionExperimentTeam", "many": False},
        "image_created_by": {"model_class": "User", "many": False},
        "obj_created_by_id": {"model_class": "User", "many": False},
    }

    def list(self, request):
        is_superuser = request.user.is_superuser
        filter_dict = request.data.get("filter_dict", {})
        exclude_dict = request.data.get("exclude_dict", {})

        ###############################################
        # Checking if there is any query with team_id #
        team_id_query = False
        inactive_query = False
        keys = list(filter_dict.keys()) + list(exclude_dict.keys())
        for k in keys:
            if "team_id" in k:
                team_id_query = True
            if "inactive" in k:
                inactive_query = True

        ###############################################
        # Show only active images
        if not inactive_query:
            filter_dict["inactive"] = False
        # If not filter to only look over the self team_id
        if not (is_superuser and team_id_query):
            filter_dict["team_id"] = request.user.experiment_team.team_id

        ###############################################
        # set filter dict
        request.data["filter_dict"] = filter_dict
        return super(
            RestDescriptionImage, self).list(request)

    def list_without_pag(self, request):
        is_superuser = request.user.is_superuser
        filter_dict = request.data.get("filter_dict", {})
        exclude_dict = request.data.get("exclude_dict", {})

        ###############################################
        # Checking if there is any query with team_id #
        team_id_query = False
        inactive_query = False
        keys = list(filter_dict.keys()) + list(exclude_dict.keys())
        for k in keys:
            if "team_id" in k:
                team_id_query = True
            if "inactive" in k:
                inactive_query = True

        ###############################################
        # Show only active images
        if not inactive_query:
            filter_dict["inactive"] = False
        # If not filter to only look over the self team_id
        if not (is_superuser and team_id_query):
            filter_dict["team_id"] = request.user.experiment_team.team_id

        ###############################################
        # set filter dict
        request.data["filter_dict"] = filter_dict

        return super(
            RestDescriptionImage, self).list_without_pag(request)

    def save(self, request):
        #############################################
        # Checking if user can add image with team id
        profile_team_id = request.user.experiment_team.team_id
        request_team_id = request.data.get("team_id")
        if profile_team_id is None and request_team_id is None:
            raise PumpWoodForbidden(
                "User is not associated with a team so can not save "
                "DescriptionImage objects.")

        is_superuser = request.user.is_superuser
        if not is_superuser and request_team_id is not None:
            raise PumpWoodForbidden(
                "User is not a Super User and is trying to set a team_id to "
                "an image.")
        #############################################

        image64 = request.data.pop("image64", None)
        pk = request.data.get("pk", None)
        response = super(
            RestDescriptionImage, self).save(request)
        response_data = response.data

        obj = DescriptionImage.objects.get(id=response_data["pk"])
        if pk is None:
            # Ajustando para poder criar fotos para serem populadas por script
            obj.team_id = (
                request_team_id or profile_team_id)
            obj.obj_created_by_id = request.user.id

        ##############################################
        # If no photo was sent return the new object #
        if image64 is None:
            obj.save()
            return Response(
                self.serializer(obj).data,
                status=response.status_code)
        else:
            obj.save()

            #########################################################
            # Uploading data to bucket #request.user.experiment_team.team_id
            img = base64.b64decode(image64)
            file_path = 'descriptionimage__file/'
            filename = "{}.jpeg".format(obj.id)
            storage_filepath = storage_object.write_file(
                file_path=file_path, file_name=filename,
                data=img, content_type="image/jpeg",
                if_exists='overide')
            obj.file = storage_filepath
            obj.image_created_by_id = request.user.id
            obj.image_uploaded_at = timezone.now()
            obj.save()

        object_data = self.serializer(obj).data
        return Response(
            object_data, status=response.status_code)
