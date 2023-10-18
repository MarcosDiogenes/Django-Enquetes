from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Escolha, Pergunta

# Create your views here.

class IndexView(generic.ListView):
    template_name = "enquetes/index.html"
    context_object_name = "lista_perguntas_recentes"

    def get_queryset(self):

        """
        Return the last five published questions (not including those set to be published in the future).
        """

        return Pergunta.objects.filter(data_pub__lte=timezone.now()).order_by("-data_pub")[:5]


class DetailView(generic.DetailView):

    model = Pergunta
    template_name = "enquetes/detalhe.html"

    def get_queryset(self):
        """
        Exclui quaisquer perguntas que não foram publicadas ainda.
        """
        return Pergunta.objects.filter(data_pub__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Pergunta
    template_name = "enquetes/resultado.html"


def voto(request, pergunta_id):
    pergunta = get_object_or_404(Pergunta, pk=pergunta_id)
    try:
        escolha_selecionada = pergunta.escolha_set.get(pk=request.POST["escolha"])
    except (KeyError, Escolha.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "enquetes/detalhe.html",
            {
                "pergunta": pergunta,
                "error_message": "Você não escolheu uma resposta.",
            },
        )
    else:
        escolha_selecionada.votes += 1
        escolha_selecionada.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("enquetes:resultado", args=(pergunta.id,)))