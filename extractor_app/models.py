from django.db import models

class ExtractedContent(models.Model):
    CONTENT_TYPE_CHOICES = [
        ('text', 'Text'),
        ('image', 'Image'),
        ('table', 'Table'),
    ]
    type = models.CharField(max_length=10, choices=CONTENT_TYPE_CHOICES)
    content = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
