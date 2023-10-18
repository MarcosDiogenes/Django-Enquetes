from django.test import TestCase
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

import datetime

from .models import Pergunta

# testes models
class TestesModeloPergunta(TestCase):
    def teste_foi_publicado_recentemente_com_pergunta_futura(self):
        """
        foi_publicado_recentemente() retorna False para questões cuja data_pub for no futuro.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        pergunta_futura = Pergunta(data_pub=time)
        self.assertIs(pergunta_futura.foi_publicado_recentemente(), False)
 
    def teste_foi_publicado_recentemente_com_pergunta_antiga(self):
        """
        foi_publicado_recentemente() retorna False para questões cuja data_pub for há mais de um dia atrás.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        pergunta_antiga = Pergunta(data_pub=time)
        self.assertIs(pergunta_antiga.foi_publicado_recentemente(), False)

    def teste_foi_publicado_recentemente_com_pergunta_recente(self):
        """
        foi_publicado_recentemente() retorna False para questões cuja data_pub for nas últimas 24hs
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        pergunta_recente = Pergunta(data_pub=time)
        self.assertIs(pergunta_recente.foi_publicado_recentemente(), True)



# testes views
def criar_pergunta(texto_pergunta, days):
    """
    Create a question with the given `question_text` and published the given number of `days` offset to now (negative for questions published in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Pergunta.objects.create(texto_pergunta=texto_pergunta, data_pub=time)


class TestesViewIndexPergunta(TestCase):
    def teste_sem_perguntas(self):
        """
        If no questions exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse("enquetes:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Não há enquetes disponíveis")
        self.assertQuerySetEqual(response.context["lista_perguntas_recentes"], [])

    def teste_pergunta_anterior(self):
        """
        Perguntas com a data_pub no passado são exibidas na página index.
        """
        pergunta = criar_pergunta(texto_pergunta="Pergunta anterior.", days=-30)
        response = self.client.get(reverse("enquetes:index"))
        self.assertQuerySetEqual(
        response.context["lista_perguntas_recentes"],
        [pergunta],
        )

    def teste_pergunta_futura(self):
        """
        Perguntas com data_pub no futuro não são exibidas na página de index.
        """
        criar_pergunta(texto_pergunta="Pergunta Futura.", days=30)
        response = self.client.get(reverse("enquetes:index"))
        self.assertContains(response, "Não há enquetes disponíveis.")
        self.assertQuerySetEqual(response.context["lista_perguntas_recentes"], [])

    def teste_pergunta_futura_e_pergunta_anterior(self):
        """
        Mesmo que existam perguntas anteriores e futuras, apenas as perguntas anteriores serão exibidas.
        """
        pergunta = criar_pergunta(texto_pergunta="Pergunta anterior.", days=-30)
        criar_pergunta(texto_pergunta="Pergunta futura.", days=30)
        response = self.client.get(reverse("enquetes:index"))
        self.assertQuerySetEqual(
            response.context["lista_perguntas_recentes"],
            [pergunta],
        )

    def teste_duas_perguntas_anteriores(self):
        """
        A página de índice de perguntas pode exibir diversas perguntas.
        """
        pergunta1 = criar_pergunta(texto_pergunta="Pergunta anterior 1.", days=-30)
        pergunta2 = criar_pergunta(texto_pergunta="Pergunta anterior 2.", days=-5)
        response = self.client.get(reverse("enquetes:index"))
        self.assertQuerySetEqual(
            response.context["lista_perguntas_recentes"],
            [pergunta2, pergunta1],
        )

class TestesDetailViewPergunta(TestCase):
    def teste_pergunta_futura(self):
        """
        O view Detalhe de uma pergunta com data_pub no futuro retorna um erro 404.
        """
        pergunta_futura = criar_pergunta(texto_pergunta="Pergunta futura.", days=5)
        url = reverse("enquetes:detalhe", args=(pergunta_futura.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def teste_pergunta_passada(self):
        """
        O view Detalhe de uma pergunta com data_pub no passado retorna um erro 404.
        """
        pergunta_passada = criar_pergunta(texto_pergunta="Pergunta passada.", days=-5)
        url = reverse("enquetes:detalhe", args=(pergunta_passada.id,))
        response = self.client.get(url)
        self.assertContains(response, pergunta_passada.texto_pergunta)