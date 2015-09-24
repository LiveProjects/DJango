from django.contrib import admin
#first input admin


#then input models
#
#finally register model name

from .models import Question
from .models import Choice

admin.site.register(Question)
admin.site.register(Choice)
