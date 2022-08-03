from django.contrib import admin

# Register your models here.

from .models import Entry

class EntryAdmin(admin.ModelAdmin):

    list_display = ('user', 'day', 'working_hours', 'note')
    
    


admin.site.register(Entry, EntryAdmin)
