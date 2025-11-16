from django.db import models

class Room(models.Model):
    ROOM_TYPE_CHOICES = [
        ('VIP', 'VIP'),
        ('Kelas 1', 'Kelas 1'),
        ('Kelas 2', 'Kelas 2'),
        ('Kelas 3', 'Kelas 3'),
        ('ICU', 'ICU'),
    ]

    name = models.CharField(max_length=100)
    room_type = models.CharField(max_length=20, choices=ROOM_TYPE_CHOICES)
    capacity = models.PositiveIntegerField()
    daily_rate = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name