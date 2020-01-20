from django.contrib import admin
from .models import Customer, Address, City, State

# Register your models here.

admin.site.register(State)
admin.site.register(City)
admin.site.register(Address)


class AddressInline(admin.StackedInline):
    model = Address
    extra = 2


class CustomerAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Info ', {'fields': ['first_name', 'last_name']}),
        ('Contact', {'fields': ['email', 'mobile_no']}),
    ]
    inlines = [AddressInline]


admin.site.register(Customer, CustomerAdmin)