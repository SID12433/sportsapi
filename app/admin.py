from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.CustomUser)
admin.site.register(models.Message)
admin.site.register(models.Event)

admin.site.register(models.Position)
admin.site.register(models.Request)
admin.site.register(models.StudentDetails)

admin.site.register(models.Sponsored)
admin.site.register(models.Post)
admin.site.register(models.SponsorProfile)
admin.site.register(models.EventRegistration)
admin.site.register(models.College)
admin.site.register(models.Student)


