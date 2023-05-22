from django.http.response import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
import re
from ..models import *
from django.views.decorators.http import require_http_methods

@method_decorator(require_http_methods(['POST','PUT','GET','DELETE']), name='dispatch')
class autorizarView(View):
    #Este metodo permite realizar las conultas que necesitan autentificacion. POST PUT DELETE
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    #Busquedas personalizadas y por defecto
    #las personalizadas varian segun el criterio ingresado, y por defecto muestra todos los objetos
    def get(self, request, campo="",criterio=""):
        if (len(campo)> 0 and len(criterio)> 0):
            if criterio == "id":
                autorizar = list(AutorizacionPaciente.objects.filter(id=campo).values())
                if len(autorizar) > 0:
                    autorizar = autorizar
                    autorizar = {'message': "Consulta exitosa", 'autorizar': autorizar}
                else:
                    autorizar = {'message': "No se encontraron los datos", 'autorizar': []} 
                    return JsonResponse(autorizar)
            elif criterio == "motivos":
                autorizar = list(AutorizacionPaciente.objects.filter(motivos=campo).values())
                if len(autorizar) > 0:
                    autorizar = autorizar
                    autorizar = {'message': "Consulta exitosa", 'autorizar': autorizar}
                else:
                    autorizar = {'message': "No se encontraron los datos", 'autorizar': []} 
                    return JsonResponse(autorizar)
        else:
            autorizar = list(AutorizacionPaciente.objects.values())
            if len(autorizar) > 0:
                autorizar = {'message': "Consulta exitosa", 'autorizar': autorizar}
            else:
                autorizar = {'message': "No se encontraron los datos", 'autorizar': []} 
        return JsonResponse(autorizar)

#Agregar un registro de autorizar
    def post(self, request):
        jd=json.loads(request.body)

        if len(jd['motivos']) <= 0:
            autorizar = {'message': "El motivos esta vacío."}

        elif len(jd['motivos']) < 4:
            autorizar = {'message': "El motivos debe tener mas de 4 caracteres."}
        elif not validar_cadena_espacios(jd['motivos']):
            autorizar = {'message': "No se permiten mas de un espacio consecutivo."}
        elif validar_cadena_repeticion(jd['motivos']):
            autorizar = {'message': "No se permiten mas de dos caracteres consecutivos del mismo tipo."}
        elif len(jd['motivos']) > 50:
            autorizar = {'message': "El motivos debe tener menos de 50 caracteres."}
        
        elif jd['confirmacion'] < 0:
            autorizar = {'message': "confirmacion debe ser positivo."}
        elif jd['confirmacion'] > 1:
            autorizar = {'message': "confirmacion debe unicamente puede ser 0 o 1."}
        else:
            AutorizacionPaciente.objects.create(motivos=jd['motivos'],confirmacion=jd['confirmacion'])
            autorizar = {'message':"Registro Exitoso."}
        return JsonResponse(autorizar)

#Actualizar un registro de autorizar
    def put(self, request,id):
        jd=json.loads(request.body)
        autorizar = list(AutorizacionPaciente.objects.filter(id=id).values())
        if len(autorizar) > 0:
            atorizacion= AutorizacionPaciente.objects.get(id=id)
            if len(jd['motivos']) <= 0:
                autorizar = {'message': "El motivos esta vacío."}
            elif len(jd['motivos']) < 4:
                autorizar = {'message': "El motivos debe tener mas de 4 caracteres."}
            
            elif len(jd['motivos']) > 50:
                autorizar = {'message': "El motivos debe tener menos de 50 caracteres."}
            elif jd['confirmacion'] < 0:
                autorizar = {'message': "confirmacion debe ser positivo."}
            elif jd['confirmacion'] > 1:
                autorizar = {'message': "confirmacion debe unicamente puede ser 0 o 1."}
            else:
                autorizar = {'message': "Registro Exitoso."}
                atorizacion.motivos = jd['motivos']
                atorizacion.confirmacion = jd['confirmacion']
                atorizacion.save()
                autorizar = {'message': "La actualización fue exitosa."}
        return JsonResponse(autorizar)
        
        
#Eliminar un registro de autorizar
    def delete(self, request,id):
        autorizar = list(AutorizacionPaciente.objects.filter(id=id).values())
        if len(autorizar) > 0:
            AutorizacionPaciente.objects.filter(id=id).delete()
            datos = {'message':"Registro Eliminado"}
        else:
            datos = {'message':"No se encontraró el registro", 'autorizar': []}
        return JsonResponse(datos)
    


def validar_cadena_repeticion(cadena):
    patron = r'([a-zA-Z])\1\1'
    return bool(re.search(patron, cadena))

def validar_cadena_espacios(cadena):
    patron = r'^[^ ]+(?: {0,1}[^ ]+)*$'
    return bool(re.match(patron,cadena))
