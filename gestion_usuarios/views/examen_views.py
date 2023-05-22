import datetime
from django.http.response import JsonResponse
from django.views import View
from datetime import date, datetime, time
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
import re
from ..models import *
from django.views.decorators.http import require_http_methods

@method_decorator(require_http_methods(['POST','PUT','GET','DELETE']), name='dispatch')
class examenViews(View):
    #Este metodo permite realizar las conultas que necesitan autentificacion. POST PUT DELETE
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    #Busquedas personalizadas y por defecto
    #las personalizadas varian segun el criterio ingresado, y por defecto muestra todos los objetos
    def get(self, request, campo="",criterio=""):
        if (len(campo)> 0 and len(criterio)> 0):
            if criterio == "id":
                examenes = Examen.objects.filter(id=campo).select_related('idMuestra','idTipo','idLaboratorio')
                if examenes is not None:
                    examenes_values = []
                    for examen in examenes:
                        examen_dict = {
                            'id': examen.id,
                            'fecha': formato_fecha(examen.fecha),
                            'fechaProgramada': formato_fecha(examen.fechaProgramada),
                            'observacion': examen.observacion,
                            'idMuestra':{
                                'id':examen.idMuestra.id,
                                'idPaciente': {
                                'id': examen.idMuestra.idPaciente.id,
                                'nombre': examen.idMuestra.idPaciente.nombre +" "+ examen.idMuestra.idPaciente.apellido,
                                'documento': examen.idMuestra.idPaciente.documento,                              
                                }        
                            },   
                            'idTipo': {
                            'id': examen.idTipo.id,
                            'tipo':examen.idMuestra.idTipoMuestra.nombre,
                            'nombre': examen.idTipo.nombre,
                            'subtipo': examen.idTipo.idsubtipo.nombre,
                            'impuesto':examen.idTipo.idImpuesto.valor,
                            'precio': examen.idTipo.precio
                            
                            },
                            'idLaboratorio': {
                                'id': examen.idLaboratorio.id,
                                'nombre': examen.idLaboratorio.nombre,
                            }    
                        } 
                        examenes_values.append(examen_dict)
                    context = {
                        'message': "Consulta exitosa",
                        'examenes': examenes_values
                    }
                    return JsonResponse(context)
                else:
                    context = {
                        'message': "No se encontraron los datos",
                        'examenes': []
                    }
                    return JsonResponse(context)  
            elif criterio == "documento":
                examenes = Examen.objects.filter(idMuestra__idPaciente__documento=campo)
                if examenes is not None:
                    examenes_values = []
                    for examen in examenes:
                        examen_dict = {
                            'id': examen.id,
                            'fecha': formato_fecha(examen.fecha),
                            'fechaProgramada': formato_fecha(examen.fechaProgramada),
                            'observacion': examen.observacion,
                            'idMuestra':{
                                'id':examen.idMuestra.id,
                                'tipo':examen.idMuestra.idTipoMuestra.nombre,
                                'idPaciente': {
                                'id': examen.idMuestra.idPaciente.id,
                                'nombre': examen.idMuestra.idPaciente.nombre +" "+ examen.idMuestra.idPaciente.apellido,
                                'documento': examen.idMuestra.idPaciente.documento,                              
                                }        
                            },   
                            'idTipo': {
                            'id': examen.idTipo.id,
                            'nombre': examen.idTipo.nombre,
                            'subtipo': examen.idTipo.idsubtipo.nombre,
                            'impuesto':examen.idTipo.idImpuesto.valor,
                            'precio': examen.idTipo.precio
                            
                            },
                            'idLaboratorio': {
                                'id': examen.idLaboratorio.id,
                                'nombre': examen.idLaboratorio.nombre,
                            }     
                        }                       
                        examenes_values.append(examen_dict)
                    context = {
                        'message': "Consulta exitosa",
                        'examenes': examenes_values
                    }
                    return JsonResponse(context)
                else:
                    context = {
                        'message': "No se encontraron los datos",
                        'examenes': []
                    }
                    return JsonResponse(context)     
            elif criterio == "nombre":
                examenes = Examen.objects.filter(idMuestra__idPaciente__nombre=campo)
                if examenes is not None:
                    examenes_values = []
                    for examen in examenes:
                        examen_dict = {
                            'id': examen.id,
                            'fecha': formato_fecha(examen.fecha),
                            'fechaProgramada': formato_fecha(examen.fechaProgramada),
                            'observacion': examen.observacion,
                            'idMuestra':{
                                'id':examen.idMuestra.id,
                                'tipo':examen.idMuestra.idTipoMuestra.nombre,
                                'idPaciente': {
                                'id': examen.idMuestra.idPaciente.id,
                                'nombre': examen.idMuestra.idPaciente.nombre +" "+ examen.idMuestra.idPaciente.apellido,
                                'documento': examen.idMuestra.idPaciente.documento,                              
                                }        
                            },   
                            'idTipo': {
                            'id': examen.idTipo.id,
                            'nombre': examen.idTipo.nombre,
                            'subtipo': examen.idTipo.idsubtipo.nombre,
                            'impuesto':examen.idTipo.idImpuesto.valor,
                            'precio': examen.idTipo.precio
                            
                            },
                            'idLaboratorio': {
                                'id': examen.idLaboratorio.id,
                                'nombre': examen.idLaboratorio.nombre,
                            }     
                        }                       
                        examenes_values.append(examen_dict)
                    context = {
                        'message': "Consulta exitosa",
                        'examenes': examenes_values
                    }
                    return JsonResponse(context)
                else:
                    context = {
                        'message': "No se encontraron los datos",
                        'examenes': []
                    }
                    return JsonResponse(context)     
        else:                
            examenes = Examen.objects.select_related('idMuestra','idTipo','idLaboratorio')
            if examenes is not None:
                examenes_values = []
                for examen in examenes:
                    examen_dict = {
                            'id': examen.id,
                            'fecha': formato_fecha(examen.fecha),
                            'fechaProgramada': formato_fecha(examen.fechaProgramada),
                            'observacion': examen.observacion,
                            'idMuestra':{
                                'id':examen.idMuestra.id,
                                'idPaciente': {
                                'id': examen.idMuestra.idPaciente.id,
                                'nombre': examen.idMuestra.idPaciente.nombre +" "+ examen.idMuestra.idPaciente.apellido,
                                'documento': examen.idMuestra.idPaciente.documento,                              
                                }        
                            },   
                            'idTipo': {
                            'id': examen.idTipo.id,
                            'nombre': examen.idTipo.nombre,
                            'subtipo': examen.idTipo.idsubtipo.nombre,
                            'impuesto':examen.idTipo.idImpuesto.valor,
                            'precio': examen.idTipo.precio
                            
                            },
                            'idLaboratorio': {
                                'id': examen.idLaboratorio.id,
                                'nombre': examen.idLaboratorio.nombre,
                            }     
                        }           
                    examenes_values.append(examen_dict)
                context = {
                    'message': "Consulta exitosa",
                    'examenes': examenes_values
                }
                return JsonResponse(context)
            else:
                context = {
                    'message': "No se encontraron los datos",
                    'examenes': []
                }
                return JsonResponse(context)

#Agregar un registro de tipo
    def post(self, request):
        
        jd=json.loads(request.body)
        rsp_fechaProgramada = datetime.fromisoformat(jd['fechaProgramada'])
        if validar_id_muestra(jd['idMuestra']):    
            examenes = {'message': "La muestra no existe"}
        elif validar_id_tipo(jd['idTipo']):    
            examenes = {'message': "El tipo no existe"}
        elif validar_id_laboratorio(jd['idLaboratorio']):    
            examenes = {'message': "El laboratorio no existe"}

        elif (rsp_fechaProgramada) is None:
            examenes = {'message': "La fecha programada esta vacía"}
        elif isinstance(rsp_fechaProgramada, str):
            examenes = {'message': "La fecha programada esta vacía"}
        elif (rsp_fechaProgramada.year) < 2000:
            examenes = {'message': "La fecha programada debe estar en el rango de año de 2000 a 2030"}
        elif (rsp_fechaProgramada.year) > 2030:
            examenes = {'message': "La fecha programada debe estar en el rango de año de 2000 a 2030"}
        elif (rsp_fechaProgramada) <= datetime.today():
            examenes = {'message': "La fecha programada debe ser mayor a la fecha de registro"}       
        elif validar_fecha_programada_repetida(rsp_fechaProgramada):
            examenes = {'message': "Ya hay una cita programada en la misma fecha"}

        elif len(jd['observacion']) <= 0:
            examenes = {'message': "La observación esta vacía."}
        elif len(jd['observacion']) < 5:
            examenes = {'message': "La observación debe tener más de 5 caracteres."}
        elif len(jd['observacion']) > 50:
            examenes = {'message': "La observación debe tener menos de 50 caracteres."}
        elif not validar_cadena_espacios(jd['observacion']):
            examenes = {'message': "No se permiten mas de un espacio consecutivo.[observacion]"}
        elif validar_cadena_repeticion(jd['observacion']):
            examenes = {'message': "No se permiten mas de dos caracteres consecutivos del mismo tipo.[observacion]"} 
        else:
            examenes = {'message': "Registro Exitoso."}
            Examen.objects.create(idMuestra=instanciar_muestra(jd['idMuestra']),
                                  idTipo=instanciar_tipo(jd['idTipo']),
                                  idLaboratorio=instanciar_laboratorio(jd['idLaboratorio']),
                                  fechaProgramada=jd['fechaProgramada'],
                                  observacion=jd['observacion'])
            examenes = {'message':"Registro Exitoso."}
        return JsonResponse(examenes)

#Actualizar un registro de tipo
    def put(self, request,id):
        jd=json.loads(request.body)
        examenes = list(Examen.objects.filter(id=id).values())
        if len(examenes) > 0:
            rsp_fechaProgramada = datetime.fromisoformat(jd['fechaProgramada'])
            examen=Examen.objects.get(id=id)           
        if validar_id_muestra(jd['idMuestra']):    
            examenes = {'message': "La muestra no existe"}
        elif validar_id_tipo(jd['idTipo']):    
            examenes = {'message': "El tipo no existe"}
        elif validar_id_laboratorio(jd['idLaboratorio']):    
            examenes = {'message': "El laboratorio no existe"}
        elif (rsp_fechaProgramada) is None:
            examenes = {'message': "La fecha programada esta vacía"}
        elif isinstance(rsp_fechaProgramada, str):
            examenes = {'message': "La fecha programada esta vacía"}
        elif (rsp_fechaProgramada.year) < 2000:
            examenes = {'message': "La fecha programada debe estar en el rango de año de 2000 a 2030"}
        elif (rsp_fechaProgramada.year) > 2030:
            examenes = {'message': "La fecha programada debe estar en el rango de año de 2000 a 2030"}
        elif (rsp_fechaProgramada) <= datetime.today():
            examenes = {'message': "La fecha programada debe ser mayor a la fecha de registro"}
        elif validar_fecha_programada_repetida(rsp_fechaProgramada):
            examenes = {'message': "Ya hay una cita programada en la misma fecha"}
        elif len(jd['observacion']) <= 0:
            examenes = {'message': "La observación esta vacía."}
        elif len(jd['observacion']) < 5:
            examenes = {'message': "La observación debe tener más de 5 caracteres."}
        elif len(jd['observacion']) > 50:
            examenes = {'message': "La observación debe tener menos de 50 caracteres."}
        elif not validar_cadena_espacios(jd['observacion']):
            examenes = {'message': "No se permiten mas de un espacio consecutivo.[observacion]"}
        elif validar_cadena_repeticion(jd['observacion']):
            examenes = {'message': "No se permiten mas de dos caracteres consecutivos del mismo tipo.[observacion]"} 
        else:            
            examen.idMuestra = instanciar_muestra(jd['idMuestra'])
            examen.idTipo = instanciar_tipo(jd['idTipo'])
            examen.idLaboratorio = instanciar_laboratorio(jd['idLaboratorio'])
            examen.observacion = jd['observacion']
            examen.fechaProgramada = jd['fechaProgramada']
            examen.save()
            examenes = {'message': "La actualización fue exitosa."}
        return JsonResponse(examenes)
        
        

#Eliminar un registro de cargos
    def delete(self, request,id):
        examenes = list(Examen.objects.filter(id=id).values())
        if len(examenes) > 0:
            Examen.objects.filter(id=id).delete()
            examenes = {'message':"Registro Eliminado"}
        else:
            examenes = {'message':"No se encontró el registro", 'examenes': []}
        return JsonResponse(examenes)

def instanciar_muestra(id):
    id = int(id)
    if (id>0):
        muestra = Muestra.objects.get(id=id)
        if muestra:
            return muestra   

def validar_id_muestra(id):
    id = int(id)
    if (id>0):
        registro = Muestra.objects.filter(id=id)
        if registro:
            return False
        else:
            return True    
   

def instanciar_tipo(id):
    id = int(id)
    if (id>0):
        tipo = Tipo.objects.get(id=id)
        if tipo:
            return tipo   

def validar_id_tipo(id):
    id = int(id)
    if (id>0):
        registro = Tipo.objects.filter(id=id)
        if registro:
            return False
        else:
            return True  
        

def instanciar_laboratorio(id):
    id=int(id)
    if (id>0):
        laboratorio = Laboratorios.objects.get(id=id)
        if laboratorio:
            return laboratorio   

def validar_id_laboratorio(id):
    id=int(id)
    if (id>0):
        registro = Laboratorios.objects.filter(id=id)
        if registro:
            return False
        else:
            return True  

def validar_id_subtipo(id):
    id=int(id)
    if (id>0):
        subtipo = Subtipo.objects.filter(id=id)
        if subtipo:
            return False
        else:
            return True


def validar_fecha_programada_repetida(fecha):
    if (fecha):
        registros = Cita.objects.filter(fechaProgramada=fecha)
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

def formato_fecha(fecha):
    if fecha is not None:
        fecha_formateada = fecha.strftime("%d-%m-%Y %H:%M:%S")
        return fecha_formateada
    else:
        return None