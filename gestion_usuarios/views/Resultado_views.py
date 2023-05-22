
from datetime import datetime
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
class resultadosViews(View):
    #Este metodo permite realizar las conultas que necesitan autentificacion. POST PUT DELETE
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    #Busquedas personalizadas y por defecto
    #las personalizadas varian segun el criterio ingresado, y por defecto muestra todos los objetos
    def get(self, request, campo="",criterio=""):
        if (len(campo)> 0 and len(criterio)> 0):
            if criterio == "id":
                resultados = Resultados.objects.filter(id=campo).select_related('idTratamiento')
                if resultados is not None:
                    resultados_values = []
                    for resultado in resultados:
                        resultado_dict = {
                            'id': resultado.id,
                            'observacion': resultado.observacion,
                            'fecha': formato_fecha(resultado.fecha),

                            'idTratamiento':{
                                'idPaciente': {
                                'id': resultado.idTratamiento.idPaciente.id,
                                'nombre': resultado.idTratamiento.idPaciente.nombre,
                                'documento': resultado.idTratamiento.idPaciente.documento
                                
                                },
                                'idTipo': {
                                'id': resultado.idTratamiento.idTipo.id,
                                'nombre': resultado.idTratamiento.idTipo.nombre
                                }

                            }
                        }
                        resultados_values.append(resultado_dict)
                    context = {
                        'message': "Consulta exitosa",
                        'resultados': resultados_values
                    }
                    return JsonResponse(context)
                else:
                    context = {
                        'message': "No se encontraron los datos",
                        'resultados': []
                    }
                    return JsonResponse(context)
                
                
            elif criterio == "nombre":
                
                resultados = Resultados.objects.filter(idTratamiento__idPaciente__nombre=campo)
                if resultados is not None:
                    resultados_values = []
                    for resultado in resultados:
                        resultado_dict = {
                            'id': resultado.id,
                            'observacion': resultado.observacion,
                            'fecha': formato_fecha(resultado.fecha),

                            'idTratamiento':{
                                'idPaciente': {
                                'id': resultado.idTratamiento.idPaciente.id,
                                'nombre': resultado.idTratamiento.idPaciente.nombre,
                                'documento': resultado.idTratamiento.idPaciente.documento
                                
                                },
                                'idTipo': {
                                'id': resultado.idTratamiento.idTipo.id,
                                'nombre': resultado.idTratamiento.idTipo.nombre
                                }

                            }
                        }
                        resultados_values.append(resultado_dict)
                    context = {
                        'message': "Consulta exitosa",
                        'resultados': resultados_values
                    }
                    return JsonResponse(context)
                else:
                    context = {
                        'message': "No se encontraron los datos",
                        'resultados': []
                    }
                    return JsonResponse(context)          
        else:                
            resultados = Resultados.objects.select_related('idTratamiento')
            if resultados is not None:
                resultados_values = []
                for resultado in resultados:
                    resultado_dict = {
                        'id': resultado.id,
                        'observacion': resultado.observacion,
                        'fecha': formato_fecha(resultado.fecha),

                        'idTratamiento':{
                            'idPaciente': {
                            'id': resultado.idTratamiento.idPaciente.id,
                            'nombre': resultado.idTratamiento.idPaciente.nombre,
                            'documento': resultado.idTratamiento.idPaciente.documento
                            },
                            'idTipo': {
                            'id': resultado.idTratamiento.idTipo.id,
                            'nombre': resultado.idTratamiento.idTipo.nombre
                            }

                        }
                    }
                    resultados_values.append(resultado_dict)
                context = {
                    'message': "Consulta exitosa",
                    'resultados': resultados_values
                }
                return JsonResponse(context)
            else:
                context = {
                    'message': "No se encontraron los datos",
                    'resultados': []
                }
                return JsonResponse(context)

#Agregar un registro de tipo
    def post(self, request):
        jd=json.loads(request.body)
        
        rsp_fecha = datetime.date.fromisoformat(jd['fecha'])
        
        if validar_id_tipo(jd['idTratamiento']):    
            resultados = {'message': "El tratamiento no existe"}
        elif len(jd['observacion']) <= 0:
            resultados = {'message': "La observación esta vacía."}
        elif len(jd['observacion']) < 5:
            resultados = {'message': "La observación debe tener más de 5 caracteres."}
        elif len(jd['observacion']) > 50:
            resultados = {'message': "La observación debe tener menos de 50 caracteres."}
        elif not validar_cadena_espacios(jd['observacion']):
            resultados = {'message': "No se permiten mas de un espacio consecutivo.[observacion]"}
        elif validar_cadena_repeticion(jd['observacion']):
            resultados = {'message': "No se permiten mas de dos caracteres consecutivos del mismo tipo.[observacion]"} 
        
        elif (rsp_fecha) is None:
            resultados = {'message': "La fecha esta vacía"}
        elif (rsp_fecha) < datetime.date.today():
            resultados = {'message': "la fecha actual es incorrecta"}
        elif validar_fecha(jd['fecha']):
            resultados = {'message': "la fecha no puede ser mayor a la actual.[fecha]"}    
        elif validar_fecha_max(jd['fecha']):
            resultados = {'message': "la fecha no puede ser menor a la actual.[fecha]"} 
       
        
        elif isinstance(rsp_fecha, str):
            resultados = {'message': "La fecha esta vacía"}
        elif (rsp_fecha.year) < 2000:
            resultados = {'message': "La fecha debe estar en el rango de año de 2000 a 2030"}
        elif (rsp_fecha.year) > 2030:
            resultados = {'message': "La fecha debe estar en el rango de año de 2000 a 2030"}
        else:
            resultados = {'message': "Registro Exitoso."}
            Resultados.objects.create(idTratamiento=instanciar_tratamiento(jd['idTratamiento']),fecha=jd['fecha'],observacion=jd['observacion'])
            resultados = {'message':"Registro Exitoso."}
        return JsonResponse(resultados)

#Actualizar un registro de tipo
    def put(self, request,id):
        jd=json.loads(request.body)
        resultados = list(Resultados.objects.filter(id=id).values())
        if len(resultados) > 0:
            rsp_fecha = datetime.datetime.fromisoformat(jd['fecha'])
            resultado=Resultados.objects.get(id=id)
            
            if validar_id_tipo(jd['idTratamiento']):    
                resultados = {'message': "El tratamiento no existe"}
            elif len(jd['observacion']) <= 0:
                resultados = {'message': "La observación esta vacía."}
            elif len(jd['observacion']) < 5:
                resultados = {'message': "La observación debe tener más de 5 caracteres."}
            elif len(jd['observacion']) > 50:
                resultados = {'message': "La observación debe tener menos de 50 caracteres."}
            elif not validar_cadena_espacios(jd['observacion']):
                resultados = {'message': "No se permiten mas de un espacio consecutivo.[direccion]"}
            elif validar_cadena_repeticion(jd['observacion']):
                resultados = {'message': "No se permiten mas de dos caracteres consecutivos del mismo tipo.[direccion]"} 
            elif (rsp_fecha) is None:
                resultados = {'message': "La fecha esta vacía"}
            elif isinstance(rsp_fecha, str):
                resultados = {'message': "La fecha esta vacía"}
            elif (rsp_fecha.year) < 2000:
                resultados = {'message': "La fecha debe estar en el rango de año de 2000 a 2030"}
            elif (rsp_fecha.year) > 2030:
                resultados = {'message': "La fecha debe estar en el rango de año de 2000 a 2030"}
            else:
                
                resultado.idTratamiento = instanciar_tratamiento(jd['idTratamiento'])
                resultado.fecha = jd['fecha']
                resultado.observacion = jd['observacion']
                resultado.save()
                resultados = {'message': "La actualización fue exitosa."}
        return JsonResponse(resultados)
        
        

#Eliminar un registro de cargos
    def delete(self, request,id):
        resultados = list(Resultados.objects.filter(id=id).values())
        if len(resultados) > 0:
            Resultados.objects.filter(id=id).delete()
            resultados = {'message':"Registro Eliminado"}
        else:
            resultados = {'message':"No se encontró el registro", 'resultados': []}
        return JsonResponse(resultados)
    
   

def instanciar_tratamiento(id):
    if (id>0):
        paciente = Tratamiento.objects.get(id=id)
        if paciente:
            return paciente   

def validar_id_tipo(id):
    if (id>0):
        registro = Tratamiento.objects.filter(id=id)
        if registro:
            return False
        else:
            return True  

def validar_id_subtipo(id):
    if (id>0):
        subtipo = Subtipo.objects.filter(id=id)
        if subtipo:
            return False
        else:
            return True

def validar_cadena_repeticion(cadena):
    patron = r'([a-zA-Z])\1\1'
    return bool(re.search(patron, cadena))

def validar_cadena_espacios(cadena):
    patron = r'^[^ ]+(?: {0,1}[^ ]+)*$'
    return bool(re.match(patron,cadena))




           
           
 
    
def validar_fecha(fecha):
    
    fecha=datetime.date.fromisoformat(fecha)
    fecha_actual = datetime.date.today()
    fechas= fecha_actual.year - fecha.year
    fechas -=((fecha_actual.month, fecha_actual.day)< (fecha.month,fecha.day))
    
    if fechas > -1:
        return False
    else:
        return True
    
def validar_fecha_max(fecha):
    
    fecha=datetime.date.fromisoformat(fecha)
    fecha_actual = datetime.date.today()
    fechas= fecha_actual.year - fecha.year
    fechas -=((fecha_actual.month, fecha_actual.day)> (fecha.month,fecha.day))
    
    if fechas > -1:
        return False
    else:
        return True
    

def formato_fecha(fecha):
    if fecha is not None:
        fecha_formateada = fecha.strftime("%d-%m-%Y")
        return fecha_formateada
    else:
        return None
