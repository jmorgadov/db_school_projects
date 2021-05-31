from typing import Any, Dict
from pages.models import simulate_battle_iter
from pages.views import BaseView
from django.http.request import HttpRequest


# Create your views here.


LOGS = []


class SimulateBattleView(BaseView):

    template_name = 'simulate_battle.html'

    def get(self, request: HttpRequest, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def post(self, request: HttpRequest, *args, **kwargs):
        global LOGS
        post = request.POST
        if 'simulate' in post:
            LOGS = []
            for log in simulate_battle_iter():
                print(log)
                LOGS.append(log)

        return super().post(request, *args, **kwargs)

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['logs'] = LOGS
        return super().get_context_data(**context)
