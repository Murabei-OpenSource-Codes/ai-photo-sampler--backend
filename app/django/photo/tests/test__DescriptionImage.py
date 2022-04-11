"""Sets an example for nosetests using regen postgres image."""
import copy
import pandas as pd
import base64
import unittest
import requests
from pumpwood_communication.microservices import PumpWoodMicroService
from pumpwood_communication.exceptions import PumpWoodForbidden


microservice = PumpWoodMicroService(
    name="test_microservice", server_url="http://localhost:8000/")
auth_header = {
    'Authorization': 'Token 3f547e9b19c448189b69fa254f555c9df0774358'}
local_path = "photo/tests/%s"
user_1_token = {
    'Authorization': 'Token 67f1b127fbde50e8779d6eb1b815608133c65fe5'}


class TestDescriptionImage(unittest.TestCase):
    """Unittest class that helps building pumpwood based systems test."""

    load_balancer_address = "http://0.0.0.0:8080/"
    'Ip of the load balancer'
    apps_to_regenerate = [
        "pumpwood-auth-app", ]
    'Name of the apps to be regenerated after the test is over'

    test_address = "http://0.0.0.0:8000/"

    def setUp(self, *args, **kwargs):
        """Regen the database in the setUp calling reload end-point."""
        ######################
        # Regenerate database#
        for app in self.apps_to_regenerate:
            path = 'reload-db/' + app + '/'
            response = requests.get(self.load_balancer_address + path)
            if response.status_code != 200:
                raise Exception(app + ' regenerate: ', response.text)
        #####################

    def test__list(self):
        """Test if fill end-point is ok."""

        all_teams = microservice.list_without_pag(
            model_class="DescriptionExperimentTeam", auth_header=auth_header)

        list_results = microservice.list(
            "DescriptionImage", auth_header=auth_header)
        results = pd.DataFrame(list_results)
        self.assertTrue(results["team_id"].isna().all())

        list_results = microservice.list(
            "DescriptionImage", exclude_dict={
                "team_id": None}, auth_header=auth_header)
        results = pd.DataFrame(list_results)
        self.assertTrue(not results["team_id"].isna().any())

        list_results = microservice.list(
            "DescriptionImage", auth_header=user_1_token)
        results = pd.DataFrame(list_results)
        self.assertTrue((results["team_id"] == 1).all())

        list_results = microservice.list(
            "DescriptionImage", filter_dict={
                "team_id": 2}, auth_header=user_1_token)
        results = pd.DataFrame(list_results)
        self.assertTrue((results["team_id"] == 1).all())

    def test__list_without_pag(self):
        """Test if fill end-point is ok."""
        list_results = microservice.list_without_pag(
            "DescriptionImage", auth_header=auth_header)
        results = pd.DataFrame(list_results)
        self.assertTrue(results["team_id"].isna().all())

        list_results = microservice.list_without_pag(
            "DescriptionImage", exclude_dict={
                "team_id": None}, auth_header=auth_header)
        results = pd.DataFrame(list_results)
        self.assertTrue(not results["team_id"].isna().any())

        list_results = microservice.list_without_pag(
            "DescriptionImage", auth_header=user_1_token)
        results = pd.DataFrame(list_results)
        self.assertTrue((results["team_id"] == 1).all())

        list_results = microservice.list_without_pag(
            "DescriptionImage", filter_dict={
                "team_id": 2}, auth_header=user_1_token)
        results = pd.DataFrame(list_results)
        self.assertTrue((results["team_id"] == 1).all())

    def test__retrieve(self):
        """Test if fill end-point is ok."""
        file_not_null = microservice.retrieve(
            "DescriptionImage", pk=124, auth_header=auth_header)
        file_null = microservice.retrieve(
            "DescriptionImage", pk=1, auth_header=auth_header)

    def test__save_no_photo(self):
        """Test if fill end-point is ok."""
        microservice.fill_options(
            "DescriptionImage", {}, auth_header=auth_header)
        description = "app_label-12345"
        notes = "notes app_label-12345"

        with self.assertRaises(PumpWoodForbidden) as context:
            new_object = microservice.save({
                "model_class": "DescriptionImage",
                "description": description,
                "notes": notes}, auth_header=auth_header)
        self.assertIn(
            'User is not associated with a team',
            context.exception.message)

        description = "user 1 app_label-12345"
        notes = "notes app_label-12345"
        new_object = microservice.save({
            "model_class": "DescriptionImage",
            "description": description,
            "notes": notes}, auth_header=user_1_token)

        self.assertEqual(new_object["image_created_at"], None)
        self.assertEqual(new_object["image_created_by_id"], None)
        self.assertEqual(new_object["obj_created_by"], 1)
        self.assertNotEqual(new_object["obj_created_at"], None)
        self.assertEqual(new_object["description"], description)
        self.assertEqual(new_object["notes"], notes)
        self.assertEqual(new_object["team_id"], 1)

    def test__save_no_photo_setting_team(self):
        """Test if fill end-point is ok."""
        description = "app_label-12345"
        notes = "notes app_label-12345"
        new_object = microservice.save({
            "model_class": "DescriptionImage",
            "description": description,
            "notes": notes, "team_id": 5},
            auth_header=auth_header)

        self.assertEqual(new_object["image_created_at"], None)
        self.assertEqual(new_object["image_created_by_id"], None)
        self.assertEqual(new_object["obj_created_by"], 3)
        self.assertNotEqual(new_object["obj_created_at"], None)
        self.assertEqual(new_object["description"], description)
        self.assertEqual(new_object["notes"], notes)
        self.assertEqual(new_object["team_id"], 5)

    def test__save_photo(self):
        with open(local_path % "database/teste.jpeg", "rb") as file:
            file_data = file.read()
        msg = base64.b64encode(file_data)

        description = "app_label-12345"
        notes = "notes app_label-12345"
        hash = "hash-1234"
        new_object = microservice.save({
            "model_class": "DescriptionImage",
            "hash": hash,
            "description": description,
            "notes": notes,
            "image64": msg}, auth_header=user_1_token)
        result = microservice.retrieve_file(
            model_class="DescriptionImage", pk=new_object["pk"],
            file_field="file", auth_header=user_1_token, save_file=False)
        retrieve_data = result["content"]

        self.assertEqual(retrieve_data, file_data)
        self.assertEqual(new_object["image_created_at"], None)
        self.assertNotEqual(new_object["image_created_by_id"], None)
        self.assertNotEqual(new_object["image_uploaded_at"], None)
        self.assertEqual(new_object["obj_created_by"], 1)
        self.assertEqual(new_object["team_id"], 1)
        self.assertNotEqual(new_object["obj_created_at"], None)
        self.assertEqual(new_object["description"], description)
        self.assertEqual(new_object["notes"], notes)

        results = microservice.remove_file_field(
            model_class="DescriptionImage", pk=new_object["pk"],
            file_field="file", auth_header=user_1_token)
        self.assertEqual(results, True)
        obj = microservice.retrieve(
            model_class="DescriptionImage", pk=new_object["pk"],
            auth_header=user_1_token)


class TestDescriptionImageActions(unittest.TestCase):
    """Unittest class that helps building pumpwood based systems test."""

    load_balancer_address = "http://0.0.0.0:8080/"
    'Ip of the load balancer'
    apps_to_regenerate = [
        "pumpwood-auth-app", ]
    'Name of the apps to be regenerated after the test is over'

    test_address = "http://0.0.0.0:8000/"

    def setUp(self, *args, **kwargs):
        """Regen the database in the setUp calling reload end-point."""
        ######################
        # Regenerate database#
        for app in self.apps_to_regenerate:
            path = 'reload-db/' + app + '/'
            response = requests.get(self.load_balancer_address + path)
            if response.status_code != 200:
                raise Exception(app + ' regenerate: ', response.text)
        #####################

    def test__list_actions(self):
        actions = microservice.list_actions(
            model_class="DescriptionImage", auth_header=auth_header)
        actions_names = set([x["action_name"] for x in actions])
        self.assertEqual(actions_names, {"remove_image_file"})

    def test__remove_file(self):
        with open(local_path % "database/teste.jpeg", "rb") as file:
            file_data = file.read()
        msg = base64.b64encode(file_data)

        description = "app_label-12345"
        notes = "notes app_label-12345"
        hash = "hash-1234"
        new_object = microservice.save({
            "model_class": "DescriptionImage",
            "hash": hash,
            "description": description,
            "notes": notes,
            "image64": msg}, auth_header=user_1_token)
        result = microservice.execute_action(
            model_class="DescriptionImage", action="remove_image_file",
            pk=new_object["pk"], auth_header=auth_header)
        actual_data = microservice.retrieve(
            model_class="DescriptionImage", pk=new_object["pk"],
            auth_header=auth_header)
        self.assertEqual(actual_data["file"], None)
