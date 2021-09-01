from django.contrib import admin
from pages.models import Contract, Message

# Register your models here.

@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'location', 'item', 'price', 'created_at')