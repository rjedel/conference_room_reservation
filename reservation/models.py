from django.db import models


class Room(models.Model):
    name = models.CharField(max_length=255, unique=True)
    capacity = models.SmallIntegerField()
    projector = models.BooleanField()


class Reservation(models.Model):
    date = models.DateField()
    room = models.ForeignKey('Room', on_delete=models.CASCADE, related_name='reservations')
    comment = models.CharField(max_length=128, blank=True)

    class Meta:
        unique_together = ('date', 'room',)
