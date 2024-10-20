from django.shortcuts import render
from .models import Libro, Cliente
from django.db.models import Q #Q te permite crear consultas que usen operadores lógicos (AND, OR, NOT) de una manera más flexible y legible.

# Create your views here.
def index(request):
    return render(request, 'index.html')

#Una url que me muestre todos los libros y sus datos, incluido los relacionados
def listar_libros(request):
    libros= Libro.objects.select_related('biblioteca').prefetch_related('autores')
    libros= libros.all()
    return render(request, 'libro/lista.html', {'lista_libros':libros})

#Una url que me muestre información sobre cada libro
#los parametros despues del request hacen referencia a lo que aparece en el navegador
def dame_libro(request, id_libro):
    libros= Libro.objects.select_related('biblioteca').prefetch_related('autores').get(id=id_libro) #id hace referencia al campo id de tu tabla
    return render(request, 'libro/libros.html', {'libro_mostrar':libros})


#Una url que me muestre los libros de un año y mes concreto
def dame_libros_fecha(request, anyo_libro, mes_libro):
    libros= Libro.objects.select_related('biblioteca').prefetch_related('autores')
    
    """
    Aplicamos el método filter: qué sirve para filtrar por un campo en la base de datos, como un WHERE en Mysql, y podemos usar “,” para hacer AND.
    para acceder al campo año y mes de un campo de tipo fecha, debemos usar DOS BARRAS BAJAS: __. Esto sería como usar las funciones YEAR y MONTH de SQL
    """
    libros= libros.filter(fecha_publicacion__year=anyo_libro,fecha_publicacion__month=mes_libro)
    return render(request, 'libro/lista.html',{'libro_mostrar':libros})

#Una url que me muestre los libros que tienen el idioma del libro o español ordenados por fecha 
# de publicación
def dame_libros_idioma(request, idioma):
    libros= Libro.objects.select_related('biblioteca').prefetch_related('autores')
    libros= libros.filter(Q(tipo=idioma) | Q(tipo='ES')).order_by('fecha_publicacion')
    return render(request, 'libro/lista.html', {'libro_mostrar':libros})


##Una url que me muestre los libros de una biblioteca que contenga un texto en concreto.
def dame_libros_biblioteca(request, id_biblioteca, texto_libro):
    libros= Libro.objects.select_related('biblioteca').prefetch_related('autores')
    libros= libros.filter(id=id_biblioteca).filter(descripcion__contains=texto_libro).order_by("-nombre") #el menos indica en orden descendente
    return render(request, 'libro/lista.html', {'libro_mostrar':libros})

#Una url que me muestre el último cliente que se llevó un libro en concreto:
"""
En este caso usamos una tabla intermedia(prestamo), de una relación ManytoMany, para saber qué clientes sacaron esos libros
[:1] Significa que queremos obtener sólo un registro. Si pusiéramos [:5], obtendremos 5 registros, y si pusieramos [3:6] obtendremos del registro 3 al 6.(Esto son los LIMIT y OFFSET de MYSQL)
get(): A la hora de usar las QuerySet, siempre nos devuelve un conjunto de registros, en este caso sólo queremos uno, por lo tanto esta función nos devolvera el registro en sí, en vez de un conjunto.

"""
def dame_ultimo_cliente_libro(request, libro):
    cliente= Cliente.objects.filter(id= libro).order_by("-prestamo__fecha_prestamo")[:1].get()
    return render(request, 'cliente/cliente.html', {"cliente":cliente})