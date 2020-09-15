from django.db import models


class EncryptionData(models.Model):
    unique_string = models.CharField(max_length=50, unique=True)
    participants = models.PositiveIntegerField()
    threshold = models.PositiveIntegerField()
    shares = models.TextField()
    orginal_image = models.ImageField(upload_to='original_images')

    def __str__(self):
        return self.unique_string
