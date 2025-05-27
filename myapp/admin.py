from django.contrib import admin
from myapp.models import Pitching

#admin.site.register(student)

class PitchingAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'game_date', 'pitch_type', 'release_speed', 'release_spin_rate',
        'description', 'plate_x', 'plate_z', 'pfx_x', 'pfx_z', 'inning',
        'pitch_number', 'outs_when_up', 'batter', 'events'
    )
    list_filter = ('pitch_type', 'description', 'events')
    search_fields = ('pitch_type', 'description', 'events')
    ordering = ('game_date',)

# 註冊模型到後台，並使用自訂的顯示方式
#admin.site.register(student, studentAdmin)
admin.site.register(Pitching, PitchingAdmin)
