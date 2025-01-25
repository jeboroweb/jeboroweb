from django.views.generic.base import TemplateView
from django.shortcuts import render


class HomePageView(TemplateView):
    template_name = "core/home.html"
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context["titulo"] = "jEbOro pErsOnal WEB "
    #     return context
    def get(self, request, *args, **kwargs):
        return render(request,self.template_name,{"titulo":"jEbOro pErsOnal Web"})

class CalendarioPageView(TemplateView):
    template_name ="calendario/calendario.html"

class SamplePageView(TemplateView):
    template_name = "core/sample.html"    