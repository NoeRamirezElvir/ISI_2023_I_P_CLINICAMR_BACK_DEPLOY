from django.http.response import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
import re
from ..models import *
from django.views.decorators.http import require_http_methods

@method_decorator(require_http_methods(['POST','PUT','GET','DELETE']), name='dispatch')
class CargosView(View):
    #Este metodo permite realizar las conultas que necesitan autentificacion. POST PUT DELETE
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    #Busquedas personalizadas y por defecto
    #las personalizadas varian segun el criterio ingresado, y por defecto muestra todos los objetos
    def get(self, request, campo="",criterio=""):
        if (len(campo)> 0 and len(criterio)> 0):
            if criterio == "id":
                cargos = list(CargoEmpleado.objects.filter(id=campo).values())
                if len(cargos) > 0:
                    cargos = cargos
                    cargos = {'message': "Consulta exitosa", 'cargos': cargos}
                else:
                    cargos = {'message': "No se encontraron los datos", 'cargos': []} 
                    return JsonResponse(cargos)
            elif criterio == "nombre":
                cargos = list(CargoEmpleado.objects.filter(nombre=campo).values())
                if len(cargos) > 0:
                    cargos = cargos
                    cargos = {'message': "Consulta exitosa", 'cargos': cargos}
                else:
                    cargos = {'message': "No se encontraron los datos", 'cargos': []} 
                    return JsonResponse(cargos)
        else:
            cargos = list(CargoEmpleado.objects.values())
            if len(cargos) > 0:
                cargos = {'message': "Consulta exitosa", 'cargos': cargos}
            else:
                cargos = {'message': "No se encontraron los datos", 'cargos': []} 
        return JsonResponse(cargos)

#Agregar un registro de cargos
    def post(self, request):
        jd=json.loads(request.body)

        if len(jd['nombre']) <= 0:
            cargos = {'message': "El nombre esta vacío."}
        elif (validar_cargo_repetido(jd['nombre'])):
            cargos = {'message': "El cargo ya existe."}
        elif len(jd['nombre']) < 4:
            cargos = {'message': "El nombre debe tener mas de 4 caracteres."}
        elif not validar_cadena_espacios(jd['nombre']):
            cargos = {'message': "No se permiten mas de un espacio consecutivo."}
        elif validar_cadena_repeticion(jd['nombre']):
            cargos = {'message': "No se permiten mas de dos caracteres consecutivos del mismo tipo."}
        elif len(jd['nombre']) > 50:
            cargos = {'message': "El nombre debe tener menos de 50 caracteres."}
        elif len(jd['descripcion']) <= 0:
            cargos = {'message': "La descripción esta vacía."}
        elif len(jd['descripcion']) < 4:
            cargos = {'message': "La descripción debe tener mas de 4 caracteres."}
        elif len(jd['descripcion']) > 50:
            cargos = {'message': "La descripción debe tener menos de 50 caracteres."}
        elif jd['activo'] < 0:
            cargos = {'message': "Activo debe ser positivo."}
        elif jd['activo'] > 1:
            cargos = {'message': "Activo debe unicamente puede ser 0 o 1."}
        else:
            CargoEmpleado.objects.create(nombre=jd['nombre'], descripcion=jd['descripcion'],activo=jd['activo'])
            cargos = {'message':"Registro Exitoso."}
        return JsonResponse(cargos)

#Actualizar un registro de cargos
    def put(self, request,id):
        jd=json.loads(request.body)
        cargos = list(CargoEmpleado.objects.filter(id=id).values())
        if len(cargos) > 0:
            cargo=CargoEmpleado.objects.get(id=id)
            if len(jd['nombre']) <= 0:
                cargos = {'message': "El nombre esta vacío."}
            elif len(jd['nombre']) < 4:
                cargos = {'message': "El nombre debe tener mas de 4 caracteres."}
            elif not validar_cadena_espacios(jd['nombre']):
                cargos = {'message': "No se permiten mas de un espacio consecutivo."}
            elif validar_cadena_repeticion(jd['nombre']):
                cargos = {'message': "No se permiten mas de dos caracteres consecutivos del mismo tipo."}
            elif len(jd['nombre']) > 50:
                cargos = {'message': "El nombre debe tener menos de 50 caracteres."}
            elif len(jd['descripcion']) <= 0:
                cargos = {'message': "La descripción esta vacía."}
            elif len(jd['descripcion']) < 4:
                cargos = {'message': "La descripción debe tener mas de 4 caracteres."}
            elif len(jd['descripcion']) > 50:
                cargos = {'message': "La descripción debe tener menos de 50 caracteres."}
            elif jd['activo'] < 0:
                cargos = {'message': "Activo debe ser positivo."}
            elif jd['activo'] > 1:
                cargos = {'message': "Activo debe unicamente puede ser 0 o 1."}
            else:
                cargos = {'message': "Registro Exitoso."}
                cargo.nombre = jd['nombre']
                cargo.descripcion = jd['descripcion']
                cargo.activo = jd['activo']
                cargo.save()
                cargos = {'message': "La actualización fue exitosa."}
        return JsonResponse(cargos)
        
        
#Eliminar un registro de cargos
    def delete(self, request,id):
        cargos = list(CargoEmpleado.objects.filter(id=id).values())
        if len(cargos) > 0:
            CargoEmpleado.objects.filter(id=id).delete()
            datos = {'message':"Registro Eliminado"}
        else:
            datos = {'message':"No se encontraró el registro", 'cargos': []}
        return JsonResponse(datos)
    
def validar_cargo_repetido(nombre): 
    if (nombre):
        registros = CargoEmpleado.objects.filter(nombre=nombre)
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
