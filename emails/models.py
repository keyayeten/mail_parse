from django.db import models
from users.models import CustomUser


class EmailMessage(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    subject = models.CharField(max_length=200)
    sent_date = models.DateTimeField()
    received_date = models.DateTimeField()
    body = models.TextField()
    attachments = models.ManyToManyField('Attachment')


class Attachment(models.Model):
    file = models.FileField(upload_to='attachments/')
