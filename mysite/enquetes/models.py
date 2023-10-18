from django.db import models
from django.utils import timezone
from django.contrib import admin


import datetime

class Pergunta(models.Model):
    texto_pergunta = models.CharField(max_length=200)
    data_pub = models.DateTimeField("data publicada")

    def __str__(self):
        return self.texto_pergunta
    
    @admin.display(
        boolean=True,
        ordering="data_pub",
        description="Publicado recentemente?",
    )

    def foi_publicado_recentemente(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.data_pub <= now


class Escolha(models.Model):
    question = models.ForeignKey(Pergunta, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text