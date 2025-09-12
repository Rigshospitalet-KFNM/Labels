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
    batchnr = models.PositiveIntegerField(
        default=0
    ) ##should reset daily

    def __str__(self) -> str:
        return self.symbol
    
class Component(models.Model):
    PROTECTED_TYPES = ["DATE", "BATCHNR", "TEXT"]
    protected = models.BooleanField(default=False) 
    
    TEXT = "TEXT"
    MODEL_FIELD = "MODEL_FIELD"
    BATCHNR = "BATCHNR"
    DATE = "DATE"

 
    COMPONENT_TYPES = [
        (TEXT, "Free text field"),
        (MODEL_FIELD, "Tied to model field"),
        (BATCHNR, "Batch number"),
        (DATE, "Date field"),
    ]
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=20, choices=COMPONENT_TYPES, default=TEXT)

    # For MODEL_FIELD type
    tied_model = models.CharField(
        max_length=50,
        choices=[("element", "Element"), ("signatory", "Signatory")],
        blank=True, null=True
    )
    tied_field = models.CharField(max_length=100, blank=True, null=True)

    # Optional static prefix/suffix/info text
    info_text = models.CharField(max_length=200, blank=True, null=True)

    # Layout control
    width_chars = models.PositiveIntegerField(default=20)

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