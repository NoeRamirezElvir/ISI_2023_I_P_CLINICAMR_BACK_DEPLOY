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
class TrasladosViews(View):
    #Este metodo permite realizar las conultas que necesitan autentificacion. POST PUT DELETE
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    #Busquedas personalizadas y por defecto
    #las personalizadas varian segun el criterio ingresado, y por defecto tratamiento todos los objetos
    def get(self, request, campo="",criterio=""):
        if (len(campo)> 0 and len(criterio)> 0):
            if criterio == "id":
                traslados = TrasladoPaciente.objects.filter(id=campo).select_related('idPaciente','idAutorizacionPaciente','idEmpleado')
                if traslados is not None:
                    traslados_values = []
                    for traslado in traslados:
                        
                        traslado_dict = {
                            'id': traslado.id,
                            'nombre': traslado.nombre,
                            'direccion':traslado.direccion,
                            'telefono': traslado.telefono,

                            'idPaciente': {
                                'id': traslado.idPaciente.id,
                                'nombre': traslado.idPaciente.nombre,
                                'apellido': traslado.idPaciente.apellido,
                                'documento': traslado.idPaciente.documento
                            },
                            'idAutorizacionPaciente': {
                                'id': traslado.idAutorizacionPaciente.id,
                                'motivos': traslado.idAutorizacionPaciente.motivos
                            },
                            'idEmpleado': {
                                'id': traslado.idEmpleado.id,
                                'nombre': traslado.idEmpleado.nombre
                                
                            }
                        }
                        traslados_values.append(traslado_dict)
                    context = {
                            'message': "Consulta exitosa",
                            'traslados': traslados_values
                        }
                    return JsonResponse(context)
                else:
                    context = {
                        'message': "No se encontraron los datos",
                        'traslados': []
                    }
                    return JsonResponse(context)
                
            elif criterio == "nombre":
                
                traslados = TrasladoPaciente.objects.filter(idPaciente__nombre=campo)
                if traslados is not None:
                    traslados_values = []
                    for traslado in traslados:
                        traslado_dict = {
                           'id': traslado.id,
                            'nombre': traslado.nombre,
                            'direccion':traslado.direccion,
                            'telefono': traslado.telefono,

                            'idPaciente': {
                                'id': traslado.idPaciente.id,
                                'nombre': traslado.idPaciente.nombre,
                                'apellido': traslado.idPaciente.apellido,
                                'documento': traslado.idPaciente.documento
                            },
                            'idAutorizacionPaciente': {
                                'id': traslado.idAutorizacionPaciente.id,
                                'motivos': traslado.idAutorizacionPaciente.motivos
                            },
                            'idEmpleado': {
                                'id': traslado.idEmpleado.id,
                                'nombre': traslado.idEmpleado.nombre
                                
                            }
                        }
                        traslados_values.append(traslado_dict)
                    context = {
                        'message': "Consulta exitosa",
                        'traslados': traslados_values
                    }
                    return JsonResponse(context)
                else:
                    context = {
                        'message': "No se encontraron los datos",
                        'traslados': []
                    }
                    return JsonResponse(context)          
        else:                
            traslados = TrasladoPaciente.objects.select_related('idPaciente')
            if traslados is not None:
                traslados_values = []
                for traslado in traslados:
                    traslado_dict = {
                            'id': traslado.id,
                            'nombre': traslado.nombre,
                            'direccion':traslado.direccion,
                            'telefono': traslado.telefono,

                            'idPaciente': {
                                'id': traslado.idPaciente.id,
                                'nombre': traslado.idPaciente.nombre,
                                'apellido': traslado.idPaciente.apellido,
                                'documento': traslado.idPaciente.documento
                            },
                            'idAutorizacionPaciente': {
                                'id': traslado.idAutorizacionPaciente.id,
                                'motivos': traslado.idAutorizacionPaciente.motivos
                            },
                            'idEmpleado': {
                                'id': traslado.idEmpleado.id,
                                'nombre': traslado.idEmpleado.nombre
                                
                            }
                    }
                    traslados_values.append(traslado_dict)
                context = {
                    'message': "Consulta exitosa",
                    'traslados': traslados_values
                }
                return JsonResponse(context)
            else:
                context = {
                    'message': "No se encontraron los datos",
                    'traslados': []
                }
                return JsonResponse(context)
            
#Agregar un registro de trasaldo
    def post(self, request):
        jd=json.loads(request.body)
        if validar_id_autorizacion(jd['idAutorizacionPaciente']):    
            traslados = {'message': "El tratamiento no existe"}
        if validar_id_paciente(jd['idPaciente']):    
            traslados = {'message': "El paciente no existe"}
        if validar_id_empleado(jd['idEmpleado']):    
            traslados = {'message': "El medico no existe"}
        if len(jd['nombre']) <= 0:
            traslados = {'message': "El nombre esta vacío."}
        elif len(jd['nombre']) < 3:
            traslados = {'message': "El nombre debe tener más de 3 caracteres."}
        elif len(jd['nombre']) > 50:
            traslados = {'message': "El nombre debe tener menos de 50 caracteres."}
        elif validar_cadena_repeticion(jd['nombre']):
            traslados = {'message': "No se permiten mas de dos caracteres consecutivos del mismo tipo."} 
        elif not validar_cadena_espacios(jd['nombre']):
            traslados = {'message': "No se permiten mas de un espacio consecutivo."}
        elif str(jd['telefono']).isalpha():
            traslados = {'message': "El teléfono solo puede contener numeros."}
        elif len(str(jd['telefono'])) <= 0:
            traslados = {'message': "El teléfono esta vacío."}
        elif len(str(jd['telefono'])) < 8:
            traslados = {'message': "El teléfono debe tener más de 8 caracteres."}
        elif len(str(jd['telefono'])) > 8:
            traslados = {'message': "El teléfono debe tener 8 caracteres."}
        elif (str(jd['telefono']))[0] == '1':
            traslados = {'message': "El teléfono debe comenzar con 2, 3, 7, 8, 9."}
        elif (str(jd['telefono']))[0] == '4':
            traslados = {'message': "El teléfono debe comenzar con 2, 3, 7, 8, 9."}
        elif (str(jd['telefono']))[0] == '5':
            traslados = {'message': "El teléfono debe comenzar con 2, 3, 7, 8, 9."}
        elif (str(jd['telefono']))[0] == '6':
            traslados = {'message': "El teléfono debe comenzar con 2, 3, 7, 8, 9."}
        elif (str(jd['telefono']))[0] == '0':
            traslados = {'message': "El teléfono debe comenzar con 2, 3, 7, 8, 9."}
        elif len(jd['direccion']) <= 0:
            traslados = {'message': "La dirección esta vacía."}
        elif len(jd['direccion']) < 5:
            traslados = {'message': "La dirección debe tener más de 5 caracteres."}
        elif len(jd['direccion']) > 50:
            traslados = {'message': "La dirección debe tener menos de 50 caracteres."}
        else:
            traslados = {'message': "Registro Exitoso."}
            TrasladoPaciente.objects.create(idAutorizacionPaciente=instanciar_autorizacion(jd['idAutorizacionPaciente']),
                                            idPaciente=instanciar_paciente(jd['idPaciente']),
                                            idEmpleado=instanciar_empleado(jd['idEmpleado']),
                                            nombre=jd['nombre'],
                                            direccion=jd['direccion'],
                                            telefono=jd['telefono'],
                                            )
                                                                    
            traslados = {'message':"Registro Exitoso."}
        return JsonResponse(traslados)
    

#Actualizar un registro de tipo
    def put(self, request,id):
        jd=json.loads(request.body)
        traslados = list(TrasladoPaciente.objects.filter(id=id).values())
        if len(traslados) > 0:
            
            traslado=TrasladoPaciente.objects.get(id=id)
        if validar_id_autorizacion(jd['idAutorizacionPaciente']):    
            traslados = {'message': "El tratamiento no existe"}
        if validar_id_paciente(jd['idPaciente']):    
            traslados = {'message': "El paciente no existe"}
        if validar_id_empleado(jd['idEmpleado']):    
            traslados = {'message': "El medico no existe"}
        if len(jd['nombre']) <= 0:
            traslados = {'message': "El nombre esta vacío."}
        elif len(jd['nombre']) < 3:
            traslados = {'message': "El nombre debe tener más de 3 caracteres."}
        elif len(jd['nombre']) > 50:
            traslados = {'message': "El nombre debe tener menos de 50 caracteres."}
        elif validar_cadena_repeticion(jd['nombre']):
            traslados = {'message': "No se permiten mas de dos caracteres consecutivos del mismo tipo."} 
        elif not validar_cadena_espacios(jd['nombre']):
            traslados = {'message': "No se permiten mas de un espacio consecutivo."}
        elif str(jd['telefono']).isalpha():
            traslados = {'message': "El teléfono solo puede contener numeros."}
        elif len(str(jd['telefono'])) <= 0:
            traslados = {'message': "El teléfono esta vacío."}
        elif len(str(jd['telefono'])) < 8:
            traslados = {'message': "El teléfono debe tener más de 8 caracteres."}
        elif len(str(jd['telefono'])) > 8:
            traslados = {'message': "El teléfono debe tener 8 caracteres."}
        elif (str(jd['telefono']))[0] == '1':
            traslados = {'message': "El teléfono debe comenzar con 2, 3, 7, 8, 9."}
        elif (str(jd['telefono']))[0] == '4':
            traslados = {'message': "El teléfono debe comenzar con 2, 3, 7, 8, 9."}
        elif (str(jd['telefono']))[0] == '5':
            traslados = {'message': "El teléfono debe comenzar con 2, 3, 7, 8, 9."}
        elif (str(jd['telefono']))[0] == '6':
            traslados = {'message': "El teléfono debe comenzar con 2, 3, 7, 8, 9."}
        elif (str(jd['telefono']))[0] == '0':
            traslados = {'message': "El teléfono debe comenzar con 2, 3, 7, 8, 9."}
        elif len(jd['direccion']) <= 0:
            traslados = {'message': "La dirección esta vacía."}
        elif len(jd['direccion']) < 5:
            traslados = {'message': "La dirección debe tener más de 5 caracteres."}
        elif len(jd['direccion']) > 50:
            traslados = {'message': "La dirección debe tener menos de 50 caracteres."}
        else:
            traslado.idPaciente = instanciar_paciente(jd['idPaciente'])
            traslado.idAutorizacionPaciente = instanciar_autorizacion(jd['idAutorizacionPaciente'])
            traslado.idEmpleado = instanciar_empleado(jd['idEmpleado'])
            traslado.nombre = jd['nombre']
            traslado.telefono = jd['telefono']
            traslado.direccion = jd['direccion']
            traslado.save()
            traslados = {'message': "La actualización fue exitosa."}
        return JsonResponse(traslados)
        
        
#Eliminar un registro de tipo
    def delete(self, request,id):
        traslado = list(TrasladoPaciente.objects.filter(id=id).values())
        if len(traslado) > 0:
            TrasladoPaciente.objects.filter(id=id).delete()
            datos = {'message':"Registro Eliminado"}
        else:
            datos = {'message':"No se encontraró el registro", 'traslado': []}
        return JsonResponse(datos)
    
def instanciar_paciente(id):
    if (id>0):
        paciente = Paciente.objects.get(id=id)
        if paciente:
            return paciente   

def validar_id_paciente(id):
    if (id>0):
        registro = Paciente.objects.filter(id=id)
        if registro:
            return False
        else:
            return True    


def instanciar_autorizacion(id):
    if (id>0):
        autorizacion = AutorizacionPaciente.objects.get(id=id)
        if autorizacion:
            return autorizacion   

def validar_id_autorizacion(id):
    if (id>0):
        registro = AutorizacionPaciente.objects.filter(id=id)
        if registro:
            return False
        else:
            return True 
        

def instanciar_empleado(id):
    if (id>0):
        empleado = Empleado.objects.get(id=id)
        if empleado:
            return empleado   

def validar_id_empleado(id):
    if (id>0):
        registro = Empleado.objects.filter(id=id)
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

