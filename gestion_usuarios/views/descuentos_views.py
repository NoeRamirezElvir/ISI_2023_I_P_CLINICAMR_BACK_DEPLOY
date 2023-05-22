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
class DescuentoViews(View):
    #Este metodo permite realizar las conultas que necesitan autentificacion. POST PUT DELETE
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    #Busquedas personalizadas y por defecto
    #las personalizadas varian segun el criterio ingresado, y por defecto muestra todos los objetos
    def get(self, request, campo="",criterio=""):
        if (len(campo)> 0 and len(criterio)> 0):
            if criterio == "id":
                Descuentos = list(Descuento.objects.filter(id=campo).values())
                if len(Descuentos) > 0:
                    Descuentos = Descuentos
                    Descuentos = {'message': "Consulta exitosa", 'Descuentos': Descuentos}
                else:
                    Descuentos = {'message': "No se encontraron los datos", 'Descuentos': []} 
                    return JsonResponse(Descuentos)
            elif criterio == "nombre":
                Descuentos = list(Descuento.objects.filter(nombre=campo).values())
                if len(Descuentos) > 0:
                    Descuentos = Descuentos
                    Descuentos = {'message': "Consulta exitosa", 'Descuentos': Descuentos}
                else:
                    Descuentos = {'message': "No se encontraron los datos", 'Descuentos': []} 
                    return JsonResponse(Descuentos)
        else:
            Descuentos = list(Descuento.objects.values())
            if len(Descuentos) > 0:
                Descuentos = {'message': "Consulta exitosa", 'Descuentos': Descuentos}
            else:
                Descuentos = {'message': "No se encontraron los datos", 'Descuentos': []} 
        return JsonResponse(Descuentos)

#Agregar un registro de descuento
    def post(self, request):
        jd=json.loads(request.body)
        if len(jd['nombre']) <= 0:
            Descuentos = {'message': "El nombre esta vacío."}
        elif (validar_descuento_repetido(jd['nombre'])):
            Descuentos = {'message': "El descuento ya existe."}
        elif len(jd['nombre']) < 2:
            Descuentos = {'message': "El nombre debe tener mas de 2 caracteres."}
        elif not validar_cadena_espacios(jd['nombre']):
            Descuentos = {'message': "No se permiten mas de un espacio consecutivo."}
        elif validar_cadena_repeticion(jd['nombre']):
            Descuentos = {'message': "No se permiten mas de dos caracteres consecutivos del mismo tipo."}
        elif len(jd['nombre']) > 20:
            Descuentos = {'message': "El nombre debe tener menos de 20 caracteres."}
        elif jd['valor'] < 0:
            Descuentos = {'message': "El valor debe ser igual o mayor a 0."}
        elif (validar_valor_repetido(jd['valor'])):
            Descuentos = {'message': "El valor ya esta en uso."}
        elif jd['valor'] > 1:
            Descuentos = {'message': "El valor es muy alto."}
        elif jd['valor'] > 0.25:
            Descuentos = {'message': "El valor es muy alto."}
        else:
            Descuentos = {'message': "Registro Exitoso."}
            Descuento.objects.create(nombre=jd['nombre'], valor=jd['valor'])
            
            
            Descuentos = {'message':"Registro Exitoso."}
        return JsonResponse(Descuentos)
    
    
        

#Actualizar un registro de Descuentos
    def put(self, request,id):
        jd=json.loads(request.body)
        Descuentos = list(Descuento.objects.filter(id=id).values())
        if len(Descuentos) > 0:
            descuento=Descuento.objects.get(id=id)
            if len(jd['nombre']) <= 0:
                Descuentos = {'message': "El nombre esta vacío."}
            elif len(jd['nombre']) < 4:
                Descuentos = {'message': "El nombre debe tener mas de 4 caracteres."}
            elif not validar_cadena_espacios(jd['nombre']):
                Descuentos = {'message': "No se permiten mas de un espacio consecutivo."}
            elif validar_cadena_repeticion(jd['nombre']):
                Descuentos = {'message': "No se permiten mas de dos caracteres consecutivos del mismo tipo."}
            elif len(jd['nombre']) > 20:
                Descuentos = {'message': "El nombre debe tener menos de 20 caracteres."}
            elif jd['valor'] < 0:
                Descuentos = {'message': "El valor debe ser igual o mayor a 0."}
            elif jd['valor'] > 1:
                Descuentos = {'message': "El valor es muy alto."}
            elif jd['valor'] > 0.25:
                Descuentos = {'message': "El valor es muy alto."}
            else:
                Descuentos = {'message': "Registro Exitoso."}
               
            

                descuento.nombre = jd['nombre']
                descuento.valor = jd['valor']
                descuento.save()
                Descuentos = {'message': "La actualización fue exitosa."}
        return JsonResponse(Descuentos)


    def delete(self, request,id):
        Descuentos = list(Descuento.objects.filter(id=id).values())
        if len(Descuentos) > 0:
            Descuento.objects.filter(id=id).delete()
            datos = {'message':"Registro Eliminado"}
        else:
            datos = {'message':"No se encontrarón registros", 'Descuentos': []}
        return JsonResponse(datos)       
    

def validar_descuento_repetido(nombre): 
    if (nombre):
        registros = Descuento.objects.filter(nombre=nombre)
        if len(registros) > 0:
            return True
        else:
            return False
    return False

def validar_valor_repetido(valor): 
    if (valor):
        registros = Descuento.objects.filter(valor=valor)
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
