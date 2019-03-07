from django.contrib import admin
from .models import Student, Test
# Register your models here.


class TestInline(admin.TabularInline):
    model = Test
    extra = 1
    fieldsets = [
        (None, {'fields': ['test_name', 'points_for_test']})
    ]


class StudAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name', 'telegram_username', 'telegram_id']})
    ]
    inlines = [TestInline]


admin.site.register(Student, StudAdmin)
