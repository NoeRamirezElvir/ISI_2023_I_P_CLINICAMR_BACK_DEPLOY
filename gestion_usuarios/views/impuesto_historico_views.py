from datetime import datetime
from django.http.response import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
import re
from ..models import *
from django.views.decorators.http import require_http_methods

@method_decorator(require_http_methods(['POST','PUT','GET','DELETE']), name='dispatch')
class ImpuestoHistorico(View):
    #Este metodo permite realizar las conultas que necesitan autentificacion. POST PUT DELETE
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    #Busquedas personalizadas y por defecto
    #las personalizadas varian segun el criterio ingresado, y por defecto muestra todos los objetos
    def get(self, request, campo="",criterio=""):
        if (len(campo)> 0 and len(criterio)> 0):
            if criterio == "id":
                historicos = ImpuestoHitorico.objects.filter(id=campo).select_related('idImpuesto')
                if historicos is not None:
                    historicos_values = []
                    for historico in historicos:
                        impuesto = historico.idImpuesto
                        historico_dict = {
                            'id': historico.id,
                            'fechaInicio': formato_fecha(historico.fechaInicio),
                            'fechaFinal': formato_fecha(historico.fechaFinal),
                            'valor': historico.valor,
                            'idImpuesto': {
                                'id': impuesto.id,
                                'nombre': impuesto.nombre,
                                'valor': impuesto.valor
                            }
                        }
                        historicos_values.append(historico_dict)
                        context = {
                            'message': "Consulta exitosa",
                            'historicos': historicos_values
                        }
                        return JsonResponse(context)
                else:
                    context = {
                        'message': "No se encontraron los datos",
                        'historicos': []
                    }
                    return JsonResponse(context)
            elif criterio == "nombre":
                idImpuesto = Impuesto.objects.filter(nombre=campo)
                if idImpuesto is not None:
                    for impuesto in idImpuesto:
                        reg = ImpuestoHitorico.objects.filter(idImpuesto=impuesto.id).select_related('idImpuesto')
                        if reg is not None:
                            historicos_values = []
                            for historico in reg:
                                impuesto = historico.idImpuesto
                                historico_dict = {
                                    'id': historico.id,
                                    'fechaInicio': formato_fecha(historico.fechaInicio),
                                    'fechaFinal': formato_fecha(historico.fechaFinal),
                                    'valor': historico.valor,
                                    'idImpuesto': {
                                        'id': impuesto.id,
                                        'nombre': impuesto.nombre,
                                        'valor': impuesto.valor
                                    }
                                }
                                historicos_values.append(historico_dict)
                            context = {
                                'message': "Consulta exitosa",
                                'historicos': historicos_values
                            }
                            return JsonResponse(context)
                        else:
                            context = {
                                'message': "No se encontraron los datos",
                                'historicos': []
                            }
                            return JsonResponse(context)
                else:
                    context = {
                        'message': "No se encontraron los datos",
                        'historicos': []
                    }
                    return JsonResponse(context)
            context = {
                    'message': "No se encontraron los datos",
                    'historicos': []
                }
            return JsonResponse(context)
        else:
            reg = ImpuestoHitorico.objects.select_related('idImpuesto')
            if reg is not None:
                historicos_values = []
                for historico in reg:
                    impuesto = historico.idImpuesto
                    historico_dict = {
                        'id': historico.id,
                        'fechaInicio': formato_fecha(historico.fechaInicio),
                        'fechaFinal': formato_fecha(historico.fechaFinal),
                        'valor': historico.valor,
                        'idImpuesto': {
                            'id': impuesto.id,
                            'nombre': impuesto.nombre,
                            'valor': impuesto.valor
                        }
                    }
                    historicos_values.append(historico_dict)
                context = {
                    'message': "Consulta exitosa",
                    'historicos': historicos_values
                }
                return JsonResponse(context)
            else:
                context = {
                    'message': "No se encontraron los datos",
                    'historicos': []
                }
                return JsonResponse(context)

#Agregar un registro de Impuesto
    def post(self, request):
        jd=json.loads(request.body)
        if jd['valor'] <= 0:
            historicos = {'message': "El valor debe ser mayor a 0."}
        elif len(str(jd['valor']))< 1:
            historicos = {'message': "El valor es muy corto."}
        elif len(str(jd['valor']))> 4:
            historicos = {'message': "El valor es muy largo."}
        elif jd['valor'] > 1:
            historicos = {'message': "El valor es muy alto."}
        else:
            historicoTemp = ImpuestoHitorico.objects.filter(idImpuesto=jd['idImpuesto']).last()
            impuesto = Impuesto.objects.filter(id=jd['idImpuesto']).last()
            if historicoTemp is not None and impuesto is not None:
                historicoTemp.fechaFinal =datetime.now()
                imp = Impuesto.objects.filter(valor=jd['valor'])
                if imp.count() >= 1:
                    historicos = {'message':"El valor ya esta en uso en otro impuesto"}
                else:
                    impuesto.valor = jd['valor']
                    historicoTemp.save()
                    impuesto.save()
                    ImpuestoHitorico.objects.create(idImpuesto=instanciar_impuesto(jd['idImpuesto']), fechaInicio=datetime.now(),valor=jd['valor'])
                    historicos = {'message': "Registro Exitoso."}
        return JsonResponse(historicos)
    
    
        

#Actualizar un registro de Impuestos
    def put(self, request,id):
        jd=json.loads(request.body)
        historicos = list(ImpuestoHitorico.objects.filter(id=id).values())
        if len(historicos) > 0:
            historico=ImpuestoHitorico.objects.get(id=id)
            if jd['valor'] <= 0:
                historicos = {'message': "El valor debe ser mayor a 0."}
            elif len(str(jd['valor']))< 1:
                historicos = {'message': "El valor es muy corto."}
            elif len(str(jd['valor']))> 4:
                historicos = {'message': "El valor es muy largo."}
            elif jd['valor'] > 1:
                historicos = {'message': "El valor es muy alto."}
            else:
                historicoTemp = ImpuestoHitorico.objects.filter(idImpuesto=jd['idImpuesto']).last()
                impuesto = Impuesto.objects.filter(id=jd['idImpuesto']).last()
                if  historicoTemp is not None and impuesto is not None:
                    historicoTemp.fechaFinal =datetime.now()
                    imp = Impuesto.objects.filter(valor=jd['valor'])
                    if imp.count() >= 1:
                        historicos = {'message':"El valor ya esta en uso en otro impuesto"}
                    else:
                        historico.fechaFinal = datetime.now()
                        historico.save()
                        impuesto.valor = jd['valor']
                        impuesto.save()
                        historicoTemp.save()
                        ImpuestoHitorico.objects.create(idImpuesto=instanciar_impuesto(jd['idImpuesto']), fechaInicio=datetime.now(),valor=jd['valor'])
                        historicos = {'message': "Registro Exitoso."}
        return JsonResponse(historicos)


    def delete(self, request,id):
        historico = list(ImpuestoHitorico.objects.filter(id=id).values())
        if len(historico) > 0:
            ImpuestoHitorico.objects.filter(id=id).delete()
            datos = {'message':"Registro Eliminado"}
        else:
            datos = {'message':"No se encontraró el registro", 'Impuestos': []}
        return JsonResponse(datos)       
    

def formato_fecha(fecha):
    if fecha is not None:
        fecha_formateada = fecha.strftime("%d-%m-%Y %H:%M:%S")
        return fecha_formateada
    else:
        return None

def validar_Impuesto_repetido(nombre): 
    if (nombre):
        registros = Impuesto.objects.filter(nombre=nombre)
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
        impuesto = Impuesto.objects.get(nombre=nombre)
    if impuesto:
        return impuesto
    
def instanciar_impuesto(id):
    if (id):
        impuesto = Impuesto.objects.get(id=id)
    if impuesto:
        return impuesto
    
def validar_valor(valor): 
    if (valor):
        registros = ImpuestoHitorico.objects.filter(valor=valor)
        if len(registros) > 0:
            return True
        else:
            return False
    return False

