from django.contrib import admin
from .models import (
	Shift, Role, User,
	Incident, GeneralComment, ShiftHandOver,
	FileDirectory, FileViews
)

# Register your models here.
admin.site.register(Shift)
admin.site.register(Role)
admin.site.register(User)
admin.site.register(Incident)
admin.site.register(GeneralComment)
admin.site.register(ShiftHandOver)
admin.site.register(FileDirectory)
admin.site.register(FileViews)