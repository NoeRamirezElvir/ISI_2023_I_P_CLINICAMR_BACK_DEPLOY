from django.http.response import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
import re
from ..models import *
from django.views.decorators.http import require_http_methods

@method_decorator(require_http_methods(['POST','PUT','GET','DELETE']), name='dispatch')
class Tipo_muestraViews(View):
    #Este metodo permite realizar las conultas que necesitan autentificacion. POST PUT DELETE
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    #Busquedas personalizadas y por defecto
    #las personalizadas varian segun el criterio ingresado, y por defecto muestra todos los objetos
    def get(self, request, campo="",criterio=""):
        if (len(campo)> 0 and len(criterio)> 0):
            if(criterio=="id"):
                tmuestra = list(TipoMuestra.objects.filter(id=campo).values())
                if len(tmuestra) > 0:
                    tmuestra= tmuestra
                    tmuestra = {'message': "Consulta exitosa", 'tmuestra': tmuestra}
                else:
                    tmuestra = {'message': "No se encontraron los datos", 'tmuestra':[]} 
                    return JsonResponse(tmuestra)
            elif(criterio=="nombre"):
                tmuestra = list(TipoMuestra.objects.filter(nombre=campo).values())
                if len(tmuestra) > 0:
                    tmuestra = tmuestra
                    tmuestra = {'message': "Consulta exitosa", 'tmuestra': tmuestra}
                else:
                    tmuestra = {'message': "No se encontraron los datos",'tmuestra':[]} 
                    return JsonResponse(tmuestra)
        else:
            tmuestra = list(TipoMuestra.objects.values())
            if len(tmuestra) > 0:
                tmuestra = {'message': "Consulta exitosa", 'tmuestra': tmuestra}
            else:
                tmuestra = {'message': "No se encontraron los datos", 'tmuestra':[]} 
        return JsonResponse(tmuestra)

#Agregar un registro de cargos
    def post(self, request):
        jd=json.loads(request.body)
        if len(jd['nombre']) <= 0:
            tmuestra = {'message': "El nombre esta vacío."}
        elif validar_tmuestra_repetida(jd['nombre']):
            tmuestra = {'message': "El nombre ya existe."}
        elif len(jd['nombre']) < 4:
            tmuestra = {'message': "El nombre debe tener mas de 4 caracteres."}
        elif not validar_cadena_espacios(jd['nombre']):
            tmuestra = {'message': "No se permiten mas de un espacio consecutivo."}
        elif validar_cadena_repeticion(jd['nombre']):
            tmuestra = {'message': "No se permiten mas de dos caracteres consecutivos del mismo tipo."}     
        elif len(jd['nombre']) > 50:
            tmuestra = {'message': "El nombre debe tener menos de 50 caracteres."}
        elif len(jd['metodoConservacion']) <= 0:
            tmuestra = {'message': "El metodo de conservacion esta vacía."}
        elif len(jd['metodoConservacion']) < 4:
            tmuestra = {'message': "El metodo de conservacion debe tener mas de 4 caracteres."}
        elif not validar_cadena_espacios(jd['metodoConservacion']):
            tmuestra = {'message': "No se permiten mas de un espacio consecutivo."}
        elif validar_cadena_repeticion(jd['metodoConservacion']):
            tmuestra = {'message': "No se permiten mas de dos caracteres consecutivos del mismo tipo."}     
        elif len(jd['metodoConservacion']) > 50:
            tmuestra = {'message': "El metodo de conservacion debe tener menos de 50 caracteres."}
        else:
            tmuestra = {'message': "Registro Exitoso."}
            TipoMuestra.objects.create(nombre=jd['nombre'], metodoConservacion=jd['metodoConservacion'])
            tmuestra = {'message':"Registro Exitoso."}
        return JsonResponse(tmuestra)

#Actualizar un registro de cargos
    def put(self, request,id):
        jd=json.loads(request.body)
        tmuestra = list(TipoMuestra.objects.filter(id=id).values())
        if len(tmuestra) > 0:
            tmuestras=TipoMuestra.objects.get(id=id)
            if len(jd['nombre']) <= 0:
                tmuestra = {'message': "El nombre esta vacío."}
            elif len(jd['nombre']) < 4:
                tmuestra = {'message': "El nombre debe tener mas de 4 caracteres."}
            elif not validar_cadena_espacios(jd['nombre']):
                tmuestra = {'message': "No se permiten mas de un espacio consecutivo."}
            elif validar_cadena_repeticion(jd['nombre']):
                tmuestra = {'message': "No se permiten mas de dos caracteres consecutivos del mismo tipo."}     
            elif len(jd['nombre']) > 50:
                tmuestra = {'message': "El nombre debe tener menos de 50 caracteres."}
            elif len(jd['metodoConservacion']) <= 0:
                tmuestra = {'message': "El metodo de conservacion esta vacía."}
            elif len(jd['metodoConservacion']) < 4:
                tmuestra = {'message': "El metodo de conservacion debe tener mas de 4 caracteres."}
            elif not validar_cadena_espacios(jd['metodoConservacion']):
                tmuestra = {'message': "No se permiten mas de un espacio consecutivo."}
            elif validar_cadena_repeticion(jd['metodoConservacion']):
                tmuestra = {'message': "No se permiten mas de dos caracteres consecutivos del mismo tipo."}     
            elif len(jd['metodoConservacion']) > 50:
                tmuestra = {'message': "El metodo de conservacion debe tener menos de 50 caracteres."}
            else:
                tmuestra = {'message': "Registro Exitoso."}
                tmuestras.nombre = jd['nombre']
                tmuestras.metodoConservacion = jd['metodoConservacion']
                tmuestras.save()
                tmuestra = {'message': "La actualización fue exitosa."}
        return JsonResponse(tmuestra)
        
        
#Eliminar un registro de cargos
    def delete(self, request,id):
        tmuestra = list(TipoMuestra.objects.filter(id=id).values())
        if len(tmuestra) > 0:
            TipoMuestra.objects.filter(id=id).delete()
            datos = {'message':"Registro Eliminado"}
        else:
            datos = {'message':"No se encontraró el registro", 'tmuestra':[]}
        return JsonResponse(datos)

def validar_tmuestra_repetida(nombre): 
    if (nombre):
        registros = TipoMuestra.objects.filter(nombre=nombre)
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