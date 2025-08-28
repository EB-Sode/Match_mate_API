from django.contrib import admin
from .models import Predictions, MatchResult

# Register your models here.
admin.site.register(Predictions)
admin.site.register(MatchResult)