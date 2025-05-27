from django.db import models

class Pitching(models.Model):  # 可日後支援多位投手
    game_date = models.DateField(null=True)
    pitch_type = models.CharField(max_length=10, blank=True, null=True)
    release_speed = models.FloatField(blank=True, null=True)
    release_spin_rate = models.FloatField(blank=True, null=True)
    description = models.CharField(max_length=50, blank=True, null=True)
    plate_x = models.FloatField(blank=True, null=True)
    plate_z = models.FloatField(blank=True, null=True)
    pfx_x = models.FloatField(blank=True, null=True)
    pfx_z = models.FloatField(blank=True, null=True)
    pitch_number = models.IntegerField(blank=True, null=True)
    inning = models.IntegerField(blank=True, null=True)
    outs_when_up = models.IntegerField(blank=True, null=True)
    batter = models.IntegerField(blank=True, null=True)
    events = models.CharField(max_length=50, blank=True, null=True)
    game_pk = models.IntegerField()
    at_bat_number = models.IntegerField()

    class Meta:
        unique_together = ('game_pk', 'at_bat_number', 'pitch_number')


    def __str__(self):
        return f"{self.game_date} | Game {self.game_pk} | AtBat {self.at_bat_number} | Pitch {self.pitch_number}"