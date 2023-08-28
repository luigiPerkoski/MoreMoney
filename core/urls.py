from django.urls import path
from . import views
 
urlpatterns = [
    path('',views.index, name = 'index'),
    path('accounts', views.accounts, name = 'accounts'),
    path('dameges', views.damege, name = 'damage'),
    path('profits', views.profit, name = 'profit'),
    path('formulario/<id>', views.processar_formulario, name = 'processar_formulario'),
]
