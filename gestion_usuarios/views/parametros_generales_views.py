from datetime import datetime, timedelta
from django.http.response import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
import re
from ..models import *
from django.views.decorators.http import require_http_methods

@method_decorator(require_http_methods(['POST','PUT','GET','DELETE']), name='dispatch')
class Parametros_GeneralesViews(View):
    #Este metodo permite realizar las conultas que necesitan autentificacion. POST PUT DELETE
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    #Busquedas personalizadas y por defecto
    #las personalizadas varian segun el criterio ingresado, y por defecto muestra todos los objetos
    def get(self, request, campo="",criterio=""):
        if (len(campo)> 0 and len(criterio)> 0):
            if criterio == "id":
                parametrosgenerales = list(ParametrosGenerales.objects.filter(id=campo).values())
                if len(parametrosgenerales ) > 0:
                    parametrosgenerales  = parametrosgenerales 
                    parametrosgenerales  = {'message': "Consulta exitosa", 'parametrosgenerales': parametrosgenerales }
                else:
                    parametrosgenerales  = {'message': "No se encontraron los datos", 'parametrosgenerales': []} 
                    return JsonResponse(parametrosgenerales )
            elif criterio == "nombre":
                parametrosgenerales  = list(ParametrosGenerales.objects.filter(nombre=campo).values())
                if len(parametrosgenerales ) > 0:
                    parametrosgenerales  = parametrosgenerales 
                    parametrosgenerales  = {'message': "Consulta exitosa", 'parametrosgenerales': parametrosgenerales }
                else:
                    parametrosgenerales  = {'message': "No se encontraron los datos", 'parametrosgenerales': []} 
                    return JsonResponse(parametrosgenerales )
        else:
            parametrosgenerales  = list(ParametrosGenerales.objects.values())
            if len(parametrosgenerales ) > 0:
                parametrosgenerales  = {'message': "Consulta exitosa", 'parametrosgenerales': parametrosgenerales }
            else:
                parametrosgenerales  = {'message': "No se encontraron los datos", 'parametrosgenerales': []} 
        return JsonResponse(parametrosgenerales )

#Agregar un registro de parametros
    def post(self, request):
        jd=json.loads(request.body)
        if len(jd['nombre']) <= 0:
            parametrosgenerales  = {'message': "El nombre esta vacío."}
        elif len(jd['nombre']) < 2:
            parametrosgenerales  = {'message': "El nombre debe tener mas de 2 caracteres."}
        elif not validar_cadena_espacios(jd['nombre']):
            parametrosgenerales  = {'message': "No se permiten mas de un espacio consecutivo.[nombre]"}
        elif validar_cadena_repeticion(jd['nombre']):
            parametrosgenerales  = {'message': "No se permiten mas de dos caracteres consecutivos del mismo tipo.[nombre]"}
        elif len(jd['nombre']) > 50:
            parametrosgenerales  = {'message': "El nombre debe tener menos de 50 caracteres."}
        elif len(jd['descripcion']) <= 0:
                parametrosgenerales = {'message': "La descripción esta vacía."}
        elif len(jd['descripcion']) < 4:
                parametrosgenerales = {'message': "La descripción debe tener mas de 4 caracteres."}
        elif not validar_cadena_espacios(jd['descripcion']):
                parametrosgenerales = {'message': "No se permiten mas de un espacio consecutivo.[descripción]"}
        elif validar_cadena_repeticion(jd['descripcion']):
                parametrosgenerales = {'message': "No se permiten mas de dos caracteres consecutivos del mismo tipo.[descripción]"}     
        elif len(jd['descripcion']) > 50:
                parametrosgenerales = {'message': "La descripción debe tener menos de 50 caracteres."}
        elif len(jd['valor']) <= 0:
            parametrosgenerales = {'message': "El valor esta vacía."}
        elif len(jd['valor']) < 4:
                parametrosgenerales = {'message': "El valor debe tener mas de 4 caracteres."}
        elif not validar_cadena_espacios(jd['valor']):
                parametrosgenerales = {'message': "No se permiten mas de un espacio consecutivo.[valor]"}
        elif validar_cadena_repeticion(jd['valor']):
                parametrosgenerales = {'message': "No se permiten mas de dos caracteres consecutivos del mismo tipo.[valor]"}     
        elif len(jd['valor']) > 50:
                parametrosgenerales = {'message': "El valor debe tener menos de 50 caracteres."}
        else:
            
            parametrosgenerales = {'message': "Registro Exitoso."}
            ParametrosGenerales.objects.create(nombre=jd['nombre'], descripcion=jd['descripcion'],valor=jd['valor'])
            parametrosgenerales = {'message':"Registro Exitoso."}
        return JsonResponse(parametrosgenerales)

    
    
        

#Actualizar un registro de parametrosgenerales 
    def put(self, request,id):
        jd=json.loads(request.body)
        parametrosgenerales  = list(ParametrosGenerales.objects.filter(id=id).values())
        if len(parametrosgenerales ) > 0:
            parametrogeneral=ParametrosGenerales.objects.get(id=id)
            if len(jd['nombre']) <= 0:
                parametrosgenerales  = {'message': "El nombre esta vacío."}
            elif len(jd['nombre']) < 4:
                parametrosgenerales  = {'message': "El nombre debe tener mas de 4 caracteres."}
            elif not validar_cadena_espacios(jd['nombre']):
                parametrosgenerales  = {'message': "No se permiten mas de un espacio consecutivo."}
            elif validar_cadena_repeticion(jd['nombre']):
                parametrosgenerales  = {'message': "No se permiten mas de dos caracteres consecutivos del mismo tipo."}
            elif len(jd['nombre']) > 20:
                parametrosgenerales  = {'message': "El nombre debe tener menos de 20 caracteres."}
            elif len(jd['descripcion']) <= 0:
                parametrosgenerales = {'message': "La descripción esta vacía."}
            elif len(jd['descripcion']) < 4:
                parametrosgenerales = {'message': "La descripción debe tener mas de 4 caracteres."}
            elif not validar_cadena_espacios(jd['descripcion']):
                parametrosgenerales = {'message': "No se permiten mas de un espacio consecutivo."}
            elif validar_cadena_repeticion(jd['descripcion']):
                parametrosgenerales = {'message': "No se permiten mas de dos caracteres consecutivos del mismo tipo."}     
            elif len(jd['descripcion']) > 50:
                parametrosgenerales = {'message': "La descripción debe tener menos de 50 caracteres."}
            elif len(jd['valor']) <= 0:
                parametrosgenerales = {'message': "El valor esta vacía."}
            elif len(jd['valor']) < 4:
                    parametrosgenerales = {'message': "El valor debe tener mas de 4 caracteres."}
            elif not validar_cadena_espacios(jd['valor']):
                    parametrosgenerales = {'message': "No se permiten mas de un espacio consecutivo.[valor]"}
            elif validar_cadena_repeticion(jd['valor']):
                    parametrosgenerales = {'message': "No se permiten mas de dos caracteres consecutivos del mismo tipo.[valor]"}     
            elif len(jd['valor']) > 50:
                    parametrosgenerales = {'message': "El valor debe tener menos de 50 caracteres."}

            else:
                parametrosgenerales = {'message': "Registro Exitoso."}
                parametrogeneral.nombre = jd['nombre']
                parametrogeneral.descripcion = jd['descripcion']
                parametrogeneral.valor = jd['valor']
                parametrogeneral.save()
                parametrosgenerales = {'message': "La actualización fue exitosa."}
        
        return JsonResponse(parametrosgenerales )


    def delete(self, request,id):
        parametrosgenerales  = list(ParametrosGenerales.objects.filter(id=id).values())
        if len(parametrosgenerales ) > 0:
            ParametrosGenerales.objects.filter(id=id).delete()
            datos = {'message':"Registro Eliminado"}
        else:
            datos = {'message':"No se encontraró el registro", 'parametrosgenerales': []}
        return JsonResponse(datos)       
    




def validar_valor_repetido(valor): 
    if (valor):
        registros = ParametrosGenerales.objects.filter(valor=valor)
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


