from django.utils import timezone
from django.db import models
from pumpwood_communication.serializers import PumpWoodJSONEncoder
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver


class DescriptionExperimentTeam(models.Model):
    """Experiment team to associate the images."""

    description = models.CharField(
        max_length=154, unique=False, blank=True, null=True)
    notes = models.TextField(null=False, default="", blank=True)
    dimensions = models.JSONField(
        encoder=PumpWoodJSONEncoder, null=False, default=dict,
        blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
        blank=True, related_name='created_experiment_team',
        verbose_name="User that created team",
        help_text="User that created team")
    created_at = models.DateTimeField(
        blank=True, null=False, verbose_name="Date/Time team creation",
        help_text="Date/Time team creation")

    class Meta:
        db_table = "experiment__team"
        verbose_name = 'Experiment Team'
        verbose_name_plural = 'Experiment Teams'

    def __str__(self):
        return f"[{self.pk}] {self.description}"

    def save(self, *args, **kwargs):
        """On save, update timestamps."""
        if not self.id:
            self.created_at = timezone.now()
        return super(DescriptionExperimentTeam, self).save(*args, **kwargs)


class ExperimentTeamUser(models.Model):
    """Associate an user with an experiment team."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        verbose_name="User associated to team",
        help_text="User associated to team",
        related_name="experiment_team")
    team = models.ForeignKey(
        DescriptionExperimentTeam, on_delete=models.SET_NULL, null=True,
        blank=True, related_name='team',
        verbose_name="Team associated to user",
        help_text="Team associated to user")

    class Meta:
        db_table = "experiment__team_user"
        verbose_name = 'Team/User association'
        verbose_name_plural = 'Team/User associations'


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        ExperimentTeamUser.objects.create(user=instance)
