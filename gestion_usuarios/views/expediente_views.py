from datetime import date, datetime
from django.http.response import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
import re
from ..models import *
from django.views.decorators.http import require_http_methods

@method_decorator(require_http_methods(['POST','PUT','GET','DELETE']), name='dispatch')
class ExpedientesViews(View):
    #Este metodo permite realizar las conultas que necesitan autentificacion. POST PUT DELETE
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    #Busquedas personalizadas y por defecto
    #las personalizadas varian segun el criterio ingresado, y por defecto muestra todos los objetos
    def get(self, request, campo="",criterio=""):
        if (len(campo)> 0 and len(criterio)> 0):
            if criterio == "id":
                expedientes = Expediente.objects.filter(id=campo).select_related('idPaciente')
                if expedientes is not None:
                    expedientes_values = []
                    for expediente in expedientes:
                        expediente_dict = {
                            'id': expediente.id,
                            'fecha': formato_fecha(expediente.fecha),
                            'observacion': expediente.observacion,
                            'activo': expediente.activo,
                                'idPaciente': {
                                    'id': expediente.idPaciente.id,
                                    'nombre': expediente.idPaciente.nombre,
                                    'apellido': expediente.idPaciente.apellido,
                                    'documento': expediente.idPaciente.documento,
                                    'telefono': expediente.idPaciente.telefono
                                },
                            'consultas':{},
                            'tratamientos':{},
                            'examenes':{}
                        }
                        expediente_dict = buscar_paciente_consultas(expediente_dict, expediente.idPaciente.id)
                        expediente_dict = buscar_paciente_tratamientos(expediente_dict, expediente.idPaciente.id)
                        expediente_dict = buscar_paciente_examenes(expediente_dict, expediente.idPaciente.id)
                        expedientes_values.append(expediente_dict)
                    context = {
                        'message': "Consulta exitosa",
                        'expedientes': expedientes_values
                    }
                    return JsonResponse(context)
                else:
                    context = {
                        'message': "No se encontraron los datos",
                        'expedientes': []
                    }
                    return JsonResponse(context)
                
                
            elif criterio == "documento":
                expedientes = Expediente.objects.filter(idPaciente__documento=campo)
                if expedientes is not None:
                    expedientes_values = []
                    for expediente in expedientes:
                        expediente_dict = {
                            'id': expediente.id,
                            'fecha': formato_fecha(expediente.fecha),
                            'observacion': expediente.observacion,
                            'activo': expediente.activo,       
                                'idPaciente': {
                                'id': expediente.idPaciente.id,
                                'nombre': expediente.idPaciente.nombre,
                                'apellido': expediente.idPaciente.apellido,
                                'documento': expediente.idPaciente.documento,
                                'telefono': expediente.idPaciente.telefono
                            },
                            'consultas':{},
                            'tratamientos':{},
                            'examenes':{}
                        }
                        expediente_dict = buscar_paciente_consultas(expediente_dict, expediente.idPaciente.id)
                        expediente_dict = buscar_paciente_tratamientos(expediente_dict, expediente.idPaciente.id)
                        expediente_dict = buscar_paciente_examenes(expediente_dict, expediente.idPaciente.id)
                        expedientes_values.append(expediente_dict)
                    context = {
                        'message': "Consulta exitosa",
                        'expedientes': expedientes_values
                    }
                    return JsonResponse(context)
                else:
                    context = {
                        'message': "No se encontraron los datos",
                        'expedientes': []
                    }
                    return JsonResponse(context)          
        else:                
            expedientes = Expediente.objects.select_related('idPaciente')
            if expedientes is not None:
                expedientes_values = []
                for expediente in expedientes:
                    expediente_dict = {
                        'id': expediente.id,
                        'fecha': formato_fecha(expediente.fecha),
                        'observacion': expediente.observacion,
                        'activo': expediente.activo,
                            'idPaciente': {
                            'id': expediente.idPaciente.id,
                            'nombre': expediente.idPaciente.nombre,
                            'apellido': expediente.idPaciente.apellido,
                            'documento': expediente.idPaciente.documento,
                            'telefono': expediente.idPaciente.telefono
                        },
                        'consultas':{},
                        'tratamientos':{},
                        'examenes':{}
                    }
                    expediente_dict = buscar_paciente_consultas(expediente_dict, expediente.idPaciente.id)
                    expediente_dict = buscar_paciente_tratamientos(expediente_dict, expediente.idPaciente.id)
                    expediente_dict = buscar_paciente_examenes(expediente_dict, expediente.idPaciente.id)
                    expedientes_values.append(expediente_dict)
                context = {
                    'message': "Consulta exitosa",
                    'expedientes': expedientes_values
                }
                return JsonResponse(context)
            else:
                context = {
                    'message': "No se encontraron los datos",
                    'expedientes': []
                }
                return JsonResponse(context)

#Agregar un registro de tipo
    def post(self, request):
        jd=json.loads(request.body)
        if Expediente.objects.filter(idPaciente=jd['idPaciente']).exists():    
            expedientes = {'message': "El expediente ya existe"}
        elif validar_id_paciente(jd['idPaciente']):    
            expedientes = {'message': "El paciente no existe"}
        elif len(jd['observacion']) <= 0:
            expedientes = {'message': "La observación esta vacía."}
        elif len(jd['observacion']) < 5:
            expedientes = {'message': "La observación debe tener más de 5 caracteres."}
        elif len(jd['observacion']) > 50:
            expedientes = {'message': "La observación debe tener menos de 50 caracteres."}
        elif not validar_cadena_espacios(jd['observacion']):
            expedientes = {'message': "No se permiten mas de un espacio consecutivo.[observacion]"}
        elif validar_cadena_repeticion(jd['observacion']):
            expedientes = {'message': "No se permiten mas de dos caracteres consecutivos del mismo tipo.[observacion]"} 
        elif jd['activo'] < 0:
            expedientes = {'message': "Activo debe ser positivo."}
        elif jd['activo'] > 1:
            expedientes = {'message': "Activo debe unicamente puede ser 0 o 1."}
        else:
            Expediente.objects.create(idPaciente=instanciar_paciente(jd['idPaciente']),fecha=date.today(),observacion=jd['observacion'],activo=jd['activo'])
            expedientes = {'message':"Registro Exitoso."}
        return JsonResponse(expedientes)

#Actualizar un registro de tipo
    def put(self, request,id):
        jd=json.loads(request.body)
        expedientes = list(Expediente.objects.filter(id=id).values())
        if len(expedientes) > 0:
            expediente=Expediente.objects.get(id=id)
            if validar_id_paciente(jd['idPaciente']):    
                expedientes = {'message': "El paciente no existe"}
            elif len(jd['observacion']) <= 0:
                expedientes = {'message': "La observación esta vacía."}
            elif len(jd['observacion']) < 5:
                expedientes = {'message': "La observación debe tener más de 5 caracteres."}
            elif len(jd['observacion']) > 50:
                expedientes = {'message': "La observación debe tener menos de 50 caracteres."}
            elif not validar_cadena_espacios(jd['observacion']):
                expedientes = {'message': "No se permiten mas de un espacio consecutivo.[direccion]"}
            elif validar_cadena_repeticion(jd['observacion']):
                expedientes = {'message': "No se permiten mas de dos caracteres consecutivos del mismo tipo.[direccion]"} 
            elif jd['activo'] < 0:
                expedientes = {'message': "Activo debe ser positivo."}
            elif jd['activo'] > 1:
                expedientes = {'message': "Activo debe unicamente puede ser 0 o 1."}
            else:  
                expediente.idPaciente = instanciar_paciente(jd['idPaciente'])
                expediente.observacion = jd['observacion']
                expediente.activo = jd['activo']
                expediente.save()
                expedientes = {'message': "La actualización fue exitosa."}
        return JsonResponse(expedientes)
        
        

#Eliminar un registro de cargos
    def delete(self, request,id):
        expedientes = list(Expediente.objects.filter(id=id).values())
        if len(expedientes) > 0:
            Expediente.objects.filter(id=id).delete()
            expedientes = {'message':"Registro Eliminado"}
        else:
            expedientes = {'message':"No se encontró el registro", 'expedientes': []}
        return JsonResponse(expedientes)
    

def validar_id_paciente(id):
    if (id>0):
        registro = Paciente.objects.filter(id=id)
        if registro:
            return False
        else:
            return True  

def instanciar_paciente(id):
    if (id>0):
        paciente = Paciente.objects.get(id=id)
        if paciente:
            return paciente   

def buscar_paciente_consultas(diccionario, id):
    registros = Consulta.objects.filter(idCita__idPaciente__id=id)
    if registros:
        for registro in registros:
            diagnostico_dict = {
                'id': registro.id,
                'informacionAdicional': registro.informacionAdicional
            }
            diccionario['consultas'][registro.id] = diagnostico_dict
        return diccionario
    else:
        return diccionario

def buscar_paciente_tratamientos(diccionario, id):
    registros = Tratamiento.objects.filter(idPaciente__id=id).select_related("idTipo")
    if registros:
        for registro in registros:
            diagnostico_dict = {
                'id': registro.id,
                'nombre': registro.idTipo.nombre,
                'estado': registro.estado
            }
            diccionario['tratamientos'][registro.id] = diagnostico_dict
        return diccionario
    else:
        return diccionario    

def buscar_paciente_examenes(diccionario, id):
    registros = Examen.objects.filter(idMuestra__idPaciente__id=id).select_related("idTipo")
    if registros:
        for registro in registros:
            diagnostico_dict = {
                'id': registro.id,
                'nombre': registro.idTipo.nombre,
                'observacion': registro.observacion
            }
            diccionario['examenes'][registro.id] = diagnostico_dict
        return diccionario
    else:
        return diccionario 


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