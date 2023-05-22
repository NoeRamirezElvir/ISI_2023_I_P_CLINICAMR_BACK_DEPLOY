from django.http.response import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
import re
from ..models import *
from django.views.decorators.http import require_http_methods

@method_decorator(require_http_methods(['POST','PUT','GET','DELETE']), name='dispatch')
class metodoPagoViews(View):
    #Este metodo permite realizar las conultas que necesitan autentificacion. POST PUT DELETE
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    #Busquedas personalizadas y por defecto
    #las personalizadas varian segun el criterio ingresado, y por defecto muestra todos los objetos
    def get(self, request, campo="",criterio=""):
        if (len(campo)> 0 and len(criterio)> 0):
            if(criterio=="id"):
                metodop = list(MetodoDePago.objects.filter(id=campo).values())
                if len(metodop) > 0:
                    metodop = metodop
                    metodop = {'message': "Consulta exitosa", 'metodop': metodop}
                else:
                    metodop = {'message': "No se encontraron los datos", 'metodop':[]} 
                    return JsonResponse(metodop)
            elif(criterio=="nombre"):
                metodop = list(MetodoDePago.objects.filter(nombre=campo).values())
                if len(metodop) > 0:
                    metodop = metodop
                    metodop = {'message': "Consulta exitosa", 'metodop': metodop}
                else:
                    metodop = {'message': "No se encontraron los datos",'metodop':[]} 
                    return JsonResponse(metodop)
        else:
            metodop = list(MetodoDePago.objects.values())
            if len(metodop) > 0:
                metodop = {'message': "Consulta exitosa", 'metodop': metodop}
            else:
                metodop = {'message': "No se encontraron los datos", 'metodop':[]} 
        return JsonResponse(metodop)

#Agregar un registro de cargos
    def post(self, request):
        jd=json.loads(request.body)
        if len(jd['nombre']) <= 0:
            metodop = {'message': "El nombre esta vacío."}
        elif validar_metodop_repetida(jd['nombre']):
            metodop = {'message': "El nombre ya existe."}
        elif len(jd['nombre']) < 4:
            metodop = {'message': "El nombre debe tener mas de 4 caracteres."}
        elif not validar_cadena_espacios(jd['nombre']):
            metodop = {'message': "No se permiten mas de un espacio consecutivo."}
        elif validar_cadena_repeticion(jd['nombre']):
            metodop = {'message': "No se permiten mas de dos caracteres consecutivos del mismo tipo."}     
        elif len(jd['nombre']) > 50:
            metodop = {'message': "El nombre debe tener menos de 50 caracteres."}
        elif len(jd['descripcion']) <= 0:
            metodop = {'message': "La descripción esta vacía."}
        elif len(jd['descripcion']) < 4:
            metodop = {'message': "La descripción debe tener mas de 4 caracteres."}
        elif not validar_cadena_espacios(jd['descripcion']):
            metodop = {'message': "No se permiten mas de un espacio consecutivo."}
        elif validar_cadena_repeticion(jd['descripcion']):
            metodop = {'message': "No se permiten mas de dos caracteres consecutivos del mismo tipo."}     
        elif len(jd['descripcion']) > 50:
            metodop = {'message': "La descripción debe tener menos de 50 caracteres."}
        else:
            nombre_minuscula = (jd['nombre']).lower()
            MetodoDePago.objects.create(nombre_minuscula, descripcion=jd['descripcion'])
            metodop = {'message':"Registro Exitoso."}
        return JsonResponse(metodop)

#Actualizar un registro de cargos
    def put(self, request,id):
        jd=json.loads(request.body)
        metodop = list(MetodoDePago.objects.filter(id=id).values())
        if len(metodop) > 0:
            metodopago=MetodoDePago.objects.get(id=id)
            if len(jd['nombre']) <= 0:
                metodop = {'message': "El nombre esta vacío."}
            elif len(jd['nombre']) < 4:
                metodop = {'message': "El nombre debe tener mas de 4 caracteres."}
            elif not validar_cadena_espacios(jd['nombre']):
                metodop = {'message': "No se permiten mas de un espacio consecutivo."}
            elif validar_cadena_repeticion(jd['nombre']):
                metodop = {'message': "No se permiten mas de dos caracteres consecutivos del mismo tipo."}     
            elif len(jd['nombre']) > 50:
                metodop = {'message': "El nombre debe tener menos de 50 caracteres."}
            elif len(jd['descripcion']) <= 0:
                metodop = {'message': "La descripción esta vacía."}
            elif len(jd['descripcion']) < 4:
                metodop = {'message': "La descripción debe tener mas de 4 caracteres."}
            elif not validar_cadena_espacios(jd['descripcion']):
                metodop = {'message': "No se permiten mas de un espacio consecutivo."}
            elif validar_cadena_repeticion(jd['descripcion']):
                metodop = {'message': "No se permiten mas de dos caracteres consecutivos del mismo tipo."}     
            elif len(jd['descripcion']) > 50:
                metodop = {'message': "La descripción debe tener menos de 50 caracteres."}
            else:
                metodop = {'message': "Registro Exitoso."}
                metodopago.nombre = jd['nombre']
                metodopago.descripcion = jd['descripcion']
                metodopago.save()
                metodop = {'message': "La actualización fue exitosa."}
        return JsonResponse(metodop)
        
        
#Eliminar un registro de cargos
    def delete(self, request,id):
        metodop = list(MetodoDePago.objects.filter(id=id).values())
        if len(metodop) > 0:
            MetodoDePago.objects.filter(id=id).delete()
            datos = {'message':"Registro Eliminado"}
        else:
            datos = {'message':"No se encontraró el registro", 'metodop':[]}
        return JsonResponse(datos)

def validar_metodop_repetida(nombre): 
    if (nombre):
        registros = MetodoDePago.objects.filter(nombre=nombre)
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