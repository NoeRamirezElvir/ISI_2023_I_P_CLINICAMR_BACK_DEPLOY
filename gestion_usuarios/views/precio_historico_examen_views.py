from datetime import datetime, timedelta
from decimal import Decimal
from django.http.response import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
import re
from ..models import *
from django.views.decorators.http import require_http_methods

@method_decorator(require_http_methods(['POST','PUT','GET','DELETE']), name='dispatch')
class PrecioHistoricoExamenesViews(View):
    #Este metodo permite realizar las conultas que necesitan autentificacion. POST PUT DELETE
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    #Busquedas personalizadas y por defecto
    #las personalizadas varian segun el criterio ingresado, y por defecto muestra todos los objetos
    def get(self, request, campo="",criterio=""):
        if (len(campo)> 0 and len(criterio)> 0):
            if criterio == "id":
                precioHistoricos = PrecioHistoricoExamen.objects.filter(id=campo).select_related('idTipo')
                if precioHistoricos is not None:
                    historicos_values = []
                    for historico in precioHistoricos:
                        historico_dict = {
                            'id': historico.id,
                            'fechaInicio': formato_fecha(historico.fechaInicio),
                            'fechaFinal': formato_fecha(historico.fechaFinal),
                            'activo':historico.activo,
                            'precio': historico.precio,
                            'idTipo': {
                                'id': historico.idTipo.id,
                                'nombre': historico.idTipo.nombre,
                                'idsubtipo':{
                                    'id': historico.idTipo.idsubtipo.id,
                                    'nombre': historico.idTipo.idsubtipo.nombre,
                                }
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
                precioHistoricos = PrecioHistoricoExamen.objects.filter(idTipo__nombre=campo)
                if precioHistoricos is not None:
                    historicos_values = []
                    for historico in precioHistoricos:
                        historico_dict = {
                            'id': historico.id,
                            'fechaInicio': formato_fecha(historico.fechaInicio),
                            'fechaFinal': formato_fecha(historico.fechaFinal),
                            'activo':historico.activo,
                            'precio': historico.precio,
                            'idTipo': {
                                'id': historico.idTipo.id,
                                'nombre': historico.idTipo.nombre,
                                'idsubtipo':{
                                    'id': historico.idTipo.idsubtipo.id,
                                    'nombre': historico.idTipo.idsubtipo.nombre,
                                }
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
            precioHistoricos = PrecioHistoricoExamen.objects.select_related('idTipo')
            if precioHistoricos is not None:
                historicos_values = []
                for historico in precioHistoricos:
                    historico_dict = {
                        'id': historico.id,
                        'fechaInicio': formato_fecha(historico.fechaInicio),
                        'fechaFinal': formato_fecha(historico.fechaFinal),
                        'activo':historico.activo,
                        'precio': historico.precio,
                        'idTipo': {
                            'id': historico.idTipo.id,
                            'nombre': historico.idTipo.nombre,
                            'idsubtipo':{
                                'id': historico.idTipo.idsubtipo.id,
                                'nombre': historico.idTipo.idsubtipo.nombre,
                            }
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

#Eliminar un registro de cargos
    def delete(self, request,id):
        precioHistorico = list(PrecioHistoricoExamen.objects.filter(id=id).values())
        if len(precioHistorico) > 0:
            PrecioHistoricoExamen.objects.filter(id=id).delete()
            precioHistorico = {'message':"Registro Eliminado"}
        else:
            precioHistorico = {'message':"No se encontró el registro", 'precioHistorico': []}
        return JsonResponse(precioHistorico)

def formato_fecha(fecha):
    if fecha is not None:
        fecha_formateada = fecha.strftime("%d-%m-%Y %H:%M:%S")
        return fecha_formateada
    else:
        return None