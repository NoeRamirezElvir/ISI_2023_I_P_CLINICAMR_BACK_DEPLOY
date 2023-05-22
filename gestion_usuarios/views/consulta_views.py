import datetime
from django.http.response import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
import re
from ..models import *
from django.views.decorators.http import require_http_methods

@method_decorator(require_http_methods(['POST','PUT','GET','DELETE']), name='dispatch')
class ConsultaViews(View):
    #Este metodo permite realizar las conultas que necesitan autentificacion. POST PUT DELETE
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    #Busquedas personalizadas y por defecto
    #las personalizadas varian segun el criterio ingresado, y por defecto muestra todos los objetos
    def get(self, request, campo="",criterio=""):
        if (len(campo)> 0 and len(criterio)> 0):
            if criterio == "id":
                consultas = Consulta.objects.filter(id=campo).select_related('idCita','idTipo')
                if consultas is not None:
                    consultas_values = []
                    for consulta in consultas:
                        consulta_dict = {
                            'id': consulta.id,
                            'fecha': formato_fecha(consulta.fecha),
                            'recomendaciones': consulta.recomendaciones,
                            'informacionAdicional': consulta.informacionAdicional,
                            'idCita':{
                                'id':consulta.idCita.id,
                                'idPaciente': {
                                    'id': consulta.idCita.idPaciente.id,
                                    'nombre': consulta.idCita.idPaciente.nombre,
                                    'documento': consulta.idCita.idPaciente.documento,
                                    'id': consulta.idCita.id,
                                    'fechaProgramada': formato_fecha(consulta.idCita.fechaProgramada),
                                    'fechaMaxima': formato_fecha(consulta.idCita.fechaMaxima)
                                }
                            },
                            'idTipo':{
                                'id':consulta.idTipo.id,
                                'nombre':consulta.idTipo.nombre,
                                'precio':consulta.idTipo.precio,
                                'impuesto':consulta.idTipo.idImpuesto.valor,
                                'subtipo':consulta.idTipo.idsubtipo.nombre
                            },
                            'idDiagnostico':{}                        
                        }
                        diagnosticos = ConsultaDetalle.objects.filter(idConsulta=consulta.id).select_related('idDiagnostico')
                        for diagnostico in diagnosticos:
                                diagnostico_dict = {
                                    'id': diagnostico.idDiagnostico.id,
                                    'descripcion': diagnostico.idDiagnostico.descripcion
                                }
                                consulta_dict['idDiagnostico'][diagnostico.idDiagnostico.id] = diagnostico_dict
                        consultas_values.append(consulta_dict)
                    context = {
                        'message': "Consulta exitosa",
                        'consultas': consultas_values
                    }
                    return JsonResponse(context)
                else:
                    context = {
                        'message': "No se encontraron los datos",
                        'consultas': []
                    }
                    return JsonResponse(context) 
            elif criterio == "documento":
                consultas = Consulta.objects.filter(idCita__idPaciente__documento=campo)
                if consultas is not None:
                    consultas_values = []
                    for consulta in consultas:
                        consulta_dict = {
                            'id': consulta.id,
                            'fecha': formato_fecha(consulta.fecha),
                            'recomendaciones': consulta.recomendaciones,
                            'informacionAdicional': consulta.informacionAdicional,
                            'idCita':{
                                'id':consulta.idCita.id,
                                'idPaciente': {
                                    'id': consulta.idCita.idPaciente.id,
                                    'nombre': consulta.idCita.idPaciente.nombre,
                                    'documento': consulta.idCita.idPaciente.documento,
                                    'id': consulta.idCita.id,
                                    'fechaProgramada': formato_fecha(consulta.idCita.fechaProgramada),
                                    'fechaMaxima': formato_fecha(consulta.idCita.fechaMaxima)
                                }
                            },
                            'idTipo':{
                                'id':consulta.idTipo.id,
                                'nombre':consulta.idTipo.nombre,
                                'precio':consulta.idTipo.precio,
                                'impuesto':consulta.idTipo.idImpuesto.valor,
                                'subtipo':consulta.idTipo.idsubtipo.nombre
                            },
                            'idDiagnostico':{}                        
                        }
                        diagnosticos = ConsultaDetalle.objects.filter(idConsulta=consulta.id).select_related('idDiagnostico')
                        for diagnostico in diagnosticos:
                                diagnostico_dict = {
                                    'id': diagnostico.idDiagnostico.id,
                                    'descripcion': diagnostico.idDiagnostico.descripcion
                                }
                                consulta_dict['idDiagnostico'][diagnostico.idDiagnostico.id] = diagnostico_dict
                        consultas_values.append(consulta_dict)
                    context = {
                        'message': "Consulta exitosa",
                        'consultas': consultas_values
                    }
                    return JsonResponse(context)
                else:
                    context = {
                        'message': "No se encontraron los datos",
                        'consultas': []
                    }
                    return JsonResponse(context)          
        else:                
            consultas = Consulta.objects.select_related('idCita','idTipo')
            if consultas is not None:
                consultas_values = []
                for consulta in consultas:
                    consulta_dict = {
                        'id': consulta.id,
                        'fecha': formato_fecha(consulta.fecha),
                        'recomendaciones': consulta.recomendaciones,
                        'informacionAdicional': consulta.informacionAdicional,
                        'idCita':{
                            'id':consulta.idCita.id,
                            'idPaciente': {
                                'id': consulta.idCita.idPaciente.id,
                                'nombre': consulta.idCita.idPaciente.nombre,
                                'documento': consulta.idCita.idPaciente.documento,
                                'id': consulta.idCita.id,
                                'fechaProgramada': formato_fecha(consulta.idCita.fechaProgramada),
                                'fechaMaxima': formato_fecha(consulta.idCita.fechaMaxima)
                            }
                        },
                        'idTipo':{
                            'id':consulta.idTipo.id,
                            'nombre':consulta.idTipo.nombre,
                            'precio':consulta.idTipo.precio,
                            'impuesto':consulta.idTipo.idImpuesto.valor,
                            'subtipo':consulta.idTipo.idsubtipo.nombre
                        },
                        'idDiagnostico':{}                        
                    }
                    diagnosticos = ConsultaDetalle.objects.filter(idConsulta=consulta.id).select_related('idDiagnostico')
                    for diagnostico in diagnosticos:
                            diagnostico_dict = {
                                'id': diagnostico.idDiagnostico.id,
                                'descripcion': diagnostico.idDiagnostico.descripcion
                            }
                            consulta_dict['idDiagnostico'][diagnostico.idDiagnostico.id] = diagnostico_dict
                    consultas_values.append(consulta_dict)
                context = {
                    'message': "Consulta exitosa",
                    'consultas': consultas_values
                }
                return JsonResponse(context)
            else:
                context = {
                    'message': "No se encontraron los datos",
                    'consultas': []
                }
                return JsonResponse(context)

#Agregar un registro de tipo
    def post(self, request):
        jd=json.loads(request.body)

        if validar_id_cita(jd['idCita']):    
            consultas = {'message': "La ci no existe"}
        elif validar_id_tipo(jd['idCita']):    
            consultas = {'message': "El tipo no existe"}
        elif len(jd['recomendaciones']) <= 0:
            consultas = {'message': "Las recomendaciones estan vacías"}
        elif len(jd['recomendaciones']) < 4:
            consultas = {'message': "Las recomendaciones deben tener mas de 4 caracteres"}
        elif len(jd['recomendaciones']) > 100:
            consultas = {'message': "Las recomendaciones deben tener menos de 100 caracteres"}
        elif not validar_cadena_espacios(jd['recomendaciones']):
            consultas = {'message': "No se permiten mas de un espacio consecutivo.[recomendaciones]"}
        elif validar_cadena_repeticion(jd['recomendaciones']):
            consultas = {'message': "No se permiten mas de dos caracteres consecutivo del mismo tipo.[recomendaciones]"}
        elif len(jd['informacionAdicional']) < 4:
            consultas = {'message': "La información adicional debe tener mas de 4 caracteres"}
        elif len(jd['informacionAdicional']) > 100:
            consultas = {'message': "Las información adicional debe tener menos de 100 caracteres"}
        elif not validar_cadena_espacios(jd['informacionAdicional']):
            consultas = {'message': "No se permiten mas de un espacio consecutivo.[informaicon adicional]"}
        elif validar_cadena_repeticion(jd['informacionAdicional']):
            consultas = {'message': "No se permiten mas de dos caracteres consecutivo del mismo tipo.[informacion adicional]"}
        elif jd['idDiagnostico'] == [] or len(jd['idDiagnostico']) < 0:
            consultas = {'message': "No hay diagnosticos relacionados o estan vacíos."}
        else:
            consultas = {'message':"Registro Exitoso."}
            consulta_reg = Consulta.objects.create(idCita=instanciar_cita(int(jd['idCita'])),
                                    idTipo=instanciar_tipo(int(jd['idTipo'])),
                                    fecha=datetime.datetime.now(),
                                    recomendaciones=jd['recomendaciones'],
                                    informacionAdicional=jd['informacionAdicional'])
            if not jd['idDiagnostico'] == [] or jd['idDiagnostico'] == 0:
                for diagnostico in jd['idDiagnostico']:
                    id_diagnostico = instanciar_diagnostico(int(diagnostico['id']))
                    ConsultaDetalle.objects.create(idConsulta=consulta_reg,idDiagnostico=id_diagnostico) 
        return JsonResponse(consultas)

#Actualizar un registro de tipo
    def put(self, request,id):
        jd=json.loads(request.body)
        consultas = list(Consulta.objects.filter(id=id).values())
        if len(consultas) > 0:
            consulta=Consulta.objects.get(id=id)           
        if validar_id_cita(jd['idCita']):    
            consultas = {'message': "La ci no existe"}
        elif validar_id_tipo(jd['idCita']):    
            consultas = {'message': "El tipo no existe"}
        elif len(jd['recomendaciones']) <= 0:
            consultas = {'message': "Las recomendaciones estan vacías"}
        elif len(jd['recomendaciones']) < 4:
            consultas = {'message': "Las recomendaciones deben tener mas de 4 caracteres"}
        elif len(jd['recomendaciones']) > 100:
            consultas = {'message': "Las recomendaciones deben tener menos de 100 caracteres"}
        elif not validar_cadena_espacios(jd['recomendaciones']):
            consultas = {'message': "No se permiten mas de un espacio consecutivo.[recomendaciones]"}
        elif validar_cadena_repeticion(jd['recomendaciones']):
            consultas = {'message': "No se permiten mas de dos caracteres consecutivo del mismo tipo.[recomendaciones]"}
        elif len(jd['informacionAdicional']) < 4:
            consultas = {'message': "La información adicional debe tener mas de 4 caracteres"}
        elif len(jd['informacionAdicional']) > 100:
            consultas = {'message': "Las información adicional debe tener menos de 100 caracteres"}
        elif not validar_cadena_espacios(jd['informacionAdicional']):
            consultas = {'message': "No se permiten mas de un espacio consecutivo.[informaicon adicional]"}
        elif validar_cadena_repeticion(jd['informacionAdicional']):
            consultas = {'message': "No se permiten mas de dos caracteres consecutivo del mismo tipo.[informacion adicional]"}
        elif jd['idDiagnostico'] == [] or len(jd['idDiagnostico']) < 0:
            consultas = {'message': "No hay diagnosticos relacionados o estan vacíos."}
        else:
            diagnosticos = ConsultaDetalle.objects.filter(idConsulta=id).values('idDiagnostico')
            ids_diagnosticos = [{'id': diagnostico['idDiagnostico']} for diagnostico in diagnosticos]
            ids_actualizar = [{'id': diagnostico['id']} for diagnostico in jd['idDiagnostico']]

            # obtener los IDs que están en idSintomas pero no en ids_lista
            ids_faltantes = [diagnostico['id'] for diagnostico in ids_actualizar if diagnostico not in ids_diagnosticos]

            # obtener los IDs que están en ids_lista pero no en idSintomas
            ids_extra = [diagnostico['id'] for diagnostico in ids_diagnosticos if diagnostico not in ids_actualizar]

            # verificar si la lista de IDs faltantes no está vacía
            if len(ids_faltantes) > 0:
                # imprimir un mensaje para cada ID faltante
                for id_faltante in ids_faltantes:
                    #Crea un detalle por cada id que no se encuentre en la lista de detalles pero si en la nueva lista
                    ConsultaDetalle.objects.create(idConsulta=consulta, idDiagnostico=instanciar_diagnostico(id_faltante))
            # verificar si la lista de IDs extra no está vacía
            if len(ids_extra) > 0:
                # imprimir un mensaje para cada ID extra
                for id_extra in ids_extra:
                    #Borra los detalles que se encuentran en la lista de detalles pero que no estan en la nueva lista
                    reg_del = ConsultaDetalle.objects.filter(idConsulta=consulta, idDiagnostico=instanciar_diagnostico(id_extra))
                    reg_del.delete()
            #Actualizar informacion de la consulta
            consulta.idCita = instanciar_cita(int(jd['idCita']))
            consulta.idTipo = instanciar_tipo(int(jd['idTipo']))
            consulta.recomendaciones = jd['recomendaciones']
            consulta.informacionAdicional =jd['informacionAdicional']
            consulta.save()
            consultas = {'message': "La actualización fue exitosa."}
        return JsonResponse(consultas)
        
        

#Eliminar un registro de cargos
    def delete(self, request,id):
        consultas = list(Consulta.objects.filter(id=id).values())
        detalles = list(ConsultaDetalle.objects.filter(idConsulta=id).values())
        if len(detalles) > 0 and len(consultas) > 0:
            #Elimina los detalles
            for detalle in detalles:
                ConsultaDetalle.objects.filter(id=detalle['id']).delete()
            #Elimina la consulta
            Consulta.objects.filter(id=id).delete()
            consultas = {'message':"Registro Eliminado"}
        else:
            consultas = {'message':"No se encontrarón registros", 'consultas': []}
        return JsonResponse(consultas)

def instanciar_diagnostico(id):
    if (id>0):
        cita = Diagnostico.objects.get(id=id)
        if cita:
            return cita   

def instanciar_cita(id):
    if (id>0):
        cita = Cita.objects.get(id=id)
        if cita:
            return cita   

def validar_id_cita(id):
    if (id>0):
        registro = Cita.objects.filter(id=id)
        if registro:
            return False
        else:
            return True  

def instanciar_tipo(id):
    if (id>0):
        cita = Tipo.objects.get(id=id)
        if cita:
            return cita   

def validar_id_tipo(id):
    if (id>0):
        registro = Tipo.objects.filter(id=id)
        if registro:
            return False
        else:
            return True    

def validar_cadena_repeticion(cadena):
    patron = r'([a-zA-Z])\1\1'
    return bool(re.search(patron, cadena))

def validar_cadena_espacios(cadena):
    patron = r'^[^ ]+(?: {0,1}[^ ]+)*$'
    return bool(re.match(patron,cadena))

def formato_fecha(fecha):
    if fecha is not None:
        fecha_formateada = fecha.strftime("%d-%m-%Y")
        return fecha_formateada
    else:
        return None