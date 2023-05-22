from django.http.response import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from passlib.context import CryptContext
import json
import re
from ..models import *
from django.views.decorators.http import require_http_methods

@method_decorator(require_http_methods(['POST','PUT','GET','DELETE']), name='dispatch')
class UsuarioViews(View):
    #Este metodo permite realizar las conultas que necesitan autentificacion. POST PUT DELETE
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    #Busquedas personalizadas y por defecto
    #las personalizadas varian segun el criterio ingresado, y por defecto muestra todos los objetos
    def get(self, request, campo="",criterio=""):
        if (len(campo)> 0 and len(criterio)> 0):
            if criterio == "id":
                usuariosr = list(Usuario.objects.filter(id=campo).values())
                if len(usuariosr) > 0:
                    usuariosr = usuariosr
                    usuariosr = {'message': "Consulta exitosa", 'usuariosr': usuariosr}
                else:
                    usuariosr = {'message': "No se encontraron los datos", 'usuariosr': []} 
                    return JsonResponse(usuariosr)
            elif criterio == "nombre":
                usuariosr = list(Usuario.objects.filter(nombreUsuario=campo).values())
                if len(usuariosr) > 0:
                    usuariosr = usuariosr
                    usuariosr = {'message': "Consulta exitosa", 'usuariosr': usuariosr}
                else:
                    usuariosr = {'message': "No se encontraron los datos", 'usuariosr': []} 
                    return JsonResponse(usuariosr)
            elif criterio == "sesion":
                usuariosr = list(Usuario.objects.filter(sesion=campo).values())
                if len(usuariosr) > 0:
                    usuariosr = usuariosr
                    usuariosr = {'message': "Consulta exitosa", 'usuariosr': usuariosr}
                else:
                    usuariosr = {'message': "No se encontraron los datos", 'usuariosr': []} 
                    return JsonResponse(usuariosr)
        else:
            usuariosr = list(Usuario.objects.values())
            if len(usuariosr) > 0:
                usuariosr = {'message': "Consulta exitosa", 'usuariosr': usuariosr}
            else:
                usuariosr = {'message': "No se encontraron los datos", 'usuariosr': []} 
        return JsonResponse(usuariosr)

#Agregar un registro de cargos
    def post(self, request):
        jd=json.loads(request.body)
        simbolos =['$', '@', '#', '%', '!', '¡','?', '¿']
        if len(jd['nombreUsuario']) <= 0:
            usuariosr = {'message': "El nombre esta vacío."}
        elif len(jd['nombreUsuario']) < 5:
            usuariosr = {'message': "El nombre debe tener mas de 5 caracteres."}
        elif not validar_cadena_espacios(jd['nombreUsuario']):
            usuariosr = {'message': "No se permiten mas de un espacio consecutivo."}
        elif validar_cadena_repeticion(jd['nombreUsuario']):
            usuariosr = {'message': "No se permiten mas de dos caracteres consecutivos del mismo tipo."}
        elif len(jd['nombreUsuario']) > 50:
            usuariosr = {'message': "El nombre debe tener menos de 50 caracteres."}
        elif (validar_usuario_repetido(jd['nombreUsuario'])):
            usuariosr = {'message': "El usuario ya existe."}
        elif len(jd['password']) <= 0:
            usuariosr = {'message': "La contraseña esta vacía."}
        elif len(jd['password']) < 7:
            usuariosr = {'message':'La contraseña debe tener mas de 7 caracteres' } 
        elif len(jd['password']) > 15:
            usuariosr = {'message':'La contraseña debe tener menos de 16 caracteres'}       
        elif not any(char.isdigit() for char in jd['password']):
            usuariosr = {'message':'La contraseña debe tener al menos un numero'}
        elif not any(char.isupper() for char in jd['password']):
            usuariosr = {'message':'La contraseña debe tener al menos una letra mayuscula'}      
        elif not any(char.islower() for char in jd['password']):
            usuariosr = {'message':'La contraseña debe tener al menos una letra minuscula'}   
        elif not any(char in simbolos for char in jd['password']):
            usuariosr = {'message':'La contraseña debe contener algun caracter especial $@#'}
        elif not jd['password'] == jd['passwordc']:
            usuariosr = {'message':'Las contraseñas no coinciden'}    
        elif jd['activo'] < 0:
            usuariosr = {'message': "Activo debe ser positivo."}
        elif jd['activo'] > 1:
            usuariosr = {'message': "Activo unicamente puede ser 0 o 1."}
        elif jd['bloqueado'] < 0:
            usuariosr = {'message': "Bloqueado debe ser positivo."}
        elif jd['bloqueado'] > 1:
            usuariosr = {'message': "Bloqueado unicamente puede ser 0 o 1."}
        else:
            usuariosr = {'message': "Registro Exitoso."}
            Usuario.objects.create(idEmpleado=instanciar_empleado(jd['idEmpleado']), nombreUsuario=jd['nombreUsuario'],password=encriptar_password(jd['password']), activo=jd['activo'], bloqueado=jd['bloqueado'],fechaCreacion=datetime.now(),fechaModificacion=datetime.now())
            usuariosr = {'message':"Registro Exitoso."}
        return JsonResponse(usuariosr)

#Actualizar un registro de cargos
    def put(self, request,id):
        jd=json.loads(request.body)
        usuariosr = list(Usuario.objects.filter(id=id).values())
        if len(usuariosr) > 0:
            usuario=Usuario.objects.get(id=id)
            simbolos =['$', '@', '#', '%', '!', '¡','?', '¿']
            if len(jd['nombreUsuario']) <= 0:
                usuariosr = {'message': "El nombre esta vacío."}
            elif not validar_cadena_espacios(jd['nombreUsuario']):
                usuariosr = {'message': "No se permiten mas de un espacio consecutivo."}
            elif validar_cadena_repeticion(jd['nombreUsuario']):
                usuariosr = {'message': "No se permiten mas de dos caracteres consecutivos del mismo tipo."}
            elif len(jd['nombreUsuario']) < 5:
                usuariosr = {'message': "El nombre debe tener mas de 5 caracteres."}
            elif len(jd['nombreUsuario']) > 50:
                usuariosr = {'message': "El nombre debe tener menos de 50 caracteres."}
            elif validar_usuario_repedio_empleado(jd['nombreUsuario'],jd['idEmpleado']):
                usuariosr = {'message': "El usuario ya existe."}
            elif len(jd['password']) <= 0:
                usuariosr = {'message': "La contraseña esta vacía."}
            elif len(jd['password']) < 7:
                usuariosr = {'message':'La contraseña debe tener mas de 7 caracteres' } 
            elif len(jd['password']) > 15:
                usuariosr = {'message':'La contraseña debe tener menos de 16 caracteres'}
            elif not jd['password'] == jd['passwordc']:
                usuariosr = {'message':'Las contraseñas no coinciden'}    
            elif not any(char.isdigit() for char in jd['password']):
                usuariosr = {'message':'La contraseña debe tener al menos un numero'}
            elif not any(char.isupper() for char in jd['password']):
                usuariosr = {'message':'La contraseña debe tener al menos una letra mayuscula'}      
            elif not any(char.islower() for char in jd['password']):
                usuariosr = {'message':'La contraseña debe tener al menos una letra minuscula'}   
            elif not any(char in simbolos for char in jd['password']):
                usuariosr = {'message':'La contraseña debe contener algun caracter especial $@#'}
            elif jd['activo'] < 0:
                usuariosr = {'message': "Activo debe ser positivo."}
            elif jd['activo'] > 1:
                usuariosr = {'message': "Activo unicamente puede ser 0 o 1."}
            elif jd['bloqueado'] < 0:
                usuariosr = {'message': "Bloqueado debe ser positivo."}
            elif jd['bloqueado'] > 1:
                usuariosr = {'message': "Bloqueado unicamente puede ser 0 o 1."}
            else:
                usuariosr = {'message': "Registro Exitoso."}
                usuario.idEmpleado = instanciar_empleado(jd['idEmpleado'])
                usuario.nombreUsuario = jd['nombreUsuario']
                usuario.password = encriptar_password(jd['password'])
                usuario.activo = jd['activo']
                usuario.bloqueado = jd['bloqueado']
                usuario.fechaModificacion = datetime.now()
                usuario.save()
                usuariosr = {'message': "La actualización fue exitosa."}
        return JsonResponse(usuariosr)
        
        
#Eliminar un registro de cargos
    def delete(self, request,id):
        usuariosr = list(Usuario.objects.filter(id=id).values())
        if len(usuariosr) > 0:
            Usuario.objects.filter(id=id).delete()
            datos = {'message':"Registro Eliminado"}
        else:
            datos = {'message':"No se encontraró el registro", 'usuariosr': []}
        return JsonResponse(datos)


def validar_usuario_repetido(nombreUsuario): 
    if (nombreUsuario):
        registros = Usuario.objects.filter(nombreUsuario=nombreUsuario)
        if len(registros) > 0:
            return True
        else:
            return False
    return False

def validar_usuario_repedio_empleado(nombreUsuario, idEmpleado):
    if (nombreUsuario and idEmpleado):
        usuarios = Usuario.objects.filter(nombreUsuario=nombreUsuario)
        x = 0
        for i in usuarios:
            if i.idEmpleado == idEmpleado and i.nombreUsuario == nombreUsuario:
                    x = x + 1
                    if x > 1:
                        return True
                    else:
                        return False
        
    


def instanciar_empleado(id):
    if (id>0):
        empleado = Empleado.objects.get(id=id)
        if empleado:
            return empleado

def encriptar_password(password):
    contexto = CryptContext(
        schemes=["pbkdf2_sha256"],
        default="pbkdf2_sha256",
        pbkdf2_sha256__rounds=10
    )
    encriptado = contexto.hash(password)
    return encriptado

def validar_cadena_repeticion(cadena):
    patron = r'([a-zA-Z])\1\1'
    return bool(re.search(patron, cadena))

def validar_cadena_espacios(cadena):
    patron = r'^[^ ]+(?: {0,1}[^ ]+)*$'
    return bool(re.match(patron,cadena))

    
         