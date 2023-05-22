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
class ImpuestoViews(View):
    #Este metodo permite realizar las conultas que necesitan autentificacion. POST PUT DELETE
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    #Busquedas personalizadas y por defecto
    #las personalizadas varian segun el criterio ingresado, y por defecto muestra todos los objetos
    def get(self, request, campo="",criterio=""):
        if (len(campo)> 0 and len(criterio)> 0):
            if criterio == "id":
                Impuestos = list(Impuesto.objects.filter(id=campo).values())
                if len(Impuestos) > 0:
                    Impuestos = Impuestos
                    Impuestos = {'message': "Consulta exitosa", 'Impuestos': Impuestos}
                else:
                    Impuestos = {'message': "No se encontraron los datos", 'Impuestos': []} 
                    return JsonResponse(Impuestos)
            elif criterio == "nombre":
                Impuestos = list(Impuesto.objects.filter(nombre=campo).values())
                if len(Impuestos) > 0:
                    Impuestos = Impuestos
                    Impuestos = {'message': "Consulta exitosa", 'Impuestos': Impuestos}
                else:
                    Impuestos = {'message': "No se encontraron los datos", 'Impuestos': []} 
                    return JsonResponse(Impuestos)
        else:
            Impuestos = list(Impuesto.objects.values())
            if len(Impuestos) > 0:
                Impuestos = {'message': "Consulta exitosa", 'Impuestos': Impuestos}
            else:
                Impuestos = {'message': "No se encontraron los datos", 'Impuestos': []} 
        return JsonResponse(Impuestos)

#Agregar un registro de Impuesto
    def post(self, request):
        jd=json.loads(request.body)
        if len(jd['nombre']) <= 0:
            Impuestos = {'message': "El nombre esta vacío."}
        elif (validar_Impuesto_repetido(jd['nombre'])):
            Impuestos = {'message': "El Impuesto ya existe."}
        elif len(jd['nombre']) < 2:
            Impuestos = {'message': "El nombre debe tener mas de 2 caracteres."}
        elif not validar_cadena_espacios(jd['nombre']):
            Impuestos = {'message': "No se permiten mas de un espacio consecutivo."}
        elif validar_cadena_repeticion(jd['nombre']):
            Impuestos = {'message': "No se permiten mas de dos caracteres consecutivos del mismo tipo."}
        elif len(jd['nombre']) > 20:
            Impuestos = {'message': "El nombre debe tener menos de 20 caracteres."}
        elif jd['valor'] <= 0:
            Impuestos = {'message': "El valor debe ser mayor a 0."}
        elif (validar_valor_repetido(jd['valor'])):
            Impuestos = {'message': "El valor ya esta en uso."}
        elif jd['valor'] > 1:
            Impuestos = {'message': "El valor es muy alto."}
        else:
            Impuestos = {'message': "Registro Exitoso."}
            Impuesto.objects.create(nombre=jd['nombre'], valor=jd['valor'])
            ImpuestoHitorico.objects.create(idImpuesto=instanciar_impuesto(jd['nombre']), fechaInicio=datetime.now(),valor=jd['valor'])
            
            Impuestos = {'message':"Registro Exitoso."}
        return JsonResponse(Impuestos)
    
    
        

#Actualizar un registro de Impuestos
    def put(self, request,id):
        jd=json.loads(request.body)
        Impuestos = list(Impuesto.objects.filter(id=id).values())
        if len(Impuestos) > 0:
            impuesto=Impuesto.objects.get(id=id)
            if len(jd['nombre']) <= 0:
                Impuestos = {'message': "El nombre esta vacío."}
            elif len(jd['nombre']) < 4:
                Impuestos = {'message': "El nombre debe tener mas de 4 caracteres."}
            elif not validar_cadena_espacios(jd['nombre']):
                Impuestos = {'message': "No se permiten mas de un espacio consecutivo."}
            elif validar_cadena_repeticion(jd['nombre']):
                Impuestos = {'message': "No se permiten mas de dos caracteres consecutivos del mismo tipo."}
            elif len(jd['nombre']) > 20:
                Impuestos = {'message': "El nombre debe tener menos de 20 caracteres."}
            elif jd['valor'] <= 0:
                Impuestos = {'message': "El valor debe ser mayor a 0."}
            elif jd['valor'] > 1:
                Impuestos = {'message': "El valor es muy alto."}
            else:
                Impuestos = {'message': "Registro Exitoso."}
                nombre_temp=impuesto.nombre
                impuesto.nombre = jd['nombre']
                if float(impuesto.id) == float(id):
                    historico = ImpuestoHitorico.objects.filter(idImpuesto=impuesto.id, valor=impuesto.valor).last()
                    if historico is not None:
                        historico.fechaFinal = fecha_final()
                        historico.save()
                        ImpuestoHitorico.objects.create(idImpuesto=instanciar_impuesto(nombre_temp), fechaInicio=datetime.now(),valor=jd['valor'])
                    else:
                        ImpuestoHitorico.objects.create(idImpuesto=instanciar_impuesto(nombre_temp), fechaInicio=datetime.now(),valor=jd['valor'])
                else:
                    ImpuestoHitorico.objects.create(idImpuesto=instanciar_impuesto(nombre_temp), fechaInicio=datetime.now(),valor=jd['valor'])
                impuesto.valor = jd['valor'] 
                impuesto.save()
                Impuestos = {'message': "La actualización fue exitosa."}
        return JsonResponse(Impuestos)


    def delete(self, request,id):
        Impuestos = list(Impuesto.objects.filter(id=id).values())
        if len(Impuestos) > 0:
            Impuesto.objects.filter(id=id).delete()
            datos = {'message':"Registro Eliminado"}
        else:
            datos = {'message':"No se encontraró el registro", 'Impuestos': []}
        return JsonResponse(datos)       
    


def fecha_final():
    fecha_menos_un_dia=datetime.today()+timedelta(days=-1)
    return fecha_menos_un_dia

def validar_Impuesto_repetido(nombre): 
    if (nombre):
        registros = Impuesto.objects.filter(nombre=nombre)
        if len(registros) > 0:
            return True
        else:
            return False
    return False

def validar_valor_repetido(valor): 
    if (valor):
        registros = Impuesto.objects.filter(valor=valor)
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

def instanciar_impuesto(nombre):
    if (nombre):
        impuesto = Impuesto.objects.filter(nombre=nombre).last()
    if impuesto:
        return impuesto
