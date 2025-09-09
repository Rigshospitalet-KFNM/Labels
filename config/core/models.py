from django.db import models
from django.forms import ValidationError

class Signatory(models.Model):
    name = models.CharField(max_length=100)
    initials = models.CharField(max_length=100)
    
    def __str__(self) -> str:
        return self.name
    
class Element(models.Model):
    symbol = models.CharField(max_length=50)
    radioactive = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.symbol
    
class LabelTemplate(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self) -> str:
        return super().__str__()
    

class LabelSettings(models.Model):
    width = models.FloatField(default=63.5,help_text="Label width in mm")
    height = models.FloatField(default=33.9,help_text="Label height in mm")


    def save(self, *args, **kwargs):
        if not self.pk and LabelSettings.objects.exists():
            raise ValidationError("Only one LabelSettings instance is allowed.")
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.width} x {self.height} mm"
    
    @classmethod
    def get_solo(cls):
        """Always return the one settings instance, create it if missing"""
        obj, created = cls.objects.get_or_create(pk=1)
        return obj