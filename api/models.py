from django.db import models
import os


class Shift(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    time_in = models.TimeField(null=True, blank=True, db_index=True)
    time_out = models.TimeField(null=True, blank=True, db_index=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.name:
            return self.name


class Role(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    abbreviation = models.CharField(max_length=10, null=True, blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.abbreviation and self.name:
            return self.abbreviation + ' - ' + self.name


class User(models.Model):
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(
        verbose_name='email address', max_length=255,
        unique=True, null=True, blank=True
    )
    role = models.ForeignKey(Role, on_delete=models.CASCADE, null=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email

PRIORITY = (('P1', 'First Priority'), ('P2', 'Second Priority'), ('P3', 'Third Priority'), ('P4', 'Fourth Priority'))


class Incident(models.Model):
    priority = models.CharField(max_length=5, choices=PRIORITY)
    incident = models.CharField(max_length=20, null=True)
    description = models.TextField(null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.incident


class GeneralComment(models.Model):
    comment = models.TextField(blank=True, null=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.comment


class ShiftHandOver(models.Model):
    date = models.DateField(null=True, blank=True)
    shift = models.ForeignKey(Shift, on_delete=models.CASCADE, null=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='receiver')
    shift_members = models.ManyToManyField(User, related_name='shift_members')
    incidents = models.ManyToManyField(Incident)
    comments = models.ManyToManyField(GeneralComment) 
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.shift:
            return self.shift.name


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
