from django.http.response import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
import re
from ..models import *
from django.views.decorators.http import require_http_methods

@method_decorator(require_http_methods(['POST','PUT','GET','DELETE']), name='dispatch')
class SintomasView(View):
    #Este metodo permite realizar las conultas que necesitan autentificacion. POST PUT DELETE
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    #Busquedas personalizadas y por defecto
    #las personalizadas varian segun el criterio ingresado, y por defecto muestra todos los objetos
    def get(self, request, campo="",criterio=""):
        if (len(campo)> 0 and len(criterio)> 0):
            if criterio == "id":
                sintomas = list(Sintoma.objects.filter(id=campo).values())
                if len(sintomas) > 0:
                    sintomas = sintomas
                    sintomas = {'message': "Consulta exitosa", 'sintomas': sintomas}
                else:
                    sintomas = {'message': "No se encontraron los datos", 'sintomas': []} 
                    return JsonResponse(sintomas)
            elif criterio == "nombre":
                sintomas = list(Sintoma.objects.filter(nombre=campo).values())
                if len(sintomas) > 0:
                    sintomas = sintomas
                    sintomas = {'message': "Consulta exitosa", 'sintomas': sintomas}
                else:
                    sintomas = {'message': "No se encontraron los datos", 'sintomas': []} 
                    return JsonResponse(sintomas)
        else:
            sintomas = list(Sintoma.objects.values())
            if len(sintomas) > 0:
                sintomas = {'message': "Consulta exitosa", 'sintomas': sintomas}
            else:
                sintomas = {'message': "No se encontraron los datos", 'sintomas': []} 
        return JsonResponse(sintomas)

#Agregar un registro de cargos
    def post(self, request):
        jd=json.loads(request.body)
        if len(jd['nombre']) <= 0:
            sintomas = {'message': "El nombre esta vacío."}
        elif (validar_sintoma_repetido(jd['nombre'])):
            sintomas = {'message': "El nombre ya esta en uso."}
        elif len(jd['nombre']) < 3:
            sintomas = {'message': "El nombre debe tener mas de 3 caracteres."}
        elif not validar_cadena_espacios(jd['nombre']):
            sintomas = {'message': "No se permiten mas de un espacio consecutivo.[nombre]"}
        elif validar_cadena_repeticion(jd['nombre']):
            sintomas = {'message': "No se permiten mas de dos caracteres consecutivos del mismo tipo.[nombre]"}
        elif len(jd['nombre']) > 50:
            sintomas = {'message': "El nombre debe tener menos de 50 caracteres."}
        elif len(jd['descripcion']) <= 0:
            sintomas = {'message': "La descripción esta vacía."}
        elif len(jd['descripcion']) < 4:
            sintomas = {'message': "La descripción debe tener mas de 4 caracteres."}
        elif not validar_cadena_espacios(jd['descripcion']):
            sintomas = {'message': "No se permiten mas de un espacio consecutivo.[descripcion]"}
        elif validar_cadena_repeticion(jd['descripcion']):
            sintomas = {'message': "No se permiten mas de dos caracteres consecutivos del mismo tipo.[descripcion]"}
        elif len(jd['descripcion']) > 50:
            sintomas = {'message': "La descripción debe tener menos de 50 caracteres."}
        else:
            Sintoma.objects.create(nombre=jd['nombre'], descripcion=jd['descripcion'])
            sintomas = {'message':"Registro Exitoso."}
        return JsonResponse(sintomas)

#Actualizar un registro de cargos
    def put(self, request,id):
        jd=json.loads(request.body)
        sintomas = list(Sintoma.objects.filter(id=id).values())
        if len(sintomas) > 0:
            sintomas_actualizar=Sintoma.objects.get(id=id)
            if len(jd['nombre']) <= 0:
                sintomas = {'message': "El nombre esta vacío."}
            elif len(jd['nombre']) < 3:
                sintomas = {'message': "El nombre debe tener mas de 3 caracteres."}
            elif not validar_cadena_espacios(jd['nombre']):
                sintomas = {'message': "No se permiten mas de un espacio consecutivo.[nombre]"}
            elif validar_cadena_repeticion(jd['nombre']):
                sintomas = {'message': "No se permiten mas de dos caracteres consecutivos del mismo tipo.[nombre]"}
            elif len(jd['nombre']) > 50:
                sintomas = {'message': "El nombre debe tener menos de 50 caracteres."}
            elif len(jd['descripcion']) <= 0:
                sintomas = {'message': "La descripción esta vacía."}
            elif len(jd['descripcion']) < 4:
                sintomas = {'message': "La descripción debe tener mas de 4 caracteres."}
            elif not validar_cadena_espacios(jd['descripcion']):
                sintomas = {'message': "No se permiten mas de un espacio consecutivo.[descripcion]"}
            elif validar_cadena_repeticion(jd['descripcion']):
                sintomas = {'message': "No se permiten mas de dos caracteres consecutivos del mismo tipo.[descripcion]"}
            elif len(jd['descripcion']) > 50:
                sintomas = {'message': "La descripción debe tener menos de 50 caracteres."}
            else:
                sintomas_actualizar.nombre = jd['nombre']
                sintomas_actualizar.descripcion = jd['descripcion']
                sintomas_actualizar.save()

                sintomas = {'message': "La actualización fue exitosa."}
        return JsonResponse(sintomas)
        
        
#Eliminar un registro de cargos
    def delete(self, request,id):
        sintomas = list(Sintoma.objects.filter(id=id).values())
        if len(sintomas) > 0:
            Sintoma.objects.filter(id=id).delete()
            datos = {'message':"Registro Eliminado"}
        else:
            datos = {'message':"No se encontraró el registro", 'sintomas': []}
        return JsonResponse(datos)
    
def validar_sintoma_repetido(nombre): 
    if (nombre):
        registros = Sintoma.objects.filter(nombre=nombre)
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
