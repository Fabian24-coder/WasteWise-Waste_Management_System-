from django.db import models
from django.core.validators import MinValueValidator


class RubbishDetail(models.Model):
    CATEGORY_CHOICES = [
        ('organic', 'Organic'),
        ('plastic', 'Plastic'),
        ('paper', 'Paper'),
        ('glass', 'Glass'),
        ('metal', 'Metal'),
        ('ewaste', 'E-waste'),
        ('hazardous', 'Hazardous'),
        ('construction', 'Construction'),
    ]
    UNIT_CHOICES = [('ton', 'Per ton'), ('kg', 'Per kg'), ('item', 'Per item'), ('bag', 'Per bag')]

    waste_id = models.AutoField(primary_key=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    name = models.CharField(max_length=100)
    rate = models.DecimalField(max_digits=10, decimal_places=2,
                               validators=[MinValueValidator(0)])
    unit = models.CharField(max_length=10, choices=UNIT_CHOICES, default='kg')
    weight = models.DecimalField(max_digits=8, decimal_places=2, null=True,
                                 blank=True, validators=[MinValueValidator(0)],
                                 help_text="Default/estimated weight")
    description = models.TextField(blank=True)
    is_hazardous = models.BooleanField(default=False)
    is_recyclable = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['category', 'name']
        verbose_name = 'Rubbish detail'

    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"
