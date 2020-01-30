from django.urls import path
from .views import \
    LoginView, logout_user, \
    AgentView, EvaluatorView, \
    STLView, TLTaskView, EvaluationView, \
    STLReview, AgentTaskView, stl_calc, \
    AgentDetailView, EvaluatorDetailView, \
    STLDetailView

app_name = 'owners'
urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('agent_view/', AgentView.as_view(), name='agent_view'),
    path('agent_detail_view/<int:pk>/', AgentDetailView.as_view(), name='agent_detail_view'),
    path('agent_task_view/', AgentTaskView.as_view(), name='agent_task_view'),
    path('evaluator_view/', EvaluatorView.as_view(), name='evaluator_view'),
    path('evaluation_view/<int:pk>/<int:task_id>', EvaluationView.as_view(), name='evaluation_view'),
    path('evaluator_detail_view/<int:id>/', EvaluatorDetailView.as_view(), name='evaluator_detail_view'),
    path('stl_view/', STLView.as_view(), name='stl_view'),
    path('stl_review/<int:pk>/<int:task_id>/<int:order_id>', STLReview.as_view(), name='stl_review'),
    path('stl_calc/', stl_calc, name='stl_calc'),
    path('stl_detail_view/<int:pk>/', STLDetailView.as_view(), name='stl_detail_view'),
    path('tl_task_view/', TLTaskView.as_view(), name='tl_task_view'),
]
