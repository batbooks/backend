from django.db import models

# Create your models here.
class TagCategory(models.Model):
    title = models.CharField(max_length=256, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title

class Tag(models.Model):
    title = models.CharField(max_length=256, unique=True)
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(TagCategory, on_delete=models.PROTECT, related_name="tags", null=True, blank=True)

    def __str__(self):
        return f"{self.title}"

class Genre(models.Model):
    title = models.CharField(max_length=256, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title


