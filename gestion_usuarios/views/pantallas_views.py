from django.http.response import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
import re
from ..models import *
from django.views.decorators.http import require_http_methods

@method_decorator(require_http_methods(['POST','PUT','GET','DELETE']), name='dispatch')
class PantallasView(View):
    #Este metodo permite realizar las conultas que necesitan autentificacion. POST PUT DELETE
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    #Busquedas personalizadas y por defecto
    #las personalizadas varian segun el criterio ingresado, y por defecto muestra todos los objetos
    def get(self, request, campo="",criterio=""):
        if (len(campo)> 0 and len(criterio)> 0):
            if criterio == "id":
                pantallas = list(Pantallas.objects.filter(id=campo).values())
                if len(pantallas) > 0:
                    pantallas = pantallas
                    pantallas = {'message': "Consulta exitosa", 'pantallas': pantallas}
                else:
                    pantallas = {'message': "No se encontraron los datos", 'pantallas': []} 
                    return JsonResponse(pantallas)
            elif criterio == "nombre":
                pantallas = list(Pantallas.objects.filter(nombre=campo).values())
                if len(pantallas) > 0:
                    pantallas = pantallas
                    pantallas = {'message': "Consulta exitosa", 'pantallas': pantallas}
                else:
                    pantallas = {'message': "No se encontraron los datos", 'pantallas': []} 
                    return JsonResponse(pantallas)
        else:
            pantallas = list(Pantallas.objects.values())
            if len(pantallas) > 0:
                pantallas = {'message': "Consulta exitosa", 'pantallas': pantallas}
            else:
                pantallas = {'message': "No se encontraron los datos", 'pantallas': []} 
        return JsonResponse(pantallas)

#Agregar un registro de cargos
    def post(self, request):
        jd=json.loads(request.body)
        if len(jd['nombre']) <= 0:
            pantallas = {'message': "El nombre esta vacío."}
        elif (validar_pantalla_repetida(jd['nombre'])):
            pantallas = {'message': "El nombre ya esta en uso."}
        elif len(jd['nombre']) < 3:
            pantallas = {'message': "El nombre debe tener mas de 3 caracteres."}
        elif not validar_cadena_espacios(jd['nombre']):
            pantallas = {'message': "No se permiten mas de un espacio consecutivo.[nombre]"}
        elif validar_cadena_repeticion(jd['nombre']):
            pantallas = {'message': "No se permiten mas de dos caracteres consecutivos del mismo tipo.[nombre]"}
        elif len(jd['nombre']) > 50:
            pantallas = {'message': "El nombre debe tener menos de 50 caracteres."}
        elif len(jd['descripcion']) <= 0:
            pantallas = {'message': "La descripción esta vacía."}
        elif len(jd['descripcion']) < 4:
            pantallas = {'message': "La descripción debe tener mas de 4 caracteres."}
        elif not validar_cadena_espacios(jd['descripcion']):
            pantallas = {'message': "No se permiten mas de un espacio consecutivo.[descripcion]"}
        elif validar_cadena_repeticion(jd['descripcion']):
            pantallas = {'message': "No se permiten mas de dos caracteres consecutivos del mismo tipo.[descripcion]"}
        elif len(jd['descripcion']) > 50:
            pantallas = {'message': "La descripción debe tener menos de 50 caracteres."}
        else:
            Pantallas.objects.create(nombre=jd['nombre'], descripcion=jd['descripcion'])
            pantallas = {'message':"Registro Exitoso."}
        return JsonResponse(pantallas)

#Actualizar un registro de cargos
    def put(self, request,id):
        jd=json.loads(request.body)
        pantallas = list(Pantallas.objects.filter(id=id).values())
        if len(pantallas) > 0:
            pantallas_actualizar=Pantallas.objects.get(id=id)
            if len(jd['nombre']) <= 0:
                pantallas = {'message': "El nombre esta vacío."}
            elif len(jd['nombre']) < 3:
                pantallas = {'message': "El nombre debe tener mas de 3 caracteres."}
            elif not validar_cadena_espacios(jd['nombre']):
                pantallas = {'message': "No se permiten mas de un espacio consecutivo.[nombre]"}
            elif validar_cadena_repeticion(jd['nombre']):
                pantallas = {'message': "No se permiten mas de dos caracteres consecutivos del mismo tipo.[nombre]"}
            elif len(jd['nombre']) > 50:
                pantallas = {'message': "El nombre debe tener menos de 50 caracteres."}
            elif len(jd['descripcion']) <= 0:
                pantallas = {'message': "La descripción esta vacía."}
            elif len(jd['descripcion']) < 4:
                pantallas = {'message': "La descripción debe tener mas de 4 caracteres."}
            elif not validar_cadena_espacios(jd['descripcion']):
                pantallas = {'message': "No se permiten mas de un espacio consecutivo.[descripcion]"}
            elif validar_cadena_repeticion(jd['descripcion']):
                pantallas = {'message': "No se permiten mas de dos caracteres consecutivos del mismo tipo.[descripcion]"}
            elif len(jd['descripcion']) > 50:
                pantallas = {'message': "La descripción debe tener menos de 50 caracteres."}
            else:
                pantallas_actualizar.nombre = jd['nombre']
                pantallas_actualizar.descripcion = jd['descripcion']
                pantallas_actualizar.save()

                pantallas = {'message': "La actualización fue exitosa."}
        return JsonResponse(pantallas)
        
        
#Eliminar un registro de cargos
    def delete(self, request,id):
        pantallas = list(Pantallas.objects.filter(id=id).values())
        if len(pantallas) > 0:
            Pantallas.objects.filter(id=id).delete()
            datos = {'message':"Registro Eliminado"}
        else:
            datos = {'message':"No se encontraró el registro", 'pantallas': []}
        return JsonResponse(datos)
    
def validar_pantalla_repetida(nombre): 
    if (nombre):
        registros = Pantallas.objects.filter(nombre=nombre)
        if len(registros) > 0:
            return True
        else:
            return False
    return False

def validar_cadena_repeticion(cadena):
    patron = r'([a-zA-Z])\1\1'
    return bool(re.search(patron, cadena))

def validar_cadena_espacios(cadena):
    patron = r'^[^ ]+(?: {0,1}[^ ]+)*$'
    return bool(re.match(patron,cadena))
