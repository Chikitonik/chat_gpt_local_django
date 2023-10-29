from django.contrib import admin

from .models import QueryLog


class QueryLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'timestamp', 'query', 'answer')


admin.site.register(QueryLog, QueryLogAdmin)
