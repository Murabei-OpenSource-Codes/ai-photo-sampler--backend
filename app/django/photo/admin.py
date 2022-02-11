import base64
import datetime
from django.utils import timezone
from django.contrib import admin
from django.db.models import Q
from photo.models import DescriptionImage
from django.utils.html import format_html
from core.singletons import storage_object
from django.contrib.admin import SimpleListFilter
from django.contrib import messages
from flat_json_widget.widgets import FlatJsonWidget
from django import forms


class EmptyFileFilter(SimpleListFilter):
    title = 'With file'
    parameter_name = 'with_files'

    def lookups(self, request, model_admin):
        return [
            ("yes", "yes"),
            ("no", "no")]

    def queryset(self, request, queryset):
        value = self.value()
        if value == "yes":
            return queryset.exclude(
                Q(file='') | Q(file=None))
        elif value == "no":
            return queryset.filter(
                Q(file='') | Q(file=None))
        return queryset


class DescriptionImageForm(forms.ModelForm):
    class Meta:
        widgets = {
            'dimension': FlatJsonWidget,
            'extra_info': FlatJsonWidget,
        }


class DescriptionImageAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'app_label', 'description', 'team',
        'image_created_at', 'with_file', 'inactive']
    list_display_links = list_display
    search_fields = ['app_label', 'description']
    readonly_fields = [
        'app_label', 'thumbnail', 'image_created_at', 'image_uploaded_at',
        'image_created_by', 'hash', 'obj_created_at', 'obj_created_by',
        'team']

    list_filter = [EmptyFileFilter, 'image_created_at', 'team', 'inactive']
    list_per_page = 30
    inlines = []
    form = DescriptionImageForm

    fieldsets = [
        ['General Information', {
            'fields': (
                "app_label", "description", "notes", "team",
                "obj_created_at", "obj_created_by", "inactive")}],
        ['Image', {
            'fields': (
                "file", "thumbnail", "image_created_at",
                "image_uploaded_at", "image_created_by")}],
        ['Dimentions/Extra Info.', {
            'fields': (
                "dimension", "extra_info",)}],
    ]

    def save_model(self, request, obj, form, change):
        if obj.id is None:
            obj.obj_created_by = request.user
            obj.obj_created_at = timezone.now()
            obj.team_id = request.user.experiment_team.team_id

        if 'file' in form.changed_data:
            temp_time = timezone.now()
            obj.image_created_at = temp_time
            obj.image_uploaded_at = temp_time
            obj.image_created_by = request.user
        obj.save()

    def thumbnail(self, obj):
        if obj.file.name:
            template = (
                "<img src='data:image/jpeg;base64,{base}' "
                "style='width: 100%;'/>")
            results = storage_object.read_file(obj.file.name)["data"]
            base64_encoded_data = base64.b64encode(results)
            image64 = base64_encoded_data.decode('utf-8')
            html = format_html(template.format(base=image64))
            return html
        else:
            return ""
    thumbnail.allow_tags = True
    thumbnail.__name__ = 'Thumbnail'

    def with_file(self, obj):
        return obj.file.name != ""

    def get_queryset(self, request):
        qs = super(DescriptionImageAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs

        return qs.filter(
            Q(team=request.user.profile.experiment_team.team_id) | Q(team__isnull=True))

    def has_add_permission(self, request, obj=None):
        if request.user.experiment_team.team_id is None:
            return False
        else:
            return True

    @admin.action(description='Remove images from objects')
    def remove_file(self, request, queryset):
        """Admin action to remove files from objects."""
        not_null_images = list(queryset.filter(file__isnull=False))
        for obj in not_null_images:
            obj.remove_image_file()

        self.message_user(
            request, '%d file(s) removed.' % len(not_null_images),
            messages.SUCCESS)

    @admin.action(description='Toggle inactive')
    def set_inactive(self, request, queryset):
        list_inactive = list(queryset.filter(
            inactive=True).values_list('id', flat=True))
        list_active = list(queryset.filter(
            inactive=False).values_list('id', flat=True))

        n_set_active = queryset.filter(
            id__in=list_inactive).update(inactive=False)
        n_set_inactive = queryset.filter(
            id__in=list_active).update(inactive=True)
        msg_template = "{} image(s) set as inactive; {} set as active"
        self.message_user(
            request, msg_template.format(n_set_inactive, n_set_active),
            messages.SUCCESS)
    actions = [remove_file, set_inactive]


admin.site.register(DescriptionImage, DescriptionImageAdmin)
