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
class MuestrasViews(View):
    #Este metodo permite realizar las conultas que necesitan autentificacion. POST PUT DELETE
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    #Busquedas personalizadas y por defecto
    #las personalizadas varian segun el criterio ingresado, y por defecto muestra todos los objetos
    def get(self, request, campo="",criterio=""):
        if (len(campo)> 0 and len(criterio)> 0):
            if criterio == "id":
                muestras = Muestra.objects.filter(id=campo).select_related('idPaciente')
                if muestras is not None:
                    muestras_values = []
                    for muestra in muestras:
                        paciente = muestra.idPaciente
                        muestra_dict = {
                            'id': muestra.id,
                            'idTipoMuestra':{
                                'id':muestra.idTipoMuestra.id,
                                'nombre':muestra.idTipoMuestra.nombre
                            },
                            'fecha': formato_fecha(muestra.fecha),
                            'idPaciente': {
                                'id': paciente.id,
                                'nombre': paciente.nombre,
                                'apellido': paciente.apellido,
                                'documento': paciente.documento
                            }
                        }
                        muestras_values.append(muestra_dict)
                    context = {
                        'message': "Consulta exitosa",
                        'muestras': muestras_values
                    }
                    return JsonResponse(context)
                else:
                    context = {
                        'message': "No se encontraron los datos",
                        'muestras': []
                    }
                    return JsonResponse(context)
            elif criterio == "nombre":
                idPaciente = Paciente.objects.filter(nombre=campo)
                if idPaciente is not None:
                    for paciente in idPaciente:
                        reg = Muestra.objects.filter(idPaciente=paciente.id).select_related('idPaciente')
                        if reg is not None:
                            muestras_values = []
                            for muestra in reg:
                                paciente = muestra.idPaciente
                                muestra_dict = {
                                    'id': muestra.id,
                                    'idTipoMuestra':{
                                        'id':muestra.idTipoMuestra.id,
                                        'nombre':muestra.idTipoMuestra.nombre
                                    },
                                    'fecha': formato_fecha(muestra.fecha),
                                    'idPaciente': {
                                        'id': paciente.id,
                                        'nombre': paciente.nombre,
                                        'apellido': paciente.apellido,
                                        'documento': paciente.documento
                                    }
                                }
                                muestras_values.append(muestra_dict)
                            context = {
                                'message': "Consulta exitosa",
                                'muestras': muestras_values
                            }
                            return JsonResponse(context)
                        else:
                            context = {
                                'message': "No se encontraron los datos",
                                'muestras': []
                            }
                            return JsonResponse(context)
                else:
                    context = {
                        'message': "No se encontraron los datos",
                        'muestras': []
                    }
                    return JsonResponse(context)
            context = {
                    'message': "No se encontraron los datos",
                    'muestras': []
                }
            return JsonResponse(context)
        else:
            reg = Muestra.objects.select_related('idPaciente')
            if reg is not None:
                muestras_values = []
                for muestra in reg:
                    paciente = muestra.idPaciente
                    muestra_dict = {
                        'id': muestra.id,
                        'idTipoMuestra':{
                            'id':muestra.idTipoMuestra.id,
                            'nombre':muestra.idTipoMuestra.nombre
                        },
                        'fecha': formato_fecha(muestra.fecha),
                        'idPaciente': {
                            'id': paciente.id,
                            'nombre': paciente.nombre,
                            'apellido': paciente.apellido,
                            'documento': paciente.documento
                        }
                    }
                    muestras_values.append(muestra_dict)
                context = {
                    'message': "Consulta exitosa",
                    'muestras': muestras_values
                }
                return JsonResponse(context)
            else:
                context = {
                    'message': "No se encontraron los datos",
                    'muestras': []
                }
                return JsonResponse(context)

#Agregar un registro de tipo
    def post(self, request):
        jd=json.loads(request.body)
        rsp_fecha = datetime.datetime.fromisoformat(jd['fecha'])
        if validar_id_paciente(jd['idPaciente']):    
            muestras = {'message': "El paciente no existe"}
        if validar_id_tipo(jd['idTipoMuestra']):    
            muestras = {'message': "El paciente no existe"}
        elif (rsp_fecha) is None:
            muestras = {'message': "La fecha esta vacía"}
        elif isinstance(rsp_fecha, str):
            muestras = {'message': "La fecha esta vacía"}
        elif (rsp_fecha.year) < 2000:
            muestras = {'message': "La fecha debe estar en el rango de año de 2000 a 2030"}
        elif (rsp_fecha.year) > 2030:
            muestras = {'message': "La fecha debe estar en el rango de año de 2000 a 2030"}
        else:
            muestras = {'message': "Registro Exitoso."}
            Muestra.objects.create(idPaciente=instanciar_paciente(jd['idPaciente']), idTipoMuestra=instanciar_tipo(jd['idTipoMuestra']),fecha=jd['fecha'])
            muestras = {'message':"Registro Exitoso."}
        return JsonResponse(muestras)

#Actualizar un registro de tipo
    def put(self, request,id):
        jd=json.loads(request.body)
        muestras = list(Muestra.objects.filter(id=id).values())
        if len(muestras) > 0:
            rsp_fecha = datetime.datetime.fromisoformat(jd['fecha'])
            muestra=Muestra.objects.get(id=id)
            if validar_id_paciente(jd['idPaciente']):    
                muestras = {'message': "El paciente no existe"}
            if validar_id_tipo(jd['idTipoMuestra']):    
                muestras = {'message': "El paciente no existe"}
            elif (rsp_fecha) is None:
                muestras = {'message': "La fecha esta vacía"}
            elif isinstance(rsp_fecha, str):
                muestras = {'message': "La fecha esta vacía"}
            elif (rsp_fecha.year) < 2000:
                muestras = {'message': "La fecha debe estar en el rango de año de 2000 a 2030"}
            elif (rsp_fecha.year) > 2030:
                muestras = {'message': "La fecha debe estar en el rango de año de 2000 a 2030"}
            else:
                muestra.idPaciente = instanciar_paciente(jd['idPaciente'])
                muestra.idTipoMuestra = instanciar_tipo(jd['idTipoMuestra'])
                muestra.fecha = jd['fecha']
                muestra.save()
                muestras = {'message': "La actualización fue exitosa."}
        return JsonResponse(muestras)
        
        
#Eliminar un registro de tipo
    def delete(self, request,id):
        muestra = list(Muestra.objects.filter(id=id).values())
        if len(muestra) > 0:
            Muestra.objects.filter(id=id).delete()
            datos = {'message':"Registro Eliminado"}
        else:
            datos = {'message':"No se encontraró el registro", 'muestra': []}
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

def instanciar_tipo(id):
    if (id>0):
        paciente = TipoMuestra.objects.get(id=id)
        if paciente:
            return paciente   

def validar_id_tipo(id):
    if (id>0):
        registro = TipoMuestra.objects.filter(id=id)
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

def formato_fecha(fecha):
    if fecha is not None:
        fecha_formateada = fecha.strftime("%d-%m-%Y %H:%M:%S")
        return fecha_formateada
    else:
        return None