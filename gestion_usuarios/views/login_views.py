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
class LoginViews(View):
    #Este metodo permite realizar las conultas que necesitan autentificacion. POST PUT DELETE
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        jd=json.loads(request.body)
        username = jd['username']
        password = jd['password']
        usuario = Usuario.objects.filter(nombreUsuario=username)
        #user = list(usuario)
        mensaje = {}
        if len(usuario) > 0:
            if usuario[0].bloqueado == 1:
                mensaje = {'mensaje':"El usuario esta bloqueado, contacte al administrador"}
            elif usuario[0].activo == 0:
                mensaje = {'mensaje':"El usuario esta desactivado, contacte al administrador"}
            else:
                if verificar_password(password, usuario[0].password):
                    mensaje = {'mensaje':"Inicio Exitoso"}
                    usuario[0].intentos = 0
                    usuario[0].activo = 1
                    usuario[0].sesion = 1
                else:
                    mensaje = {'mensaje':"Contraseña Incorrecta"}
                    usuario[0].intentos += 1
                    if usuario[0].intentos == 3:
                        mensaje = {'mensaje':"El usuario ha sido bloqueado, contacte al administrador"}
                        usuario[0].bloqueado = 1
                        usuario[0].activo = 0 
                        usuario[0].sesion = 0            
        else:
            mensaje = {'mensaje':"No se encontro el usuario"}
        if usuario:
            usuario[0].save()
        return JsonResponse(mensaje)
    
    def put(self, request,id):
        usuario = Usuario.objects.get(id=id)
        usuario.sesion = 0
        usuario.save()
        mensaje = {'mensaje':"Exito"}
        return JsonResponse(mensaje)

def verificar_password(password, encript):
    contexto = CryptContext(
        schemes=["pbkdf2_sha256"],
        default="pbkdf2_sha256",
        pbkdf2_sha256__rounds=10
    )
    validacion = contexto.verify(password, encript)
    return validacion
