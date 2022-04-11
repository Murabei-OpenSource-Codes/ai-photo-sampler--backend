#!/usr/bin/python3
# -*- coding: utf-8 -*-
from rest_framework import serializers
from pumpwood_djangoviews.serializers import (
    ClassNameField, CustomNestedSerializer, DynamicFieldsModelSerializer)
from photo.models import DescriptionImage


########
# List #
########
class SerializerDescriptionImage(DynamicFieldsModelSerializer):
    pk = serializers.IntegerField(source='id', allow_null=True, required=False)
    model_class = ClassNameField()

    class Meta:
        model = DescriptionImage
        fields = (
            'pk', 'model_class', 'hash', 'app_label', 'description', 'notes',
            'dimentions', 'extra_info', 'file', 'image_created_at',
            'image_uploaded_at', 'image_created_by_id', 'obj_created_at',
            'obj_created_by_id', 'team_id', 'inactive')
        read_only_fields = ['obj_created_by_id', 'obj_created_at']

    def create(self, validated_data):
        validated_data["obj_created_by_id"] = self.context['request'].user.id
        return super(
            SerializerDescriptionImage, self).create(validated_data)
