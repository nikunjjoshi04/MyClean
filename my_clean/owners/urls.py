from django.urls import path
from .views import \
    LoginView, logout_user, \
    AgentView, EvaluatorView, \
    STLView, TLView, EvaluationView

app_name = 'owners'
urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('agent_view/', AgentView.as_view(), name='agent_view'),
    path('evaluator_view/', EvaluatorView.as_view(), name='evaluator_view'),
    path('evaluation_view/<int:pk>/<int:task_id>', EvaluationView.as_view(), name='evaluation_view'),
    path('stl_view/', STLView.as_view(), name='stl_view'),
    path('tl_view/', TLView.as_view(), name='tl_view'),
]
