from django.contrib import admin

from .models import Escolha, Pergunta

class EscolhaNaLinha(admin.TabularInline):
    model = Escolha
    extra = 3

class PerguntaAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["texto_pergunta"]}),
        ("Informações de data", {"fields": ["data_pub"]}),
    ]
    inlines = [EscolhaNaLinha]
    list_display = ["texto_pergunta", "data_pub", "foi_publicado_recentemente"]
    list_filter = ["data_pub"]
    search_fields = ["texto_pergunta"]




admin.site.register(Pergunta, PerguntaAdmin)