from django.http.response import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
import re
from ..models import *
from django.views.decorators.http import require_http_methods

@method_decorator(require_http_methods(['POST','PUT','GET','DELETE']), name='dispatch')
class AccionesView(View):
    #Este metodo permite realizar las conultas que necesitan autentificacion. POST PUT DELETE
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    #Busquedas personalizadas y por defecto
    #las personalizadas varian segun el criterio ingresado, y por defecto muestra todos los objetos
    def get(self, request, campo="",criterio=""):
        if (len(campo)> 0 and len(criterio)> 0):
            if criterio == "id":
                acciones = list(Acciones.objects.filter(id=campo).values())
                if len(acciones) > 0:
                    acciones = acciones
                    acciones = {'message': "Consulta exitosa", 'acciones': acciones}
                else:
                    acciones = {'message': "No se encontraron los datos", 'acciones': []} 
                    return JsonResponse(acciones)
            elif criterio == "nombre":
                acciones = list(Acciones.objects.filter(nombre=campo).values())
                if len(acciones) > 0:
                    acciones = acciones
                    acciones = {'message': "Consulta exitosa", 'acciones': acciones}
                else:
                    acciones = {'message': "No se encontraron los datos", 'acciones': []} 
                    return JsonResponse(acciones)
        else:
            acciones = list(Acciones.objects.values())
            if len(acciones) > 0:
                acciones = {'message': "Consulta exitosa", 'acciones': acciones}
            else:
                acciones = {'message': "No se encontraron los datos", 'acciones': []} 
        return JsonResponse(acciones)

#Agregar un registro de cargos
    def post(self, request):
        jd=json.loads(request.body)
        if len(jd['nombre']) <= 0:
            acciones = {'message': "El nombre esta vacío."}
        elif (validar_acciones_repetidas(jd['nombre'])):
            acciones = {'message': "El nombre ya esta en uso."}
        elif len(jd['nombre']) < 3:
            acciones = {'message': "El nombre debe tener mas de 3 caracteres."}
        elif not validar_cadena_espacios(jd['nombre']):
            acciones = {'message': "No se permiten mas de un espacio consecutivo.[nombre]"}
        elif validar_cadena_repeticion(jd['nombre']):
            acciones = {'message': "No se permiten mas de dos caracteres consecutivos del mismo tipo.[nombre]"}
        elif len(jd['nombre']) > 50:
            acciones = {'message': "El nombre debe tener menos de 50 caracteres."}
        elif len(jd['descripcion']) <= 0:
            acciones = {'message': "La descripción esta vacía."}
        elif len(jd['descripcion']) < 4:
            acciones = {'message': "La descripción debe tener mas de 4 caracteres."}
        elif not validar_cadena_espacios(jd['descripcion']):
            acciones = {'message': "No se permiten mas de un espacio consecutivo.[descripcion]"}
        elif validar_cadena_repeticion(jd['descripcion']):
            acciones = {'message': "No se permiten mas de dos caracteres consecutivos del mismo tipo.[descripcion]"}
        elif len(jd['descripcion']) > 50:
            acciones = {'message': "La descripción debe tener menos de 50 caracteres."}
        else:
            Acciones.objects.create(nombre=jd['nombre'], descripcion=jd['descripcion'])
            acciones = {'message':"Registro Exitoso."}
        return JsonResponse(acciones)

#Actualizar un registro de cargos
    def put(self, request,id):
        jd=json.loads(request.body)
        acciones = list(Acciones.objects.filter(id=id).values())
        if len(acciones) > 0:
            acciones_actualizar=Acciones.objects.get(id=id)
            if len(jd['nombre']) <= 0:
                acciones = {'message': "El nombre esta vacío."}
            elif len(jd['nombre']) < 3:
                acciones = {'message': "El nombre debe tener mas de 3 caracteres."}
            elif not validar_cadena_espacios(jd['nombre']):
                acciones = {'message': "No se permiten mas de un espacio consecutivo.[nombre]"}
            elif validar_cadena_repeticion(jd['nombre']):
                acciones = {'message': "No se permiten mas de dos caracteres consecutivos del mismo tipo.[nombre]"}
            elif len(jd['nombre']) > 50:
                acciones = {'message': "El nombre debe tener menos de 50 caracteres."}
            elif len(jd['descripcion']) <= 0:
                acciones = {'message': "La descripción esta vacía."}
            elif len(jd['descripcion']) < 4:
                acciones = {'message': "La descripción debe tener mas de 4 caracteres."}
            elif not validar_cadena_espacios(jd['descripcion']):
                acciones = {'message': "No se permiten mas de un espacio consecutivo.[descripcion]"}
            elif validar_cadena_repeticion(jd['descripcion']):
                acciones = {'message': "No se permiten mas de dos caracteres consecutivos del mismo tipo.[descripcion]"}
            elif len(jd['descripcion']) > 50:
                acciones = {'message': "La descripción debe tener menos de 50 caracteres."}
            else:
                acciones_actualizar.nombre = jd['nombre']
                acciones_actualizar.descripcion = jd['descripcion']
                acciones_actualizar.save()

                acciones = {'message': "La actualización fue exitosa."}
        return JsonResponse(acciones)
        
        
#Eliminar un registro de cargos
    def delete(self, request,id):
        acciones = list(Acciones.objects.filter(id=id).values())
        if len(acciones) > 0:
            Acciones.objects.filter(id=id).delete()
            datos = {'message':"Registro Eliminado"}
        else:
            datos = {'message':"No se encontraró el registro", 'acciones': []}
        return JsonResponse(datos)
    
def validar_acciones_repetidas(nombre): 
    if (nombre):
        registros = Acciones.objects.filter(nombre=nombre)
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
