from django.contrib import admin
from .models import UserFile, FileText

# Register your models here.


admin.site.register((UserFile, FileText))