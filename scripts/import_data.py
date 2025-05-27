# scripts/import_data.py
import os
import sys
import django
from datetime import date
#import pandas as pd
from pybaseball import statcast_pitcher

# 設定 Django 環境
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "firstproject.settings")
django.setup()

from myapp.models import Pitching

# ⚾ 抓取資料
yamamoto_id = 808967
start_date = "2025-03-01"
end_date = date.today().isoformat()

print(f"📥 抓取 {start_date} ～ {end_date} 的逐球資料...")
df = statcast_pitcher(start_date, end_date, yamamoto_id)

# 🧹 預處理
df = df.dropna(subset=["game_date", "game_pk", "at_bat_number", "pitch_number"])
df = df.drop_duplicates(subset=["game_pk", "at_bat_number", "pitch_number"])

# 🎯 把 DB 裡已存在的主鍵先撈出來（避免重複寫入）
existing_keys = set(
    Pitching.objects
    .values_list("game_pk", "at_bat_number", "pitch_number")
)

# 🔁 建立新物件清單
new_pitchings = []

for _, row in df.iterrows():
    key = (row["game_pk"], row["at_bat_number"], row["pitch_number"])
    if key in existing_keys:
        continue  # 跳過已存在資料

    new_pitchings.append(Pitching(
        game_pk=row["game_pk"],
        at_bat_number=row["at_bat_number"],
        pitch_number=row["pitch_number"],
        game_date=row["game_date"],
        pitch_type=row["pitch_type"],
        release_speed=row["release_speed"],
        release_spin_rate=row["release_spin_rate"],
        description=row["description"],
        plate_x=row["plate_x"],
        plate_z=row["plate_z"],
        pfx_x=row["pfx_x"],
        pfx_z=row["pfx_z"],
        inning=row["inning"],
        outs_when_up=row["outs_when_up"],
        batter=row["batter"],
        events=row["events"]
    ))

# ✅ 批次寫入
Pitching.objects.bulk_create(new_pitchings, batch_size=100)

print(f"✅ 寫入完成：新增 {len(new_pitchings)} 筆資料")
