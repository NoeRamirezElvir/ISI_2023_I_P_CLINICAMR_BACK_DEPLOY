from django.http.response import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
import re
from ..models import *
from django.views.decorators.http import require_http_methods

@method_decorator(require_http_methods(['POST','PUT','GET','DELETE']), name='dispatch')
class EspecialidadViews(View):
    #Este metodo permite realizar las conultas que necesitan autentificacion. POST PUT DELETE
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    #Busquedas personalizadas y por defecto
    #las personalizadas varian segun el criterio ingresado, y por defecto muestra todos los objetos
    def get(self, request, campo="",criterio=""):
        if (len(campo)> 0 and len(criterio)> 0):
            if(criterio=="id"):
                especialidad = list(EspecialidadMedico.objects.filter(id=campo).values())
                if len(especialidad) > 0:
                    especialidad = especialidad
                    especialidad = {'message': "Consulta exitosa", 'especialidad': especialidad}
                else:
                    especialidad = {'message': "No se encontraron los datos", 'especialidad':[]} 
                    return JsonResponse(especialidad)
            elif(criterio=="nombre"):
                especialidad = list(EspecialidadMedico.objects.filter(nombre=campo).values())
                if len(especialidad) > 0:
                    especialidad = especialidad
                    especialidad = {'message': "Consulta exitosa", 'especialidad': especialidad}
                else:
                    especialidad = {'message': "No se encontraron los datos",'especialidad':[]} 
                    return JsonResponse(especialidad)
        else:
            especialidad = list(EspecialidadMedico.objects.values())
            if len(especialidad) > 0:
                especialidad = {'message': "Consulta exitosa", 'especialidad': especialidad}
            else:
                especialidad = {'message': "No se encontraron los datos", 'especialidad':[]} 
        return JsonResponse(especialidad)

#Agregar un registro de cargos
    def post(self, request):
        jd=json.loads(request.body)
        if len(jd['nombre']) <= 0:
            especialidad = {'message': "El nombre esta vacío."}
        elif validar_especialidad_repetida(jd['nombre']):
            especialidad = {'message': "El nombre ya existe."}
        elif len(jd['nombre']) < 4:
            especialidad = {'message': "El nombre debe tener mas de 4 caracteres."}
        elif not validar_cadena_espacios(jd['nombre']):
            especialidad = {'message': "No se permiten mas de un espacio consecutivo."}
        elif validar_cadena_repeticion(jd['nombre']):
            especialidad = {'message': "No se permiten mas de dos caracteres consecutivos del mismo tipo."}     
        elif len(jd['nombre']) > 50:
            especialidad = {'message': "El nombre debe tener menos de 50 caracteres."}
        elif len(jd['descripcion']) <= 0:
            especialidad = {'message': "La descripción esta vacía."}
        elif len(jd['descripcion']) < 4:
            especialidad = {'message': "La descripción debe tener mas de 4 caracteres."}
        elif not validar_cadena_espacios(jd['descripcion']):
            especialidad = {'message': "No se permiten mas de un espacio consecutivo."}
        elif validar_cadena_repeticion(jd['descripcion']):
            especialidad = {'message': "No se permiten mas de dos caracteres consecutivos del mismo tipo."}     
        elif len(jd['descripcion']) > 50:
            especialidad = {'message': "La descripción debe tener menos de 50 caracteres."}
        else:
            especialidad = {'message': "Registro Exitoso."}
            EspecialidadMedico.objects.create(nombre=jd['nombre'], descripcion=jd['descripcion'])
            especialidad = {'message':"Registro Exitoso."}
        return JsonResponse(especialidad)

#Actualizar un registro de cargos
    def put(self, request,id):
        jd=json.loads(request.body)
        especialidad = list(EspecialidadMedico.objects.filter(id=id).values())
        if len(especialidad) > 0:
            especialidades=EspecialidadMedico.objects.get(id=id)
            if len(jd['nombre']) <= 0:
                especialidad = {'message': "El nombre esta vacío."}
            elif len(jd['nombre']) < 4:
                especialidad = {'message': "El nombre debe tener mas de 4 caracteres."}
            elif not validar_cadena_espacios(jd['nombre']):
                especialidad = {'message': "No se permiten mas de un espacio consecutivo."}
            elif validar_cadena_repeticion(jd['nombre']):
                especialidad = {'message': "No se permiten mas de dos caracteres consecutivos del mismo tipo."}     
            elif len(jd['nombre']) > 50:
                especialidad = {'message': "El nombre debe tener menos de 50 caracteres."}
            elif len(jd['descripcion']) <= 0:
                especialidad = {'message': "La descripción esta vacía."}
            elif len(jd['descripcion']) < 4:
                especialidad = {'message': "La descripción debe tener mas de 4 caracteres."}
            elif not validar_cadena_espacios(jd['descripcion']):
                especialidad = {'message': "No se permiten mas de un espacio consecutivo."}
            elif validar_cadena_repeticion(jd['descripcion']):
                especialidad = {'message': "No se permiten mas de dos caracteres consecutivos del mismo tipo."}     
            elif len(jd['descripcion']) > 50:
                especialidad = {'message': "La descripción debe tener menos de 50 caracteres."}
            else:
                especialidad = {'message': "Registro Exitoso."}
                especialidades.nombre = jd['nombre']
                especialidades.descripcion = jd['descripcion']
                especialidades.save()
                especialidad = {'message': "La actualización fue exitosa."}
        return JsonResponse(especialidad)
        
        
#Eliminar un registro de cargos
    def delete(self, request,id):
        especialidad = list(EspecialidadMedico.objects.filter(id=id).values())
        if len(especialidad) > 0:
            EspecialidadMedico.objects.filter(id=id).delete()
            datos = {'message':"Registro Eliminado"}
        else:
            datos = {'message':"No se encontraró el registro", 'especialidad':[]}
        return JsonResponse(datos)

def validar_especialidad_repetida(nombre): 
    if (nombre):
        registros = EspecialidadMedico.objects.filter(nombre=nombre)
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