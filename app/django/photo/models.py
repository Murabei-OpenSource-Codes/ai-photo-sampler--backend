"""Photos Sampled using the app."""
from django.db import models
from django.utils import timezone
from pumpwood_communication.serializers import PumpWoodJSONEncoder
from pumpwood_communication.exceptions import PumpWoodActionArgsException
from django.conf import settings
from pumpwood_viewutils.action import action
from core.singletons import storage_object, base_path
from experiment.models import DescriptionExperimentTeam


def change_path_upload(instance, filename):
    """Set path for image."""
    time_fmt = timezone.now().isoformat()
    return (
        "{base_path}/descriptionimage__file/"
        "{time_fmt}__{filename}").format(
        base_path=base_path, time_fmt=time_fmt,
        filename=filename.replace(" ", "_").lower())


class DescriptionImage(models.Model):
    """Images sampled using App or Web site."""

    hash = models.CharField(
        max_length=40, unique=True, null=True, blank=True,
        verbose_name="Unique hash",
        help_text="Unique hash associated with each photo from app")

    app_label = models.CharField(
        max_length=154, unique=False, blank=True, null=True,
        verbose_name="App label", help_text="Label used on app")

    description = models.CharField(
        max_length=154, unique=False, blank=True, null=True,
        verbose_name="Short description",
        help_text="Short description")
    notes = models.TextField(
        null=False, default="", blank=True,
        verbose_name="Notes", help_text="Notes about the photo")

    dimension = models.JSONField(
        encoder=PumpWoodJSONEncoder, null=False, default=dict,
        blank=True, verbose_name="Dimentions",
        help_text="Key/Value Dimentions")
    extra_info = models.JSONField(
        encoder=PumpWoodJSONEncoder, null=False, default=dict,
        blank=True, verbose_name="Extra information",
        help_text="Extra information")

    file = models.ImageField(
        null=True, blank=True,
        upload_to=change_path_upload,
        verbose_name="Image file",
        help_text="Image file")

    image_created_at = models.DateTimeField(
        null=True, verbose_name="Date/Time image creation",
        help_text="Date/Time image creation")
    image_uploaded_at = models.DateTimeField(
        null=True, verbose_name="Date/Time image uploaded",
        help_text="Date/Time image uploaded")
    image_created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
        blank=False, related_name='images_uploaded',
        verbose_name="User that created image",
        help_text="User that created image")

    obj_created_at = models.DateTimeField(null=True)
    obj_created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
        blank=False, related_name='images_created')
    team = models.ForeignKey(
        DescriptionExperimentTeam, on_delete=models.SET_NULL, null=True,
        blank=False, related_name='images_uploaded')
    inactive = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.app_label} - {self.image_created_at}"

    class Meta:
        unique_together = ('description', 'team')
        db_table = "photo__description"
        verbose_name = 'Sampled image'
        verbose_name_plural = 'Sampled images'

    def save(self, *args, **kwargs):
        """On save, update timestamps."""
        if not self.id:
            self.obj_created_at = timezone.now()
        return super(DescriptionImage, self).save(*args, **kwargs)

    @action(info="Remove image file from object.")
    def remove_image_file(self):
        """
        Remove image file from object.

        Args:
            No Args.
        Kwargs:
            No Kwargs.
        """
        if self.file is None:
            raise PumpWoodActionArgsException(
                "file is None can not be deleted")

        if self.file.name:
            storage_object.delete_file(file_path=self.file.name)
        self.file = None
        self.image_created_at = None
        self.image_uploaded_at = None
        self.image_created_by = None
        self.save()
        return True
