from django.db import models

# Create your models here.
class Scholarship_Type(models.Model):
    scholarname = models.CharField(max_length=45)
    scholardescr = models.TextField(null=True)
    
    def __str__(self) -> str:
        return self.scholarname