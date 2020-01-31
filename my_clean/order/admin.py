from django.contrib import admin
from .models import Order, OrderTask, Team, Evaluation, DustLevelPrice, Services, Visit

# Register your models here.
admin.site.register(Services)
admin.site.register(DustLevelPrice)
admin.site.register(Order)
admin.site.register(OrderTask)
admin.site.register(Evaluation)
admin.site.register(Team)
admin.site.register(Visit)
