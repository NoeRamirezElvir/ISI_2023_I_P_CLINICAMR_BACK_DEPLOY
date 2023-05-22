from django.http.response import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
import re
from ..models import *
from django.views.decorators.http import require_http_methods

@method_decorator(require_http_methods(['POST','PUT','GET','DELETE']), name='dispatch')
class EnfermedadView(View):
    #Este metodo permite realizar las conultas que necesitan autentificacion. POST PUT DELETE
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    #Busquedas personalizadas y por defecto
    #las personalizadas varian segun el criterio ingresado, y por defecto muestra todos los objetos
    def get(self, request, campo="",criterio=""):
        try:
            if (len(campo)> 0 and len(criterio)> 0):
                if criterio == "id":
                    enfermedades = Enfermedad.objects.filter(id=campo).values()
                    if enfermedades is not None:
                        enfermedades_values = []
                        for enfermedad in enfermedades:
                            enfermedad_dict = {
                                'id': enfermedad['id'],
                                'nombre': enfermedad['nombre'],
                                'idSintomas':{}
                            }
                            sintomas = EnfermedadDetalle.objects.filter(idEnfermedad = enfermedad['id']).select_related('idSintoma')
                            for sintoma in sintomas:
                                sintoma_dict = {
                                    'id': sintoma.idSintoma.id,
                                    'nombre': sintoma.idSintoma.nombre
                                }
                                enfermedad_dict['idSintomas'][sintoma.idSintoma.id] = sintoma_dict
                            enfermedades_values.append(enfermedad_dict)
                        context = {
                            'message': "Consulta exitosa",
                            'enfermedades': enfermedades_values
                        }
                        return JsonResponse(context)
                    else:
                        context = {
                            'message': "No se encontraron los datos",
                            'enfermedades': enfermedades_values
                        }
                        return JsonResponse(context)
                elif criterio == "nombre":
                    enfermedades = Enfermedad.objects.filter(nombre=campo).values()
                    if enfermedades is not None:
                        enfermedades_values = []
                        for enfermedad in enfermedades:
                            enfermedad_dict = {
                                'id': enfermedad['id'],
                                'nombre': enfermedad['nombre'],
                                'idSintomas':{}
                            }
                            sintomas = EnfermedadDetalle.objects.filter(idEnfermedad = enfermedad['id']).select_related('idSintoma')
                            for sintoma in sintomas:
                                sintoma_dict = {
                                    'id': sintoma.idSintoma.id,
                                    'nombre': sintoma.idSintoma.nombre
                                }
                                enfermedad_dict['idSintomas'][sintoma.idSintoma.id] = sintoma_dict
                            enfermedades_values.append(enfermedad_dict)
                        context = {
                            'message': "Consulta exitosa",
                            'enfermedades': enfermedades_values
                        }
                        return JsonResponse(context)
                    else:
                        context = {
                            'message': "No se encontraron los datos",
                            'enfermedades': enfermedades_values
                        }
                        return JsonResponse(context)
            else:
                enfermedades = Enfermedad.objects.values()
                if enfermedades is not None:
                    enfermedades_values = []
                    for enfermedad in enfermedades:
                        enfermedad_dict = {
                            'id': enfermedad['id'],
                            'nombre': enfermedad['nombre'],
                            'idSintomas':{}
                        }
                        sintomas = EnfermedadDetalle.objects.filter(idEnfermedad = enfermedad['id']).select_related('idSintoma')
                        for sintoma in sintomas:
                            sintoma_dict = {
                                'id': sintoma.idSintoma.id,
                                'nombre': sintoma.idSintoma.nombre
                            }
                            enfermedad_dict['idSintomas'][sintoma.idSintoma.id] = sintoma_dict
                        enfermedades_values.append(enfermedad_dict)
                    context = {
                        'message': "Consulta exitosa",
                        'enfermedades': enfermedades_values
                    }
                    return JsonResponse(context)
                else:
                    enfermedades_values = []
                    context = {
                        'message': "No se encontraron los datos",
                        'enfermedades': enfermedades_values
                    }
                    return JsonResponse(context)
            return JsonResponse(context)
        except TypeError as e:
            context = {
                'message': f"El registro no existe. Excepcion: {e}",
            }
            return JsonResponse(context)
        except Exception as a:
            context = {
                'message': f"Error. Excepcion: {a}",
            }
            return JsonResponse(context)

#Agregar un registro de cargos
    def post(self, request):
        jd=json.loads(request.body)
        if len(jd['nombre']) <= 0:
            mensaje_post = {'message': "El nombre esta vacío."}
        elif (validar_nombre_repetido(jd['nombre'])):
            mensaje_post = {'message': "El nombre ya esta en uso."}
        elif len(jd['nombre']) < 3:
            mensaje_post = {'message': "El nombre debe tener mas de 3 caracteres."}
        elif not validar_cadena_espacios(jd['nombre']):
            mensaje_post = {'message': "No se permiten mas de un espacio consecutivo."}
        elif validar_cadena_repeticion(jd['nombre']):
            mensaje_post = {'message': "No se permiten mas de dos caracteres consecutivos del mismo tipo."}
        elif len(jd['nombre']) > 50:
            mensaje_post = {'message': "El nombre debe tener menos de 50 caracteres."}
        elif jd['idSintomas'] is None :
            mensaje_post = {'message': "No hay sintomas relacionados o estan vacíos."}
        elif jd['idSintomas'] == []:
            mensaje_post = {'message': "No hay sintomas relacionados o estan vacíos."}
        elif len(jd['idSintomas']) < 0:
            mensaje_post = {'message': "No hay sintomas relacionados o estan vacíos."}
        else:
            
            Enfermedad.objects.create(nombre=jd['nombre'])
            for sintoma in jd['idSintomas']:
                idsintoma = instanciar_sintoma(int(sintoma['id']))
                EnfermedadDetalle.objects.create(idEnfermedad=instanciar_enfermedad(jd['nombre']), idSintoma = idsintoma)
            mensaje_post = {'message':"Registro Exitoso."}
        return JsonResponse(mensaje_post)

#Actualizar un registro de cargos
    def put(self, request,id):
        jd=json.loads(request.body)
        mensaje_put = list(Enfermedad.objects.filter(id=id).values())
        if len(mensaje_put) > 0:
            enfermedad_actualizar=Enfermedad.objects.get(id=id)
            if len(jd['nombre']) <= 0:
                mensaje_put = {'message': "El nombre esta vacío."}
            elif len(jd['nombre']) < 3:
                mensaje_put = {'message': "El nombre debe tener mas de 3 caracteres."}
            elif not validar_cadena_espacios(jd['nombre']):
                mensaje_put = {'message': "No se permiten mas de un espacio consecutivo."}
            elif validar_cadena_repeticion(jd['nombre']):
                mensaje_put = {'message': "No se permiten mas de dos caracteres consecutivos del mismo tipo."}
            elif len(jd['nombre']) > 50:
                mensaje_put = {'message': "El nombre debe tener menos de 50 caracteres."}
            elif jd['idSintomas'] == []:
                mensaje_put = {'message': "No hay sintomas relacionados o estan vacíos."}
            elif len(jd['idSintomas']) < 0:
                mensaje_put = {'message': "No hay sintomas relacionados o estan vacíos."}
            else:
                sintomas = EnfermedadDetalle.objects.filter(idEnfermedad=id).values('idSintoma')
                ids_sintomas = [{'id': sintoma['idSintoma']} for sintoma in sintomas]
                ids_actualizar = [{'id': sintoma['id']} for sintoma in jd['idSintomas']]

                # obtener los IDs que están en idSintomas pero no en ids_lista
                ids_faltantes = [sintoma['id'] for sintoma in ids_actualizar if sintoma not in ids_sintomas]

                # obtener los IDs que están en ids_lista pero no en idSintomas
                ids_extra = [sintoma['id'] for sintoma in ids_sintomas if sintoma not in ids_actualizar]

                # verificar si la lista de IDs faltantes no está vacía
                if len(ids_faltantes) > 0:
                    # imprimir un mensaje para cada ID faltante
                    for id_faltante in ids_faltantes:
                        #Crea un detalle por cada id que no se encuentre en la lista de detalles pero si en la nueva lista
                        EnfermedadDetalle.objects.create(idEnfermedad=enfermedad_actualizar, idSintoma = instanciar_sintoma(id_faltante))
                # verificar si la lista de IDs extra no está vacía
                if len(ids_extra) > 0:
                    # imprimir un mensaje para cada ID extra
                    for id_extra in ids_extra:
                        #Borra los detalles que se encuentran en la lista de detalles pero que no estan en la nueva lista
                        reg_del = EnfermedadDetalle.objects.filter(idEnfermedad=enfermedad_actualizar, idSintoma = instanciar_sintoma(id_extra))
                        reg_del.delete()


                enfermedad_actualizar.nombre = jd['nombre']
                enfermedad_actualizar.save()
                mensaje_put = {'message': "La actualización fue exitosa."}
        return JsonResponse(mensaje_put)
        
        
#Eliminar un registro de cargos
    def delete(self, request,id):
        enfermedades = list(Enfermedad.objects.filter(id=id).values())
        if len(enfermedades) > 0:
            Enfermedad.objects.filter(id=id).delete()
            datos = {'message':"Registro Eliminado"}
        else:
            datos = {'message':"No se encontraron registros", 'enfermedades': []}
        return JsonResponse(datos)
    

def validar_detalle_existente(idEnfermedad,idSintoma):
    if (idEnfermedad and idSintoma):
        registros = EnfermedadDetalle.objects.filter(idEnfermedad=idEnfermedad, idSintoma=idSintoma)
        if registros:
            return False
        else:
            return True

def validar_nombre_repetido(nombre): 
    if (nombre):
        registros = Enfermedad.objects.filter(nombre=nombre)
        if len(registros) > 0:
            return True
        else:
            return False
    return False

def instanciar_sintoma(id):
    if (id > 0):
        sintoma = Sintoma.objects.filter(id=id).last()
    if sintoma:
        return sintoma

def instanciar_enfermedad(nombre):
    if (nombre):
        enfermedad = Enfermedad.objects.filter(nombre=nombre).last()
    if enfermedad:
        return enfermedad

def validar_cadena_repeticion(cadena):
    patron = r'([a-zA-Z])\1\1'
    return bool(re.search(patron, cadena))

def validar_cadena_espacios(cadena):
    patron = r'^[^ ]+(?: {0,1}[^ ]+)*$'
    return bool(re.match(patron,cadena))
