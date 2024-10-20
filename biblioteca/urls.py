from django.urls import path
from .import views


urlpatterns = [
    path('',views.index,name='index'),
    path('libros/listar', views.listar_libros, name= 'lista_libros'),
    
    #<int:id_libro>: el segundo parametro se puede llamar como quiera
    path('libros/<int:id_libro>/', views.dame_libro, name='dame_libro'),
    path('libros/listar/<int:anyo_libro>/<int:mes_libro>', views.dame_libros_fecha, name='dame_libros_fecha'),
    path('libros/listar/<str:idioma>/', views.dame_libros_idioma, name= 'dame_libros_idioma'),  
    path('biblioteca/<int:id_biblioteca>/libros/<str:texto_libro>', views.dame_libros_biblioteca, name= 'dame_libros_biblioteca'),
    path('ultimo-cliente-libro/<int:libro>', views.dame_ultimo_cliente_libro, name= 'ultimo_cliente_libro'),

]




