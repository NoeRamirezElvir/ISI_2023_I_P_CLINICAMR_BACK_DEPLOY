from django.http.response import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
import re
from ..models import *
from django.views.decorators.http import require_http_methods

@method_decorator(require_http_methods(['POST','PUT','GET','DELETE']), name='dispatch')
class RecaudoDetalleMedicamentoView(View):
    #Este metodo permite realizar las conultas que necesitan autentificacion. POST PUT DELETE
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    #Busquedas personalizadas y por defecto
    #las personalizadas varian segun el criterio ingresado, y por defecto muestra todos los objetos
    def get(self, request, campo="",criterio=""):
        if (len(campo)> 0 and len(criterio)> 0):
            if criterio == "id":
                detalles = RecaudoDetalleMedicamento.objects.filter(id=campo).select_related('idMedicamento','idRecaudo')
                if len(detalles) > 0:
                    detalle_values = []
                    for detalle in detalles:
                        detalle_dict={
                            'id':detalle.id,
                            'idMedicamento':{
                                'id':detalle.idMedicamento.id,
                                'nombre':detalle.idMedicamento.nombre,
                                'cantidad':detalle.cantidad
                                
                            },
                            'idRecaudo':{
                                'id':detalle.idRecaudo.id,
                                'noFactura':detalle.idRecaudo.noFactura,
                                'estado':detalle.idRecaudo.estado
                            }
                        }
                        detalle_values.append(detalle_dict)
                    context = {'message': "Consulta exitosa", 'detalles': detalle_values}
                    return JsonResponse(context)
                else:
                    context = {'message': "No se encontraron los datos", 'detalles': []} 
                    return JsonResponse(context)
            elif criterio == "numeroFactura":
                detalles = RecaudoDetalleMedicamento.objects.filter(idRecaudo__noFactura=campo).select_related('idMedicamento','idRecaudo')
                if len(detalles) > 0:
                    detalle_values = []
                    for detalle in detalles:
                        detalle_dict={
                            'id':detalle.id,
                            'idMedicamento':{
                                'id':detalle.idMedicamento.id,
                                'nombre':detalle.idMedicamento.nombre,
                                'cantidad':detalle.cantidad
                                
                            },
                            'idRecaudo':{
                                'id':detalle.idRecaudo.id,
                                'noFactura':detalle.idRecaudo.noFactura,
                                'estado':detalle.idRecaudo.estado
                            }
                        }
                        detalle_values.append(detalle_dict)
                    context = {'message': "Consulta exitosa", 'detalles': detalle_values}
                    return JsonResponse(context)
                else:
                    context = {'message': "No se encontraron los datos", 'detalles': []} 
                    return JsonResponse(context)
        else:
            detalles = RecaudoDetalleMedicamento.objects.select_related('idMedicamento','idRecaudo')
            if len(detalles) > 0:
                detalle_values = []
                for detalle in detalles:
                    detalle_dict={
                        'id':detalle.id,
                        'idMedicamento':{
                            'id':detalle.idMedicamento.id,
                            'nombre':detalle.idMedicamento.nombre,
                            'cantidad':detalle.cantidad
                            
                        },
                        'idRecaudo':{
                            'id':detalle.idRecaudo.id,
                            'noFactura':detalle.idRecaudo.noFactura,
                            'estado':detalle.idRecaudo.estado
                        }
                    }
                    detalle_values.append(detalle_dict)
                context = {'message': "Consulta exitosa", 'detalles': detalle_values}
                return JsonResponse(context)
            else:
                context = {'message': "No se encontraron los datos", 'detalles': []} 
                return JsonResponse(context)
    
        
#Eliminar un registro de cargos
    def delete(self, request,id):
        detalles = list(RecaudoDetalleMedicamento.objects.filter(id=id).values())
        if len(detalles) > 0:
            RecaudoDetalleMedicamento.objects.filter(id=id).delete()
            datos = {'message':"Registro Eliminado"}
        else:
            datos = {'message':"No se encontraron registros", 'detalles': []}
        return JsonResponse(datos)
    