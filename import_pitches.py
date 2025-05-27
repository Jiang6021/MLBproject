# import_pitches.py
import pandas as pd
from myapp.models import Pitch
from django.utils.dateparse import parse_date
import django
import os
import sqlite3


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "你的專案名稱.settings")
django.setup()

df = pd.read_sql("SELECT * FROM yamamoto_pitching", sqlite3.connect("yamamoto.db"))

for _, row in df.iterrows():
    Pitch.objects.create(
        game_date=parse_date(row["game_date"]),
        pitch_type=row.get("pitch_type"),
        release_speed=row.get("release_speed"),
        description=row.get("description"),
        stand=row.get("stand"),
        balls=row.get("balls"),
        strikes=row.get("strikes"),
        release_pos_x=row.get("release_pos_x"),
        release_pos_z=row.get("release_pos_z"),
    )
