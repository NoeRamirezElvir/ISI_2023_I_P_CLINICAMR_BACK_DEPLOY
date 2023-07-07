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
class PermisosViews(View):
    #Este metodo permite realizar las conultas que necesitan autentificacion. POST PUT DELETE
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    #Busquedas personalizadas y por defecto
    #las personalizadas varian segun el criterio ingresado, y por defecto tratamiento todos los objetos
    def get(self, request, campo="",criterio=""):
        if (len(campo)> 0 and len(criterio)> 0):
            if criterio == "id":
                permisos = Permisos.objects.filter(id=campo).select_related('idCargoEmpleado','idAcciones','idPantallas')
                if permisos is not None:
                    permisos_values = []
                    for permiso in permisos:
                        
                        permiso_dict = {
                            'id': permiso.id,
                            'activo': permiso.activo,
                            

                            'idCargoEmpleado': {
                                'id': permiso.idCargoEmpleado.id,
                                'nombre': permiso.idCargoEmpleado.nombre,
                                'descripcion': permiso.idCargoEmpleado.descripcion,
                                'activo': permiso.idCargoEmpleado.activo
                            },
                            'idAcciones': {
                                'id': permiso.idAcciones.id,
                                'nombre': permiso.idAcciones.nombre
                            },
                            'idPantallas': {
                                'id': permiso.idPantallas.id,
                                'nombre': permiso.idPantallas.nombre
                                
                            }
                        }
                        permisos_values.append(permiso_dict)
                    context = {
                            'message': "Consulta exitosa",
                            'permisos': permisos_values
                        }
                    return JsonResponse(context)
                else:
                    context = {
                        'message': "No se encontraron los datos",
                        'permisos': []
                    }
                    return JsonResponse(context)
                
            elif criterio == "nombre":
                
                permisos = Permisos.objects.filter(idCargoEmpleado__idAcciones_idPantallas_nombre=campo)
                if permisos is not None:
                    permisos_values = []
                    for permiso in permisos:
                        permiso_dict = {
                           'id': permiso.id,
                            'activo': permiso.activo,
                            

                            'idCargoEmpleado': {
                                'id': permiso.idCargoEmpleado.id,
                                'nombre': permiso.idCargoEmpleado.nombre,
                                'descripcion': permiso.idCargoEmpleado.descripcion,
                                'activo': permiso.idCargoEmpleado.activo
                            },
                            'idAcciones': {
                                'id': permiso.idAcciones.id,
                                'nombre': permiso.idAcciones.nombre
                            },
                            'idPantallas': {
                                'id': permiso.idPantallas.id,
                                'nombre': permiso.idPantallas.nombre
                                
                            }
                        }
                        permisos_values.append(permiso_dict)
                    context = {
                        'message': "Consulta exitosa",
                        'permisos': permisos_values
                    }
                    return JsonResponse(context)
                else:
                    context = {
                        'message': "No se encontraron los datos",
                        'permisos': []
                    }
                    return JsonResponse(context)          
        else:                
            permisos = Permisos.objects.select_related('idCargoEmpleado','idAcciones','idPantallas')
            if permisos is not None:
                permisos_values = []
                for permiso in permisos:
                    permiso_dict = {
                            'id': permiso.id,
                            'activo': permiso.activo,
                            

                            'idCargoEmpleado': {
                                'id': permiso.idCargoEmpleado.id,
                                'nombre': permiso.idCargoEmpleado.nombre,
                                'descripcion': permiso.idCargoEmpleado.descripcion,
                                'activo': permiso.idCargoEmpleado.activo
                            },
                            'idAcciones': {
                                'id': permiso.idAcciones.id,
                                'nombre': permiso.idAcciones.nombre
                            },
                            'idPantallas': {
                                'id': permiso.idPantallas.id,
                                'nombre': permiso.idPantallas.nombre
                                
                            }
                    }
                    permisos_values.append(permiso_dict)
                context = {
                    'message': "Consulta exitosa",
                    'permisos': permisos_values
                }
                return JsonResponse(context)
            else:
                context = {
                    'message': "No se encontraron los datos",
                    'permisos': []
                }
                return JsonResponse(context)
            
#Agregar un registro de trasaldo
    def post(self, request):
        jd=json.loads(request.body)
        if validar_id_acciones(jd['idAcciones']):    
            permisos = {'message': "Las acciones no existen"}
        if validar_id_cargo(jd['idCargoEmpleado']):    
            permisos = {'message': "El Cargo no existe"}
        if validar_id_pantallas(jd['idPantallas']):    
            permisos = {'message': "La pantalla no existe"}
        elif jd['activo'] < 0:
            permisos = {'message': "Activo debe ser positivo."}
        elif jd['activo'] > 1:
            permisos = {'message': "Activo debe unicamente puede ser 0 o 1."}
        else:
            permisos = {'message': "Registro Exitoso."}
            Permisos.objects.create(idAcciones=instanciar_acciones(jd['idAcciones']),
                                            idCargoEmpleado=instanciar_cargo(jd['idCargoEmpleado']),
                                            idPantallas=instanciar_pantallas(jd['idPantallas']),
                                            activo=jd['activo'],
                                            
                                            )
                                                                    
            permisos = {'message':"Registro Exitoso."}
        return JsonResponse(permisos)
    

#Actualizar un registro de tipo
    def put(self, request,id):
        jd=json.loads(request.body)
        permisos = list(Permisos.objects.filter(id=id).values())
        if len(permisos) > 0:
            
            permiso=Permisos.objects.get(id=id)
        if validar_id_acciones(jd['idAcciones']):    
            permisos = {'message': "Las acciones no existen"}
        if validar_id_cargo(jd['idCargoEmpleado']):    
            permisos = {'message': "El Cargo no existe"}
        if validar_id_pantallas(jd['idPantallas']):    
            permisos = {'message': "La pantalla no existe"}
        elif jd['activo'] < 0:
            permisos = {'message': "Activo debe ser positivo."}
        elif jd['activo'] > 1:
            permisos = {'message': "Activo debe unicamente puede ser 0 o 1."}
        else:
            permiso.idCargoEmpleado = instanciar_cargo(jd['idCargoEmpleado'])
            permiso.idAcciones = instanciar_acciones(jd['idAutorizacionCargo'])
            permiso.idPantallas = instanciar_pantallas(jd['idEmpleado'])
            permiso.activo = jd['activo']
            permiso.save()
            permisos = {'message': "La actualización fue exitosa."}
        return JsonResponse(permisos)
        
        
#Eliminar un registro de tipo
    def delete(self, request,id):
        permiso = list(Permisos.objects.filter(id=id).values())
        if len(permiso) > 0:
            Permisos.objects.filter(id=id).delete()
            datos = {'message':"Registro Eliminado"}
        else:
            datos = {'message':"No se encontraró el registro", 'traslado': []}
        return JsonResponse(datos)
    
def instanciar_cargo(id):
    if (id>0):
        cargo = CargoEmpleado.objects.get(id=id)
        if cargo:
            return cargo   

def validar_id_cargo(id):
    if (id>0):
        registro = CargoEmpleado.objects.filter(id=id)
        if registro:
            return False
        else:
            return True    


def instanciar_acciones(id):
    if (id>0):
        accion = Acciones.objects.get(id=id)
        if accion:
            return accion  

def validar_id_acciones(id):
    if (id>0):
        registro = Acciones.objects.filter(id=id)
        if registro:
            return False
        else:
            return True 
        

def instanciar_pantallas(id):
    if (id>0):
        pantalla = Pantallas.objects.get(id=id)
        if pantalla:
            return pantalla   

def validar_id_pantallas(id):
    if (id>0):
        registro = Pantallas.objects.filter(id=id)
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

