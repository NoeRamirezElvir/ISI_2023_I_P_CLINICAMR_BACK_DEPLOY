from django.http.response import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
import re
from ..models import *
from django.views.decorators.http import require_http_methods

@method_decorator(require_http_methods(['POST','PUT','GET','DELETE']), name='dispatch')
class DiagnosticoView(View):
    #Este metodo permite realizar las conultas que necesitan autentificacion. POST PUT DELETE
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    #Busquedas personalizadas y por defecto
    #las personalizadas varian segun el criterio ingresado, y por defecto muestra todos los objetos


    def get(self, request, campo="",criterio=""):
        #try:
            if (len(campo)> 0 and len(criterio)> 0):
                if criterio == "id":
                    diagnosticos = Diagnostico.objects.filter(id=campo).values()
                    if diagnosticos is not None:
                        diagnosticos_values = []
                        for diagnostico in diagnosticos:
                            diagnostico_dict = {
                                'id': diagnostico['id'],
                                'descripcion': diagnostico['descripcion'],
                                'idEnfermedades':{}
                            }
                            enfermedades = DiagnosticoDetalle.objects.filter(idDiagnostico = diagnostico['id']).select_related('idEnfermedad')
                            for enfermedad in enfermedades:
                                enfermedad_dict = {
                                    'id': enfermedad.idEnfermedad.id,
                                    'nombre': enfermedad.idEnfermedad.nombre
                                }
                                diagnostico_dict['idEnfermedades'][enfermedad.idEnfermedad.id] = enfermedad_dict
                            diagnosticos_values.append(diagnostico_dict)
                        context = {
                            'message': "Consulta exitosa",
                            'diagnosticos': diagnosticos_values
                        }
                        return JsonResponse(context)
                    else:
                        context = {
                            'message': "No se encontraron los datos",
                            'diagnosticos': diagnosticos_values
                        }
                        return JsonResponse(context)
                elif criterio == "descripcion":
                    diagnosticos = Diagnostico.objects.filter(descripcion=campo).values()
                    if diagnosticos is not None:
                        diagnosticos_values = []
                        for diagnostico in diagnosticos:
                            diagnostico_dict = {
                                'id': diagnostico['id'],
                                'descripcion': diagnostico['descripcion'],
                                'idEnfermedades':{}
                            }
                            enfermedades = DiagnosticoDetalle.objects.filter(idDiagnostico = diagnostico['id']).select_related('idEnfermedad')
                            for enfermedad in enfermedades:
                                enfermedad_dict = {
                                    'id': enfermedad.idEnfermedad.id,
                                    'nombre': enfermedad.idEnfermedad.nombre
                                }
                                diagnostico_dict['idEnfermedades'][enfermedad.idEnfermedad.id] = enfermedad_dict
                            diagnosticos_values.append(diagnostico_dict)
                        context = {
                            'message': "Consulta exitosa",
                            'diagnosticos': diagnosticos_values
                        }
                        return JsonResponse(context)
                    else:
                        context = {
                            'message': "No se encontraron los datos",
                            'diagnosticos': diagnosticos_values
                        }
                        return JsonResponse(context)
            else:
                diagnosticos = Diagnostico.objects.values()
                if diagnosticos is not None:
                    diagnosticos_values = []
                    for diagnostico in diagnosticos:
                        diagnostico_dict = {
                            'id': diagnostico['id'],
                            'descripcion': diagnostico['descripcion'],
                            'idEnfermedades':{}
                        }
                        enfermedades = DiagnosticoDetalle.objects.filter(idDiagnostico = diagnostico['id']).select_related('idEnfermedad')
                        for enfermedad in enfermedades:
                            enfermedad_dict = {
                                'id': enfermedad.idEnfermedad.id,
                                'nombre': enfermedad.idEnfermedad.nombre
                            }
                            diagnostico_dict['idEnfermedades'][enfermedad.idEnfermedad.id] = enfermedad_dict
                        diagnosticos_values.append(diagnostico_dict)
                    context = {
                        'message': "Consulta exitosa",
                        'diagnosticos': diagnosticos_values
                    }
                    return JsonResponse(context)
                else:
                    context = {
                        'message': "No se encontraron los datos",
                        'diagnosticos': diagnosticos_values
                    }
                    return JsonResponse(context)
            return JsonResponse(context)




            
#Agregar un registro de cargos
    def post(self, request):
        jd=json.loads(request.body)
        if len(jd['descripcion']) <= 0:
            mensaje_post = {'message': "La descripción esta vacía."}
        
        elif len(jd['descripcion']) < 3:
            mensaje_post = {'message': "La descripcion debe tener mas de 3 caracteres."}
        elif not validar_cadena_espacios(jd['descripcion']):
            mensaje_post = {'message': "No se permiten mas de un espacio consecutivo."}
        elif validar_cadena_repeticion(jd['descripcion']):
            mensaje_post = {'message': "No se permiten mas de dos caracteres consecutivos del mismo tipo."}
        elif len(jd['descripcion']) > 100:
            mensaje_post = {'message': "El descripcion debe tener menos de 100 caracteres."}
        elif jd['idEnfermedades'] is None :
            mensaje_post = {'message': "No hay Enfermedades relacionados o estan vacíos."}
        elif jd['idEnfermedades'] == []:
            mensaje_post = {'message': "No hay Enfermedades relacionados o estan vacíos."}
        elif len(jd['idEnfermedades']) < 0:
            mensaje_post = {'message': "No hay Enfermedades relacionados o estan vacíos."}
        else:
            diagnostico= Diagnostico.objects.create(descripcion=jd['descripcion'])
            for enfermedad in jd ['idEnfermedades']:
                idenfermedad =instanciar_enfermedad(int(enfermedad['id']))
                DiagnosticoDetalle.objects.create(idDiagnostico=diagnostico,idEnfermedad=idenfermedad)
                mensaje_post={'message':"Registro exitoso"}
        return JsonResponse(mensaje_post)
            



#Actualizar un registro de cargos
    def put(self, request,id):
        jd=json.loads(request.body)
        mensaje_put = list(Diagnostico.objects.filter(id=id).values())
        if len(mensaje_put) > 0:
            diagnostico_actualizar=Diagnostico.objects.get(id=id)
            if len(jd['descripcion']) <= 0:
                mensaje_put = {'message': "El descripcion esta vacío."}
            elif len(jd['descripcion']) < 3:
                mensaje_put = {'message': "El descripcion debe tener mas de 3 caracteres."}
            elif not validar_cadena_espacios(jd['descripcion']):
                mensaje_put = {'message': "No se permiten mas de un espacio consecutivo."}
            elif validar_cadena_repeticion(jd['descripcion']):
                mensaje_put = {'message': "No se permiten mas de dos caracteres consecutivos del mismo tipo."}
            elif len(jd['descripcion']) > 100:
                mensaje_put = {'message': "El descripcion debe tener menos de 100 caracteres."}
            elif jd['idEnfermedades'] == []:
                mensaje_put = {'message': "No hay enfermedades relacionados o estan vacíos."}
            elif len(jd['idEnfermedades']) < 0:
                mensaje_put = {'message': "No hay enfermedades relacionados o estan vacíos."}
            else:
                enfermedades = DiagnosticoDetalle.objects.filter(idDiagnostico=id).values('idEnfermedad')
                ids_enfermedades = [{'id': enfermedad['idEnfermedad']} for enfermedad in enfermedades]
                ids_actualizar = [{'id': enfermedad['id']} for enfermedad in jd['idEnfermedades']]

                # obtener los IDs que están en idSintomas pero no en ids_lista
                ids_faltantes = [diagnostico['id'] for diagnostico in ids_actualizar if diagnostico not in ids_enfermedades]

                # obtener los IDs que están en ids_lista pero no en idSintomas
                ids_extra = [enfermedad['id'] for enfermedad in ids_enfermedades if enfermedad not in ids_actualizar]

                # verificar si la lista de IDs faltantes no está vacía
                if len(ids_faltantes) > 0:
                    # imprimir un mensaje para cada ID faltante
                    for id_faltante in ids_faltantes:
                        #Crea un detalle por cada id que no se encuentre en la lista de detalles pero si en la nueva lista
                        DiagnosticoDetalle.objects.create(idDiagnostico=diagnostico_actualizar, idEnfermedad = instanciar_enfermedad(id_faltante))
                # verificar si la lista de IDs extra no está vacía
                if len(ids_extra) > 0:
                    # imprimir un mensaje para cada ID extra
                    for id_extra in ids_extra:
                        #Borra los detalles que se encuentran en la lista de detalles pero que no estan en la nueva lista
                        reg_del = DiagnosticoDetalle.objects.filter(idDiagnostico=diagnostico_actualizar, idEnfermedad = instanciar_enfermedad(id_extra))
                        reg_del.delete()


                diagnostico_actualizar.descripcion = jd['descripcion']
                diagnostico_actualizar.save()
                mensaje_put = {'message': "La actualización fue exitosa."}
        return JsonResponse(mensaje_put)
        
        
#Eliminar un registro de cargos
    def delete(self, request,id):
        diagnostico = list(Diagnostico.objects.filter(id=id).values())
        detalles = list(DiagnosticoDetalle.objects.filter(idDiagnostico=id).values())
        if len(diagnostico) > 0 and len(detalles) > 0:
            #Se eliminan los detalles
            for detalle in detalles:
                DiagnosticoDetalle.objects.filter(id=detalle['id']).delete()
            #Se elimina el diagnostico
            Diagnostico.objects.filter(id=id).delete()
            datos = {'message':"Registro Eliminado"}
        else:
            datos = {'message':"No se encontraró el registro", 'diagnostico':[]}
        return JsonResponse(datos)



def validar_cadena_repeticion(cadena):
    patron = r'([a-zA-Z])\1\1'
    return bool(re.search(patron, cadena))

def validar_cadena_espacios(cadena):
    patron = r'^[^ ]+(?: {0,1}[^ ]+)*$'
    return bool(re.match(patron,cadena))

def validar_detalle_existente(idDiagnostico,idEnfermedad):
    if (idDiagnostico and idEnfermedad):
        registros = DiagnosticoDetalle.objects.filter(idDiagnostico=idDiagnostico, idEnfermedad=idEnfermedad)
        if registros:
            return False
        else:
            return True

def instanciar_enfermedad(id):
    if (id > 0):
        enfermedad = Enfermedad.objects.filter(id=id).last()
    if enfermedad:
        return enfermedad

def instanciar_enfermedades(nombre):
    if (nombre):
        enfermedad = Enfermedad.objects.filter(nombre=nombre).last()
    if enfermedad:
        return enfermedad
