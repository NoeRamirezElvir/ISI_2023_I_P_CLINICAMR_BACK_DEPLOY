from datetime import datetime, timedelta
from django.http.response import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
import re
from ..models import *
from django.views.decorators.http import require_http_methods
from decimal import Decimal

@method_decorator(require_http_methods(['POST','PUT','GET','DELETE']), name='dispatch')
class TiposView(View):
    #Este metodo permite realizar las conultas que necesitan autentificacion. POST PUT DELETE
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    #Busquedas personalizadas y por defecto
    #las personalizadas varian segun el criterio ingresado, y por defecto muestra todos los objetos
    def get(self, request, campo="",criterio=""):
        if (len(campo)> 0 and len(criterio)> 0):
            if criterio == "id":
                tipos = Tipo.objects.filter(id=campo).select_related('idsubtipo','idImpuesto')
                if tipos is not None:
                    tipos_values = []
                    for tipo in tipos:
                        tipo_dict = {
                            'id': tipo.id,
                            'nombre': tipo.nombre,
                            'descripcion': tipo.descripcion,
                            'precio': tipo.precio,
                            'idsubtipo': {
                                'id': tipo.idsubtipo.id,
                                'nombre': tipo.idsubtipo.nombre
                            },
                            'idImpuesto': []
                        }
                        if tipo.idImpuesto is not None:
                            tipo_dict['idImpuesto'] = {
                                'id': tipo.idImpuesto.id,
                                'nombre': tipo.idImpuesto.nombre,
                                'valor': tipo.idImpuesto.valor
                            }
                        tipos_values.append(tipo_dict)
                    context = {
                        'message': "Consulta exitosa",
                        'tipos': tipos_values
                    }
                    return JsonResponse(context)
                else:
                    context = {
                        'message': "No se encontraron los datos",
                        'tipos': []
                    }
                    return JsonResponse(context)
            elif criterio == "nombre":
                tipos = Tipo.objects.filter(nombre=campo).select_related('idsubtipo','idImpuesto')
                if tipos is not None:
                    tipos_values = []
                    for tipo in tipos:
                        tipo_dict = {
                            'id': tipo.id,
                            'nombre': tipo.nombre,
                            'descripcion': tipo.descripcion,
                            'precio': tipo.precio,
                            'idsubtipo': {
                                'id': tipo.idsubtipo.id,
                                'nombre': tipo.idsubtipo.nombre
                            },
                            'idImpuesto': []
                        }
                        if tipo.idImpuesto is not None:
                            tipo_dict['idImpuesto'] = {
                                'id': tipo.idImpuesto.id,
                                'nombre': tipo.idImpuesto.nombre,
                                'valor': tipo.idImpuesto.valor
                            }
                        tipos_values.append(tipo_dict)
                    context = {
                        'message': "Consulta exitosa",
                        'tipos': tipos_values
                    }
                    return JsonResponse(context)
                else:
                    context = {
                        'message': "No se encontraron los datos",
                        'tipos': []
                    }
                    return JsonResponse(context)
            elif criterio == "subtipo":
                tipos = Tipo.objects.filter(idsubtipo__nombre=campo).select_related('idImpuesto')
                if tipos is not None:
                    tipos_values = []
                    for tipo in tipos:
                        tipo_dict = {
                            'id': tipo.id,
                            'nombre': tipo.nombre,
                            'descripcion': tipo.descripcion,
                            'precio': tipo.precio,
                            'idsubtipo': {
                                'id': tipo.idsubtipo.id,
                                'nombre': tipo.idsubtipo.nombre
                            },
                            'idImpuesto': []
                        }
                        if tipo.idImpuesto is not None:
                            tipo_dict['idImpuesto'] = {
                                'id': tipo.idImpuesto.id,
                                'nombre': tipo.idImpuesto.nombre,
                                'valor': tipo.idImpuesto.valor
                            }
                        tipos_values.append(tipo_dict)
                    context = {
                        'message': "Consulta exitosa",
                        'tipos': tipos_values
                    }
                    return JsonResponse(context)
                else:
                    context = {
                        'message': "No se encontraron los datos",
                        'tipos': []
                    }
                    return JsonResponse(context)
        else:
            tipos = Tipo.objects.select_related('idsubtipo','idImpuesto')
            if tipos is not None:
                tipos_values = []
                for tipo in tipos:
                    tipo_dict = {
                        'id': tipo.id,
                        'nombre': tipo.nombre,
                        'descripcion': tipo.descripcion,
                        'precio': tipo.precio,
                        'idsubtipo': {
                            'id': tipo.idsubtipo.id,
                            'nombre': tipo.idsubtipo.nombre
                        },
                        'idImpuesto': []
                    }
                    if tipo.idImpuesto is not None:
                        tipo_dict['idImpuesto'] = {
                            'id': tipo.idImpuesto.id,
                            'nombre': tipo.idImpuesto.nombre,
                            'valor': tipo.idImpuesto.valor
                        }
                    tipos_values.append(tipo_dict)
                context = {
                    'message': "Consulta exitosa",
                    'tipos': tipos_values
                }
                return JsonResponse(context)
            else:
                context = {
                    'message': "No se encontraron los datos",
                    'tipos': []
                }
                return JsonResponse(context)

#Agregar un registro de tipo
    def post(self, request):
        jd=json.loads(request.body)

        if len(jd['nombre']) <= 0:
            tipo = {'message': "El nombre esta vacío."}
        elif (validar_tipo_repetido(jd['nombre'])):
            tipo = {'message': "El tipo ya existe."}
        elif len(jd['nombre']) < 4:
            tipo = {'message': "El nombre debe tener mas de 4 caracteres."}
        elif not validar_cadena_espacios(jd['nombre']):
            tipo = {'message': "No se permiten mas de un espacio consecutivo."}
        elif validar_cadena_repeticion(jd['nombre']):
            tipo = {'message': "No se permiten mas de dos caracteres consecutivos del mismo tipo."}
        elif len(jd['nombre']) > 50:
            tipo = {'message': "El nombre debe tener menos de 50 caracteres."}
        elif len(jd['descripcion']) <= 0:
            tipo = {'message': "La descripción esta vacía."}
        elif len(jd['descripcion']) < 4:
            tipo = {'message': "La descripción debe tener mas de 4 caracteres."}
        elif len(jd['descripcion']) > 50:
            tipo = {'message': "La descripción debe tener menos de 50 caracteres."}
        elif jd['idsubtipo'] == [] or jd['idsubtipo'] == 0:
            tipo = {'message': "Seleccione un subtipo existente."}
        elif validar_tipo_impuesto(int(jd['idsubtipo'])) and (jd['idImpuesto'] == [] or jd['idImpuesto'] == 0):
            tipo = {'message': "Seleccione un impuesto existente."}
        else:
            tipo = {'message':"Registro Exitoso."}
            subtipo = instanciar_subtipo(int(jd['idsubtipo']))
            if subtipo.nombre.lower() == 'examen'.lower():
                if Decimal(jd['precio']) > 0:
                    precios= Decimal(jd['precio'])
                    if len(str(jd['precio'])) > 11:
                        tipo = {'message': "El precio debe tener menos de 10 digitos."}
                    elif round(Decimal(jd['precio'])) > 99999999.99:
                        tipo = {'message': "El precio es muy alto."}
                    elif round(Decimal(jd['precio']), 2) > round(Decimal(jd['precio']), 2):
                        tipo = {'message': "El precio debe ser mayor al costo de compra."}
                    else:
                        id_tipo = Tipo.objects.create(nombre=jd['nombre'], descripcion=jd['descripcion'],idsubtipo=instanciar_subtipo(int(jd['idsubtipo'])),idImpuesto=instanciar_impuesto(int(jd['idImpuesto'])),precio=precios)
                        PrecioHistoricoExamen.objects.create(idTipo=id_tipo,
                                                            fechaInicio=datetime.now(),
                                                            activo=1,
                                                            precio=jd['precio'])
                else:
                    tipo = {'message': "El precio debe ser mayor a 0."}
                
            elif subtipo.nombre.lower() == 'tratamiento'.lower():
                precios= Decimal(jd['precio'])
                if Decimal(jd['precio']) > 0:
                    if len(str(jd['precio'])) > 11:
                        tipo = {'message': "El precio debe tener menos de 10 digitos."}
                    elif round(Decimal(jd['precio'])) > 99999999.99:
                        tipo = {'message': "El precio es muy alto."}
                    elif round(Decimal(jd['precio']), 2) > round(Decimal(jd['precio']), 2):
                        tipo = {'message': "El precio debe ser mayor al costo de compra."}
                    else:
                        id_tipo = Tipo.objects.create(nombre=jd['nombre'], descripcion=jd['descripcion'],idsubtipo=instanciar_subtipo(int(jd['idsubtipo'])),idImpuesto=instanciar_impuesto(int(jd['idImpuesto'])),precio=precios)
                        PrecioHistoricoTratamiento.objects.create(idTipo=id_tipo,
                                                            fechaInicio=datetime.now(),
                                                            activo=1,
                                                            precio=jd['precio'])
                else:
                    tipo = {'message': "El precio debe ser mayor a 0."}
            elif subtipo.nombre.lower() == 'consulta'.lower():
                precios= Decimal(jd['precio'])
                if Decimal(jd['precio']) > 0:
                    if len(str(jd['precio'])) > 11:
                        tipo = {'message': "El precio debe tener menos de 10 digitos."}
                    elif round(Decimal(jd['precio'])) > 99999999.99:
                        tipo = {'message': "El precio es muy alto."}
                    elif round(Decimal(jd['precio']), 2) > round(Decimal(jd['precio']), 2):
                        tipo = {'message': "El precio debe ser mayor al costo de compra."}
                    else:
                        id_tipo = Tipo.objects.create(nombre=jd['nombre'], descripcion=jd['descripcion'],idsubtipo=instanciar_subtipo(int(jd['idsubtipo'])),idImpuesto=instanciar_impuesto(int(jd['idImpuesto'])),precio=precios)
                        PrecioHistoricoConsulta.objects.create(idTipo=id_tipo,
                                                            fechaInicio=datetime.now(),
                                                            activo=1,
                                                            precio=jd['precio'])
                else:
                    tipo = {'message': "El precio debe ser mayor a 0."}
            else:
                Tipo.objects.create(nombre=jd['nombre'], descripcion=jd['descripcion'],idsubtipo=instanciar_subtipo(int(jd['idsubtipo'])),precio=0.00)
        return JsonResponse(tipo)

#Actualizar un registro de tipo
    def put(self, request,id):
        jd=json.loads(request.body)
        tipo = list(Tipo.objects.filter(id=id).values())
        if len(tipo) > 0:
            tipos=Tipo.objects.get(id=id)
            if len(jd['nombre']) <= 0:
                tipo = {'message': "El nombre esta vacío."}
            elif len(jd['nombre']) < 4:
                tipo = {'message': "El nombre debe tener mas de 4 caracteres."}
            elif not validar_cadena_espacios(jd['nombre']):
                tipo = {'message': "No se permiten mas de un espacio consecutivo."}
            elif validar_cadena_repeticion(jd['nombre']):
                tipo = {'message': "No se permiten mas de dos caracteres consecutivos del mismo tipo."}
            elif len(jd['nombre']) > 50:
                tipo = {'message': "El nombre debe tener menos de 50 caracteres."}
            elif len(jd['descripcion']) <= 0:
                tipo = {'message': "La descripción esta vacía."}
            elif len(jd['descripcion']) < 4:
                tipo = {'message': "La descripción debe tener mas de 4 caracteres."}
            elif len(jd['descripcion']) > 50:
                tipo = {'message': "La descripción debe tener menos de 50 caracteres."}
            elif jd['idsubtipo'] == [] or jd['idsubtipo'] == 0:
                tipo = {'message': "Seleccione un subtipo existente."}
            elif validar_tipo_impuesto(int(jd['idsubtipo'])) and (jd['idImpuesto'] == [] or jd['idImpuesto'] == 0):
                tipo = {'message': "Seleccione un impuesto existente."}
            else:
                tipo = {'message': "La actualización fue exitosa."}
                tipo_temp = tipos
                tipos.idsubtipo = instanciar_subtipo(int(jd['idsubtipo']))
                tipos.idImpuesto = instanciar_impuesto(int(jd['idImpuesto']))
                tipos.nombre = jd['nombre']
                tipos.descripcion = jd['descripcion']
                tipos.precio = Decimal(jd['precio'])
                subtipo = instanciar_subtipo(int(jd['idsubtipo']))
                if subtipo.nombre.lower() == 'examen'.lower():
                    if Decimal(jd['precio']) > 0:
                        if len(str(jd['precio'])) > 11:
                            tipo = {'message': "El precio debe tener menos de 10 digitos."}
                        elif round(Decimal(jd['precio'])) > 99999999.99:
                            tipo = {'message': "El precio es muy alto."}
                        else:
                            precio_historico_examen =  PrecioHistoricoExamen.objects.filter(idTipo=id).last()
                            if precio_historico_examen is not None:
                                if not round(Decimal(precio_historico_examen.precio), 2) == round(Decimal(tipos.precio), 2):
                                    precio_historico_examen.fechaFinal = fecha_final()
                                    precio_historico_examen.save()
                                    PrecioHistoricoExamen.objects.create(idTipo=tipo_temp,
                                                                        fechaInicio=datetime.now(),
                                                                        activo=1,
                                                                        precio=jd['precio'])
                            else:
                                PrecioHistoricoExamen.objects.create(idTipo=tipo_temp,
                                                                    fechaInicio=datetime.now(),
                                                                    activo=1,
                                                                    precio=jd['precio'])
                    else:
                        tipo = {'message': "El precio debe ser mayor a 0."}
                elif subtipo.nombre.lower() == 'tratamiento'.lower():
                    if Decimal(jd['precio']) > 0:
                        if len(str(jd['precio'])) > 11:
                            tipo = {'message': "El precio debe tener menos de 10 digitos."}
                        elif round(Decimal(jd['precio'])) > 99999999.99:
                            tipo = {'message': "El precio es muy alto."}
                        else:
                            precio_historico_tratamiento =  PrecioHistoricoTratamiento.objects.filter(idTipo=id).last()
                            if precio_historico_tratamiento is not None:
                                if not round(Decimal(precio_historico_tratamiento.precio), 2) == round(Decimal(tipos.precio), 2):
                                    precio_historico_tratamiento.fechaFinal = fecha_final()
                                    precio_historico_tratamiento.save()
                                    PrecioHistoricoTratamiento.objects.create(idTipo=tipo_temp,
                                                                        fechaInicio=datetime.now(),
                                                                        activo=1,
                                                                        precio=jd['precio'])
                            else:
                                PrecioHistoricoTratamiento.objects.create(idTipo=tipo_temp,
                                                                    fechaInicio=datetime.now(),
                                                                    activo=1,
                                                                    precio=jd['precio'])
                    else:
                        tipo = {'message': "El precio debe ser mayor a 0."}
                elif subtipo.nombre.lower() == 'consulta'.lower():
                    if Decimal(jd['precio']) > 0:
                        if len(str(jd['precio'])) > 11:
                            tipo = {'message': "El precio debe tener menos de 10 digitos."}
                        elif round(Decimal(jd['precio'])) > 99999999.99:
                            tipo = {'message': "El precio es muy alto."}
                        else:
                            precio_historico_tratamiento =  PrecioHistoricoConsulta.objects.filter(idTipo=id).last()
                            if precio_historico_tratamiento is not None:
                                if not round(Decimal(precio_historico_tratamiento.precio), 2) == round(Decimal(tipos.precio), 2):
                                    precio_historico_tratamiento.fechaFinal = fecha_final()
                                    precio_historico_tratamiento.save()
                                    PrecioHistoricoConsulta.objects.create(idTipo=tipo_temp,
                                                                        fechaInicio=datetime.now(),
                                                                        activo=1,
                                                                        precio=jd['precio'])
                            else:
                                PrecioHistoricoConsulta.objects.create(idTipo=tipo_temp,
                                                                    fechaInicio=datetime.now(),
                                                                    activo=1,
                                                                    precio=jd['precio'])
                    else:
                        tipo = {'message': "El precio debe ser mayor a 0."}
                tipos.save()
        return JsonResponse(tipo)
        
        
        
#Eliminar un registro de tipo
    def delete(self, request,id):
        tipo = list(Tipo.objects.filter(id=id).values())
        if len(tipo) > 0:
            Tipo.objects.filter(id=id).delete()
            datos = {'message':"Registro Eliminado"}
        else:
            datos = {'message':"No se encontraró el registro", 'tipos': []}
        return JsonResponse(datos)



def fecha_final():
    fecha_menos_un_dia=datetime.today()+timedelta(days=-1)
    return fecha_menos_un_dia

def validar_tipo_repetido(nombre): 
    if (nombre):
        registros = Tipo.objects.filter(nombre=nombre)
        if len(registros) > 0:
            return True
        else:
            return False
    return False

def validar_tipo_impuesto(id): 
    subtipo = instanciar_subtipo(id)
    print(subtipo.nombre)
    if (subtipo.nombre).lower() == 'examen':
        return True
    elif (subtipo.nombre).lower() == 'tratamiento':
        return True
    elif (subtipo.nombre).lower() == 'consulta':
        return True
    else:
        return False

def validar_tipo_repedio_subtipo(nombre, idsubtipo):
    if (nombre and nombre):
        tipos = Tipo.objects.filter(nombre=nombre)
        x = 0
        for i in tipos:
            if i.idsubtipo == idsubtipo and i.nombre == nombre:
                    x = x + 1
                    if x > 1:
                        return True
                    else:
                        return False

def instanciar_subtipo(id):
    if (id>0):
        subtipo = Subtipo.objects.get(id=id)
        if subtipo:
            return subtipo
        

def validar_id_subtipo(id):
    if (id>0):
        subtipo = Subtipo.objects.filter(id=id)
        if subtipo:
            return False
        else:
            return True

def instanciar_impuesto(id):
    if (id>0):
        impuesto = Impuesto.objects.get(id=id)
        if impuesto:
            return impuesto

def validar_cadena_repeticion(cadena):
    patron = r'([a-zA-Z])\1\1'
    return bool(re.search(patron, cadena))

def validar_cadena_espacios(cadena):
    patron = r'^[^ ]+(?: {0,1}[^ ]+)*$'
    return bool(re.match(patron,cadena))