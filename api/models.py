from django.db import models
import os


# Create your models here.
class FileDirectory(models.Model):
    document = models.FileField(null=True, upload_to='documents/')
    description = models.TextField(null=True, blank=True)
    uploaded_at = models.DateTimeField(null=True, auto_now_add=True)

    def filename(self):
        return os.path.basename(self.document.name)

    def extension(self):
        name, extension = os.path.splitext(self.document.name)
        return str(extension).replace('.', '')

    def __str__(self):
        return self.document.name


class FileViews(models.Model):
    file = models.ForeignKey(FileDirectory, on_delete=models.CASCADE)
    number_of_views = models.DecimalField(
        default=0,max_digits=10, decimal_places=2
    )

    def __str__(self):
        self.file.document.name + ': ' + self.number_of_views
