from django.contrib import admin
from .models import Challenge, Participation, Progress

# Register your models here.
admin.site.register(Challenge)
admin.site.register(Participation)
admin.site.register(Progress)
