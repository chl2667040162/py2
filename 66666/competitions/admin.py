from django.contrib import admin
from .models import Competition, Participant

@admin.register(Competition)
class CompetitionAdmin(admin.ModelAdmin):
    list_display = ('name', 'sport_type', 'location', 'start_date', 'status', 'created_by')
    list_filter = ('status', 'sport_type', 'is_public', 'start_date')
    search_fields = ('name', 'description', 'location')
    date_hierarchy = 'start_date'
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'description', 'sport_type', 'location')
        }),
        ('Даты и время', {
            'fields': ('start_date', 'end_date', 'registration_deadline')
        }),
        ('Участники', {
            'fields': ('max_participants', 'current_participants')
        }),
        ('Статус и доступ', {
            'fields': ('status', 'is_public', 'created_by')
        }),
        ('Системная информация', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('user', 'competition', 'registration_date', 'is_confirmed')
    list_filter = ('is_confirmed', 'competition')
    search_fields = ('user__username', 'competition__name')