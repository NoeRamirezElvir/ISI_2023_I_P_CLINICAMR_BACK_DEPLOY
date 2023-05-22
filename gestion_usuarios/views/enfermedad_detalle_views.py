from django.http.response import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
import re
from ..models import *
from django.views.decorators.http import require_http_methods

@method_decorator(require_http_methods(['POST','PUT','GET','DELETE']), name='dispatch')
class EnfermedadDetalleView(View):
    #Este metodo permite realizar las conultas que necesitan autentificacion. POST PUT DELETE
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    #Busquedas personalizadas y por defecto
    #las personalizadas varian segun el criterio ingresado, y por defecto muestra todos los objetos
    def get(self, request, campo="",criterio=""):
        if (len(campo)> 0 and len(criterio)> 0):
            if criterio == "id":
                detalles = EnfermedadDetalle.objects.filter(id=campo).select_related('idEnfermedad','idSintoma')
                if len(detalles) > 0:
                    detalle_values = []
                    for detalle in detalles:
                        detalle_dict={
                            'id':detalle.id,
                            'idEnfermedad':{
                            'id':detalle.idEnfermedad.id,
                            'nombre':detalle.idEnfermedad.nombre
                            },
                            'idSintoma':{
                            'id':detalle.idSintoma.id,
                            'nombre':detalle.idSintoma.nombre
                            }
                        }
                        detalle_values.append(detalle_dict)
                    context = {'message': "Consulta exitosa", 'detalles': detalle_values}
                    return JsonResponse(context)
                else:
                    context = {'message': "No se encontraron los datos", 'detalles': []} 
                    return JsonResponse(context)
            elif criterio == "nombre":
                enfermedades = Enfermedad.objects.filter(nombre=campo)
                if enfermedades is not None:
                    for enfermedad in enfermedades:
                        detalles = EnfermedadDetalle.objects.filter(idEnfermedad=enfermedad.id).select_related('idEnfermedad','idSintoma')
                        if detalles is not None:
                            detalles_values = []
                            for detalle in detalles:
                                enf = detalle.idEnfermedad
                                sin = detalle.idSintoma
                                historico_dict = {
                                    'id': detalle.id,
                                    'idEnfermedad': {
                                        'id': enf.id,
                                        'nombre': enf.nombre
                                    },
                                    'idSintoma': {
                                        'id': sin.id,
                                        'nombre': sin.nombre
                                    }
                                }
                                detalles_values.append(historico_dict)
                            context = {
                                'message': "Consulta exitosa",
                                'detalles': detalles_values
                            }
                            return JsonResponse(context)
                        else:
                            context = {
                                'message': "No se encontraron los datos",
                                'detalles': []
                            }
                            return JsonResponse(context)
                else:
                    context = {
                        'message': "No se encontraron los datos",
                        'detalles': []
                    }
                    return JsonResponse(context)
            context = {
                    'message': "No se encontraron los datos",
                    'detalles': []
                }
            return JsonResponse(context)
        else:
            detalles = EnfermedadDetalle.objects.select_related('idEnfermedad','idSintoma')
            if len(detalles) > 0:
                detalle_values = []
                for detalle in detalles:
                    detalle_dict={
                        'id':detalle.id,
                        'idEnfermedad':{
                        'id':detalle.idEnfermedad.id,
                        'nombre':detalle.idEnfermedad.nombre
                        },
                        'idSintoma':{
                        'id':detalle.idSintoma.id,
                        'nombre':detalle.idSintoma.nombre
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
        detalles = list(EnfermedadDetalle.objects.filter(id=id).values())
        if len(detalles) > 0:
            EnfermedadDetalle.objects.filter(id=id).delete()
            datos = {'message':"Registro Eliminado"}
        else:
            datos = {'message':"No se encontraró el registro", 'detalles': []}
        return JsonResponse(datos)
    