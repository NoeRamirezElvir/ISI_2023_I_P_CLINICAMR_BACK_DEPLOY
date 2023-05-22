from django.http.response import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
import re
from ..models import *
from django.views.decorators.http import require_http_methods

@method_decorator(require_http_methods(['POST','PUT','GET','DELETE']), name='dispatch')
class subtipoView(View):
    #Este metodo permite realizar las conultas que necesitan autentificacion. POST PUT DELETE
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    #Busquedas personalizadas y por defecto
    #las personalizadas varian segun el criterio ingresado, y por defecto muestra todos los objetos
    def get(self, request, campo="",criterio=""):
        if (len(campo)> 0 and len(criterio)> 0):
            if criterio == "id":
                subtipo = list(Subtipo.objects.filter(id=campo).values())
                if len(subtipo) > 0:
                    subtipo = subtipo
                    subtipo = {'message': "Consulta exitosa", 'subtipo': subtipo}
                else:
                    subtipo = {'message': "No se encontraron los datos", 'subtipo': []} 
                    return JsonResponse(subtipo)
            elif criterio == "nombre":
                subtipo = list(Subtipo.objects.filter(nombre=campo).values())
                if len(subtipo) > 0:
                    subtipo = subtipo
                    subtipo = {'message': "Consulta exitosa", 'subtipo': subtipo}
                else:
                    subtipo = {'message': "No se encontraron los datos", 'subtipo': []} 
                    return JsonResponse(subtipo)
        else:
            subtipo = list(Subtipo.objects.values())
            if len(subtipo) > 0:
                subtipo = {'message': "Consulta exitosa", 'subtipo': subtipo}
            else:
                subtipo = {'message': "No se encontraron los datos", 'subtipo': []} 
        return JsonResponse(subtipo)

#Agregar un registro de subtipo
    def post(self, request):
        jd=json.loads(request.body)

        if len(jd['nombre']) <= 0:
            subtipo = {'message': "El nombre esta vacío."}
        elif (validar_subtipo_repetido(jd['nombre'])):
            subtipo = {'message': "El subtipos ya existe."}
        elif len(jd['nombre']) < 4:
            subtipo = {'message': "El nombre debe tener mas de 4 caracteres."}
        elif not validar_cadena_espacios(jd['nombre']):
            subtipo = {'message': "No se permiten mas de un espacio consecutivo."}
        elif validar_cadena_repeticion(jd['nombre']):
            subtipo = {'message': "No se permiten mas de dos caracteres consecutivos del mismo tipo."}
        elif len(jd['nombre']) > 50:
            subtipo = {'message': "El nombre debe tener menos de 50 caracteres."}
        elif jd['activo'] < 0:
            subtipo = {'message': "Activo debe ser positivo."}
        elif jd['activo'] > 1:
            subtipo = {'message': "Activo debe unicamente puede ser 0 o 1."}
        else:
            nombre_minuscula = (jd['nombre']).lower()
            Subtipo.objects.create(nombre=nombre_minuscula, activo=jd['activo'])
            subtipo = {'message':"Registro Exitoso."}
        return JsonResponse(subtipo)

#Actualizar un registro de subtipo
    def put(self, request,id):
        jd=json.loads(request.body)
        subtipo = list(Subtipo.objects.filter(id=id).values())
        if len(subtipo) > 0:
            subtipos=Subtipo.objects.get(id=id)
            if len(jd['nombre']) <= 0:
                subtipo = {'message': "El nombre esta vacío."}
            elif len(jd['nombre']) < 4:
                subtipo = {'message': "El nombre debe tener mas de 4 caracteres."}
            elif not validar_cadena_espacios(jd['nombre']):
                subtipo = {'message': "No se permiten mas de un espacio consecutivo."}
            elif validar_cadena_repeticion(jd['nombre']):
                subtipo = {'message': "No se permiten mas de dos caracteres consecutivos del mismo tipo."}
            elif len(jd['nombre']) > 50:
                subtipo = {'message': "El nombre debe tener menos de 50 caracteres."}
            elif jd['activo'] < 0:
                subtipo = {'message': "Activo debe ser positivo."}
            elif jd['activo'] < 0:
                subtipo = {'message': "Activo debe unicamente puede ser 0 o 1."}
            else:
                subtipo = {'message': "Registro Exitoso."}
                subtipos.nombre = (jd['nombre']).lower()
                subtipos.activo = jd['activo']
                subtipos.save()
                subtipo = {'message': "La actualización fue exitosa."}
        return JsonResponse(subtipo)
        
        
#Eliminar un registro de subtipo
    def delete(self, request,id):
        subtipo = list(Subtipo.objects.filter(id=id).values())
        if len(subtipo) > 0:
            Subtipo.objects.filter(id=id).delete()
            datos = {'message':"Registro Eliminado"}
        else:
            datos = {'message':"No se encontraró el registro", 'subtipo': []}
        return JsonResponse(datos)
    
def validar_subtipo_repetido(nombre): 
    if (nombre):
        registros = Subtipo.objects.filter(nombre=nombre)
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
