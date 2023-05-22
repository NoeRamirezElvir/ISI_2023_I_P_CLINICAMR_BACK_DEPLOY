from django.http.response import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
import re
from ..models import *
from django.views.decorators.http import require_http_methods

@method_decorator(require_http_methods(['POST','PUT','GET','DELETE']), name='dispatch')
class ConsultaDetallesViews(View):
    #Este metodo permite realizar las conultas que necesitan autentificacion. POST PUT DELETE
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    #Busquedas personalizadas y por defecto
    #las personalizadas varian segun el criterio ingresado, y por defecto muestra todos los objetos
    def get(self, request, campo="",criterio=""):
        if (len(campo)> 0 and len(criterio)> 0):
            if criterio == "id":
                detalles = ConsultaDetalle.objects.filter(id=campo).select_related('idConsulta','idDiagnostico')
                if len(detalles) > 0:
                    detalle_values = []
                    for detalle in detalles:
                        detalle_dict={
                            'id':detalle.id,
                            'idConsulta':{
                            'id':detalle.idConsulta.id,
                            'paciente':detalle.idConsulta.idCita.idPaciente.documento
                            },
                            'idDiagnostico':{
                            'id':detalle.idDiagnostico.id,
                            'descripcion':detalle.idDiagnostico.descripcion,
                                'idEnfermedades':{}
                            }
                        }
                        enfermedades = DiagnosticoDetalle.objects.filter(idDiagnostico = detalle.idDiagnostico.id).select_related('idEnfermedad')
                        for enfermedad in enfermedades:
                            enfermedad_dict = {
                                'id': enfermedad.idEnfermedad.id,
                                'nombre': enfermedad.idEnfermedad.nombre
                            }
                            detalle_dict['idDiagnostico']['idEnfermedades'][enfermedad.idEnfermedad.id] = enfermedad_dict
                        detalle_values.append(detalle_dict)
                    context = {'message': "Consulta exitosa", 'detalles': detalle_values}
                    return JsonResponse(context)
                else:
                    context = {'message': "No se encontraron los datos", 'detalles': []} 
                    return JsonResponse(context)
            elif criterio == "documento":
                    detalles = ConsultaDetalle.objects.filter(idConsulta__idCita__idPaciente__documento=campo).select_related('idConsulta','idDiagnostico')
                    if detalles is not None:
                        detalles_values = []
                        for detalle in detalles:
                            detalle_dict={
                                'id':detalle.id,
                                'idConsulta':{
                                'id':detalle.idConsulta.id,
                                'paciente':detalle.idConsulta.idCita.idPaciente.documento
                                },
                                'idDiagnostico':{
                                'id':detalle.idDiagnostico.id,
                                'descripcion':detalle.idDiagnostico.descripcion,
                                    'idEnfermedades':{}
                                }
                            }
                            enfermedades = DiagnosticoDetalle.objects.filter(idDiagnostico = detalle.idDiagnostico.id).select_related('idEnfermedad')
                            for enfermedad in enfermedades:
                                enfermedad_dict = {
                                    'id': enfermedad.idEnfermedad.id,
                                    'nombre': enfermedad.idEnfermedad.nombre
                                }
                                detalle_dict['idDiagnostico']['idEnfermedades'][enfermedad.idEnfermedad.id] = enfermedad_dict
                            detalles_values.append(detalle_dict)
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
            detalles = ConsultaDetalle.objects.select_related('idConsulta','idDiagnostico')
            if len(detalles) > 0:
                detalle_values = []
                for detalle in detalles:
                    detalle_dict={
                        'id':detalle.id,
                        'idConsulta':{
                        'id':detalle.idConsulta.id,
                        'paciente':detalle.idConsulta.idCita.idPaciente.documento
                        },
                        'idDiagnostico':{
                            'id':detalle.idDiagnostico.id,
                            'descripcion':detalle.idDiagnostico.descripcion,
                            'idEnfermedades':{}
                        }
                    }
                    enfermedades = DiagnosticoDetalle.objects.filter(idDiagnostico = detalle.idDiagnostico.id).select_related('idEnfermedad')
                    for enfermedad in enfermedades:
                        enfermedad_dict = {
                            'id': enfermedad.idEnfermedad.id,
                            'nombre': enfermedad.idEnfermedad.nombre
                        }
                        detalle_dict['idDiagnostico']['idEnfermedades'][enfermedad.idEnfermedad.id] = enfermedad_dict
                    detalle_values.append(detalle_dict)
                context = {'message': "Consulta exitosa", 'detalles': detalle_values}
                return JsonResponse(context)
            else:
                context = {'message': "No se encontraron los datos", 'detalles': []} 
                return JsonResponse(context)
    
        
#Eliminar un registro de cargos
    def delete(self, request,id):
        detalles = list(ConsultaDetalle.objects.filter(id=id).values())
        if len(detalles) > 0:
            ConsultaDetalle.objects.filter(id=id).delete()
            datos = {'message':"Registro Eliminado"}
        else:
            datos = {'message':"No se encontraró el registro", 'detalles': []}
        return JsonResponse(datos)

