#!/usr/bin/python3
# -*- coding: utf-8 -*-
from rest_framework import serializers
from pumpwood_djangoviews.serializers import (
    ClassNameField, CustomNestedSerializer, DynamicFieldsModelSerializer)
from experiment.models import DescriptionExperimentTeam


########
# List #
########
class DescriptionExperimentTeamSerializer(DynamicFieldsModelSerializer):
    pk = serializers.IntegerField(source='id', allow_null=True, required=False)
    model_class = ClassNameField()

    class Meta:
        model = DescriptionExperimentTeam
        fields = (
            'pk', 'model_class', 'description', 'notes', 'dimensions',
            'created_by', 'created_at')
        read_only_fields = ['created_by', 'created_at']

    def create(self, validated_data):
        validated_data["created_by_id"] = self.context['request'].user.id
        return super(
            DescriptionExperimentTeamSerializer, self).create(validated_data)


class ExperimentTeamUserSerializer(DynamicFieldsModelSerializer):
    pk = serializers.IntegerField(source='id', allow_null=True, required=False)
    model_class = ClassNameField()

    class Meta:
        model = DescriptionExperimentTeam
        fields = (
            'pk', 'model_class', 'user_id', 'team_id')
