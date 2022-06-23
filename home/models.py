from django.db import models


# this models holds the animated text on the homepage
class AnimatedText(models.Model):
    line1 = models.CharField(max_length=150, blank=False) 
    line2 = models.CharField(max_length=150, blank=False) 

    def __str__(self) -> str:
        return self.line1
