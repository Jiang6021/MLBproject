from django.contrib import admin
from myapp.models import student

#admin.site.register(student)

class studentAdmin(admin.ModelAdmin):
    list_display = ('id', 'cName', 'cSex', 'cBirthday', 'cEmail', 'cPhone', 'cAddr')  # 後台顯示的欄位
    list_filter = ('cName', 'cSex')  # 可以篩選的欄位（右側 filter）
    search_fields = ('cName',)  # 支援搜尋的欄位
    ordering = ('id',)  # 預設排序方式

# 註冊模型到後台，並使用自訂的顯示方式
admin.site.register(student, studentAdmin)