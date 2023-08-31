from django.urls import path
from . import views
 
urlpatterns = [
    path('',views.index, name = 'index'),
    path('accounts', views.accounts, name = 'accounts'),
    path('dameges', views.damege, name = 'damage'),
    path('profits', views.profit, name = 'profit'),
    path('formulario/<id>', views.processar_formulario, name = 'processar_formulario'),
    path('new_extract', views.new_extract, name='new_extract'),
    path('extract_forms', views.extract_forms, name='extract_forms'),

]
