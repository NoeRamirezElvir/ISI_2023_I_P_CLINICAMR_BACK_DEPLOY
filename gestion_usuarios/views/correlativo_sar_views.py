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
class CorrelativoViews(View):
    #Este metodo permite realizar las conultas que necesitan autentificacion. POST PUT DELETE
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    #Busquedas personalizadas y por defecto
    #las personalizadas varian segun el criterio ingresado, y por defecto muestra todos los objetos
    def get(self, request, campo="",criterio=""):
        if (len(campo)> 0 and len(criterio)> 0):
            if criterio == "id":
                correlativo = list(CorrelativoSar.objects.filter(id=campo).values())
                if len(correlativo) > 0:
                    correlativo = correlativo
                    correlativo = {'message': "Consulta exitosa", 'correlativo': correlativo}
                else:
                    correlativo = {'message': "No se encontraron los datos", 'correlativo': []} 
                return JsonResponse(correlativo)
            elif criterio == "cai":
                correlativo = list(CorrelativoSar.objects.filter(cai=campo).values())
                if len(correlativo) > 0:
                    correlativo = correlativo
                    correlativo = {'message': "Consulta exitosa", 'correlativo': correlativo}
                else:
                    correlativo = {'message': "No se encontraron los datos", 'correlativo': []} 
                return JsonResponse(correlativo)
            elif criterio == "activo":
                correlativo = list(CorrelativoSar.objects.filter(activo=campo).values())
                if len(correlativo) > 0:
                    correlativo = correlativo
                    correlativo = {'message': "Consulta exitosa", 'correlativo': correlativo}
                else:
                    correlativo = {'message': "No se encontraron los datos", 'correlativo': []} 
                return JsonResponse(correlativo)
        else:
            correlativo = list(CorrelativoSar.objects.values())
            if len(correlativo) > 0:
                correlativo = {'message': "Consulta exitosa", 'correlativo': correlativo}
            else:
                correlativo = {'message': "No se encontraron los datos", 'correlativo': []} 
        return JsonResponse(correlativo)

#Agregar un registro de cargos
    def post(self, request):
        jd=json.loads(request.body)
        rsp_fechaLimite = date.fromisoformat(jd['fechaLimiteEmision'])
        if len(jd['cai']) <= 0:
            mensaje_post = {'message': "El cai esta vacío."}
        elif len(jd['cai']) < 10:
            mensaje_post = {'message': "El cai debe tener mas de 10 digitos."}
        elif CorrelativoSar.objects.filter(cai=(jd['cai'])).exists():
            mensaje_post = {'message': "El cai ya esta en uso."}
        elif not validar_cai(jd['cai']):
            mensaje_post = {'message': "La cadena de texto debe tener 36 caracteres, contar con cuatro guines(-), unicamente numeros y letras"}
        elif not validar_cadena_espacios(jd['cai']):
            mensaje_post = {'message': "No se permiten espacios[cai]."}
        elif len(jd['cai']) > 50:
            mensaje_post = {'message': "El cai debe tener menos de 50 digitos."}

        elif (jd['rangoInicial']) < 0:
            mensaje_post = {'message': "El rango inicial debe ser mayor a cero."}
        elif (jd['rangoInicial']) > 99999999:
            mensaje_post = {'message': "El rango inicial es muy alto."}
        elif (jd['rangoInicial']) >= (jd['rangoFinal']):
            mensaje_post = {'message': "El rango inicial debe ser menor al rango final."}

        elif (jd['rangoFinal']) < 0:
            mensaje_post = {'message': "El rango final debe ser mayor a cero."}
        elif (jd['rangoFinal']) > 99999999:
            mensaje_post = {'message': "El rango final es muy alto."}
        elif (jd['rangoFinal']) <= (jd['rangoInicial']):
            mensaje_post = {'message': "El rango final debe ser mayor al rango final."}

        elif (rsp_fechaLimite) is None or isinstance(rsp_fechaLimite, str):
            mensaje_post = {'message': "La fecha limite esta vacía"}
        elif (rsp_fechaLimite) == date.today():
            mensaje_post = {'message': "La fecha limite no puede ser igual a la fecha fecha actual"}
        elif (rsp_fechaLimite) < date.today():
            mensaje_post = {'message': "La fecha limite debe ser mayor a la actual"}

        else:
            CorrelativoSar.objects.create(cai=(jd['cai']).strip(),
                                          rangoInicial=jd['rangoInicial'],
                                          rangoFinal=jd['rangoFinal'],
                                          consecutivo=jd['rangoInicial'],
                                          fechaInicio = date.today(),
                                          fechaLimiteEmision=jd['fechaLimiteEmision'],
                                          )
            mensaje_post = {'message':"Registro Exitoso."}
        return JsonResponse(mensaje_post)

#Actualizar un registro de cargos
    def put(self, request,id):
        jd=json.loads(request.body)
        mensaje_put = list(CorrelativoSar.objects.filter(id=id).values())
        if len(mensaje_put) > 0:
            rsp_fechaLimite = date.fromisoformat(jd['fechaLimiteEmision'])
            correlativo_actualizar=CorrelativoSar.objects.get(id=id)
            if len(jd['cai']) <= 0:
                mensaje_put = {'message': "El cai esta vacío."}
            elif len(jd['cai']) < 10:
                mensaje_put = {'message': "El cai debe tener mas de 10 digitos."}
            elif CorrelativoSar.objects.filter(cai=len(jd['cai'])).exists():
                mensaje_put = {'message': "El cai ya esta en uso."}
            elif not validar_cai(jd['cai']):
                mensaje_put = {'message': "La cadena de texto debe tener 36 caracteres, contar con cuatro guines(-), unicamente numeros y letras"}
            elif not validar_cadena_espacios(jd['cai']):
                mensaje_put = {'message': "No se permiten espacios[cai]."}
            elif len(jd['cai']) > 50:
                mensaje_put = {'message': "El cai debe tener menos de 50 digitos."}

            elif (jd['rangoInicial']) < 0:
                mensaje_put = {'message': "El rango inicial debe ser mayor a cero."}
            elif (jd['rangoInicial']) > 99999999:
                mensaje_put = {'message': "El rango inicial es muy alto."}
            elif (jd['rangoInicial']) >= (jd['rangoFinal']):
                mensaje_put = {'message': "El rango inicial debe ser menor al rango final."}

            elif (jd['rangoFinal']) < 0:
                mensaje_put = {'message': "El rango final debe ser mayor a cero."}
            elif (jd['rangoFinal']) > 99999999:
                mensaje_put = {'message': "El rango final es muy alto."}
            elif (jd['rangoFinal']) <= (jd['rangoInicial']):
                mensaje_put = {'message': "El rango final debe ser mayor al rango final."}

            elif (rsp_fechaLimite) is None or isinstance(rsp_fechaLimite, str):
                mensaje_put = {'message': "La fecha limite esta vacía"}
            elif (rsp_fechaLimite) == date.today():
                mensaje_put = {'message': "La fecha limite no puede ser igual a la fecha fecha actual"}
            elif (rsp_fechaLimite) < date.today():
                mensaje_put = {'message': "La fecha limite debe ser mayor a la actual"}
            elif(int(jd['consecutivo']) < jd['rangoInicial']):
                mensaje_put = {'message': "El consecutivo debe ser mayor o igual al rango inicial"}
            elif(int(jd['consecutivo']) > jd['rangoFinal']):
                mensaje_put = {'message': "El consecutivo debe ser menor o igual al rango final"}
            else:
                correlativo_actualizar.consecutivo=int(jd['consecutivo'])
                correlativo_actualizar.activo = 1
                correlativo_actualizar.cai=(jd['cai']).strip()
                correlativo_actualizar.rangoInicial=jd['rangoInicial']
                correlativo_actualizar.rangoFinal=jd['rangoFinal']
                correlativo_actualizar.fechaLimiteEmision=jd['fechaLimiteEmision']

                correlativo_actualizar.save()
                mensaje_put = {'message': "La actualización fue exitosa."}
        return JsonResponse(mensaje_put)
        
        
#Eliminar un registro de cargos
    def delete(self, request,id):
        correlativo_delete = list(CorrelativoSar.objects.filter(id=id).values())
        if len(correlativo_delete) > 0:
            CorrelativoSar.objects.filter(id=id).delete()
            datos = {'message':"Registro Eliminado"}
        else:
            datos = {'message':"No se encontraró el registro", 'correlativo': []}
        return JsonResponse(datos)
    

def validar_cadena_repeticion(cadena):
    patron = r'([a-zA-Z])\1\1'
    return bool(re.search(patron, cadena))

def validar_cadena_espacios(cadena):
    patron = r'^[^ ]+(?: {0,0}[^ ]+)*$'
    return bool(re.match(patron,cadena))

def validar_cai(cadena):
    patron = r'^[a-z0-9]{8}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{12}$'
    return bool(re.match(patron,cadena))
