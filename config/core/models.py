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
    
class Component(models.Model):
    name = models.CharField(max_length=255)
    # Default value source
    tied_model = models.CharField(
        max_length=50,
        choices=[
            ("element", "Element"),
            ("signatory", "Signatory"),
            # Add more as needed
        ],
        blank=True,
        null=True
    )
    tied_field = models.CharField(max_length=50, blank=True, null=True)
    
    # Add width (in characters) — editable in builder
    width_chars = models.PositiveIntegerField(default=20, help_text="Max characters allowed")

    def __str__(self):
        return self.name
    
class LabelTemplate(models.Model):
    name = models.CharField(max_length=100)

    # Reference components; if a component is deleted, delete template-component link
    components = models.ManyToManyField(
        Component,
        through="TemplateComponent",
        related_name="templates"
    )


    def __str__(self) -> str:
        return super().__str__()
    
class TemplateComponent(models.Model):
    template = models.ForeignKey(LabelTemplate, on_delete=models.CASCADE)
    component = models.ForeignKey(Component, on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]
        unique_together = ["template", "component"]

    def __str__(self):
        return f"{self.template.name} → {self.component.name}"
    

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