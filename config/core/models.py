from django.db import models

class Signatory(models.Model):
    name = models.CharField(max_length=100)
    initials = models.CharField(max_length=100)
    
    def __str__(self) -> str:
        return self.name
    
class Element(models.Model):
    code = models.CharField(max_length=50)
    radioactive = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.code
    
class LabelTemplate(models.Model):
    def __str__(self) -> str:
        return super().__str__()