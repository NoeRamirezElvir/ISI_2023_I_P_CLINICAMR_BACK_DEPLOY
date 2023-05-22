from django.http.response import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
import re
from ..models import *
from django.views.decorators.http import require_http_methods

@method_decorator(require_http_methods(['POST','PUT','GET','DELETE']), name='dispatch')
class ProveedorView(View):
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
                    proveedores = list(Proveedor.objects.filter(id=campo).values())
                    if len(proveedores) > 0:
                        proveedores = proveedores
                        proveedores = {'message': "Consulta exitosa", 'proveedores': proveedores}
                    else:
                        proveedores = {'message': "No se encontraron los datos", 'proveedores': []} 
                        return JsonResponse(proveedores)
                elif criterio == "nombre":
                    proveedores = list(Proveedor.objects.filter(nombre=campo).values())
                    if len(proveedores) > 0:
                        proveedores = proveedores
                        proveedores = {'message': "Consulta exitosa", 'proveedores': proveedores}
                    else:
                        proveedores = {'message': "No se encontraron los datos", 'proveedores': []} 
                        return JsonResponse(proveedores)
            else:
                proveedores = list(Proveedor.objects.values())
                if len(proveedores) > 0:
                    proveedores = {'message': "Consulta exitosa", 'proveedores': proveedores}
                else:
                    proveedores = {'message': "No se encontraron los datos", 'proveedores': []} 
            return JsonResponse(proveedores)
        except Exception as e:
            mensaje_delete = {'message': f"Error: {e}"}
            return JsonResponse(mensaje_delete)

#Agregar un registro de cargos
    def post(self, request):
        try:
            jd=json.loads(request.body)

            if len(jd['nombre']) <= 0:
                mensaje_post = {'message': "El nombre esta vacío."}
            elif len(jd['nombre']) < 3:
                mensaje_post = {'message': "El nombre debe tener mas de 3 caracteres."}
            elif not validar_cadena_espacios(jd['nombre']):
                mensaje_post = {'message': "No se permiten mas de un espacio consecutivo.[nombre]"}
            elif validar_cadena_repeticion(jd['nombre']):
                mensaje_post = {'message': "No se permiten mas de dos caracteres consecutivos del mismo tipo.[nombre]"}
            elif len(jd['nombre']) > 50:
                mensaje_post = {'message': "El nombre debe tener menos de 50 caracteres."}
            elif not len(str(jd['telefono'])) == 8:
                mensaje_post = {'message': "El teléfono debe tener 8 digitos."}
            elif (str(jd['telefono']))[0] == '1':
                mensaje_post = {'message': "El teléfono debe comenzar con 2, 3, 7, 8, 9."}
            elif (str(jd['telefono']))[0] == '4':
                mensaje_post = {'message': "El teléfono debe comenzar con 2, 3, 7, 8, 9."}
            elif (str(jd['telefono']))[0] == '5':
                mensaje_post = {'message': "El teléfono debe comenzar con 2, 3, 7, 8, 9."}
            elif (str(jd['telefono']))[0] == '6':
                mensaje_post = {'message': "El teléfono debe comenzar con 2, 3, 7, 8, 9."}
            elif (str(jd['telefono']))[0] == '0':
                mensaje_post = {'message': "El teléfono debe comenzar con 2, 3, 7, 8, 9."}
            elif (validar_telefono_repetido(jd['telefono'])):
                mensaje_post = {'message': "El telefono ya esta en uso."}
            elif len(jd['correo']) <= 0:
                mensaje_post = {'message': "El correo esta vacío."}
            elif len(jd['correo']) < 5:
                mensaje_post = {'message': "El correo debe tener más de 5 caracteres."}
            elif len(jd['correo']) > 30:
                mensaje_post = {'message': "El correo debe tener menos de 30 caracteres."}
            elif validar_correo(jd['correo']):
                mensaje_post = {'message': "El correo debe tener un formato válido, Ejemplo: ejemplo.correo@ejemplo.com"}
            elif (validar_correo_repetido(jd['correo'])):
                mensaje_post = {'message': "El correo ya esta en uso."}
            elif len(jd['direccion']) <= 0:
                mensaje_post = {'message': "La dirección esta vacía."}
            elif len(jd['direccion']) < 5:
                mensaje_post = {'message': "La dirección debe tener más de 5 caracteres."}
            elif len(jd['direccion']) > 50:
                mensaje_post = {'message': "La dirección debe tener menos de 50 caracteres."}
            elif not validar_cadena_espacios(jd['direccion']):
                mensaje_post = {'message': "No se permiten mas de un espacio consecutivo.[direccion]"}
            elif validar_cadena_repeticion(jd['direccion']):
                mensaje_post = {'message': "No se permiten mas de dos caracteres consecutivos del mismo tipo.[direccion]"} 
            else:
                mensaje_post = {'message': "Registro Exitoso."}
                Proveedor.objects.create(nombre=jd['nombre'],
                                        telefono=jd['telefono'],
                                        correo=jd['correo'],
                                        direccion=jd['direccion'])
                mensaje_post = {'message':"Registro Exitoso."}
            return JsonResponse(mensaje_post)
        except Exception as e:
            mensaje_delete = {'message': f"Error: {e}"}
            return JsonResponse(mensaje_delete)

#Actualizar un registro de cargos
    def put(self, request,id):
        try:
            jd=json.loads(request.body)
            mensaje_put = list(Proveedor.objects.filter(id=id).values())
            if len(mensaje_put) > 0:
                proveedor_actualizar=Proveedor.objects.get(id=id)
                if len(jd['nombre']) <= 0:
                    mensaje_put = {'message': "El nombre esta vacío."}
                elif len(jd['nombre']) < 3:
                    mensaje_put = {'message': "El nombre debe tener mas de 3 caracteres."}
                elif not validar_cadena_espacios(jd['nombre']):
                    mensaje_put = {'message': "No se permiten mas de un espacio consecutivo.[nombre]"}
                elif validar_cadena_repeticion(jd['nombre']):
                    mensaje_put = {'message': "No se permiten mas de dos caracteres consecutivos del mismo tipo.[nombre]"}
                elif len(jd['nombre']) > 50:
                    mensaje_put = {'message': "El nombre debe tener menos de 50 caracteres."}
                elif not len(str(jd['telefono'])) == 8:
                    mensaje_put = {'message': "El teléfono debe tener 8 digitos."}
                elif (str(jd['telefono']))[0] == '1':
                    mensaje_put = {'message': "El teléfono debe comenzar con 2, 3, 7, 8, 9."}
                elif (str(jd['telefono']))[0] == '4':
                    mensaje_put = {'message': "El teléfono debe comenzar con 2, 3, 7, 8, 9."}
                elif (str(jd['telefono']))[0] == '5':
                    mensaje_put = {'message': "El teléfono debe comenzar con 2, 3, 7, 8, 9."}
                elif (str(jd['telefono']))[0] == '6':
                    mensaje_put = {'message': "El teléfono debe comenzar con 2, 3, 7, 8, 9."}
                elif (str(jd['telefono']))[0] == '0':
                    mensaje_put = {'message': "El teléfono debe comenzar con 2, 3, 7, 8, 9."}
                elif len(jd['correo']) <= 0:
                    mensaje_put = {'message': "El correo esta vacío."}
                elif len(jd['correo']) < 5:
                    mensaje_put = {'message': "El correo debe tener más de 5 caracteres."}
                elif len(jd['correo']) > 30:
                    mensaje_put = {'message': "El correo debe tener menos de 30 caracteres."}
                elif validar_correo(jd['correo']):
                    mensaje_put = {'message': "El correo debe tener un formato válido, Ejemplo: ejemplo.correo@ejemplo.com"}
                elif len(jd['direccion']) <= 0:
                    mensaje_put = {'message': "La dirección esta vacía."}
                elif len(jd['direccion']) < 5:
                    mensaje_put = {'message': "La dirección debe tener más de 5 caracteres."}
                elif len(jd['direccion']) > 50:
                    mensaje_put = {'message': "La dirección debe tener menos de 50 caracteres."}
                elif not validar_cadena_espacios(jd['direccion']):
                    mensaje_put = {'message': "No se permiten mas de un espacio consecutivo.[direccion]"}
                elif validar_cadena_repeticion(jd['direccion']):
                    mensaje_put = {'message': "No se permiten mas de dos caracteres consecutivos del mismo tipo.[direccion]"}
                else:
                    proveedor_actualizar.nombre = jd['nombre']
                    proveedor_actualizar.telefono = jd['telefono']
                    proveedor_actualizar.correo = jd['correo']
                    proveedor_actualizar.direccion = jd['direccion']
                    proveedor_actualizar.save()
                    mensaje_put = {'message': "La actualización fue exitosa."}
            return JsonResponse(mensaje_put)
        except Exception as e:
            mensaje_put = {'message': f"Error: {e}"}
            return JsonResponse(mensaje_put)
        
        
#Eliminar un registro de cargos
    def delete(self, request,id):
            proveedores = list(Proveedor.objects.filter(id=id).values())
            if len(proveedores) > 0:
                Proveedor.objects.filter(id=id).delete()
                mensaje_delete = {'message':"Registro Eliminado"}
            else:
                mensaje_delete = {'message':"No se encontró el registro", 'proveedores': []}
            return JsonResponse(mensaje_delete)

def validar_telefono_repetido(valor): 
    if (valor):
        registros = Proveedor.objects.filter(telefono=valor)
        if len(registros) > 0:
            return True
        else:
            return False
    return False

def validar_correo_repetido(valor): 
    if (valor):
        registros = Proveedor.objects.filter(correo=valor)
        if len(registros) > 0:
            return True
        else:
            return False
    return False

def validar_correo(correo):
    expresion_regular = r"^[a-zA-Z0-9._%+-]{4,30}@[a-zA-Z0-9]{2,20}\.[a-zA-Z]{2,20}(?:\.[a-zA-Z]{2,20})?$"
    return re.match(expresion_regular, correo) is None

def validar_cadena_repeticion(cadena):
    patron = r'([a-zA-Z])\1\1'
    return bool(re.search(patron, cadena))

def validar_cadena_espacios(cadena):
    patron = r'^[^ ]+(?: {0,1}[^ ]+)*$'
    return bool(re.match(patron,cadena))
