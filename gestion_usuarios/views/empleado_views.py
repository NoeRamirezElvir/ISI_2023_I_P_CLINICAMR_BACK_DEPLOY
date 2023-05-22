
from django.http.response import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from datetime import  datetime,date,timedelta
import datetime
from time import strptime



import json
import re
from ..models import *

from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_http_methods

@method_decorator(require_http_methods(['POST','PUT','GET','DELETE']), name='dispatch')
class EmpleadoViews(View):
    #Este metodo permite realizar Els conultas que necesitan autentificacion. POST PUT DELETE
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    #Busquedas personalizadas y por defecto
    #las personalizadas varian segun el criterio ingresado, y por defecto muestra todos los objetos
    def get(self, request, campo="",criterio=""):
        if (len(campo)> 0 and len(criterio)> 0):
            if(criterio=="id"):
                empleados = list(Empleado.objects.filter(id=campo).values())
                if len(empleados) > 0:
                    empleados = empleados
                    empleados = {'message': "Consulta exitosa", 'empleados': empleados}
                else:
                    empleados = {'message': "No se encontraron los datos", 'empleados': []} 
                    return JsonResponse(empleados)
            elif(criterio=="nombre"):
                empleados = list(Empleado.objects.filter(nombre=campo).values())
                if len(empleados) > 0:
                    empleados = {'message': "Consulta exitosa", 'empleados': empleados}
                else:
                    empleados = {'message': "No se encontraron los datos", 'empleados': []} 
                    return JsonResponse(empleados)
            elif(criterio=="documento"):
                empleados = list(Empleado.objects.filter(documento=campo).values())
                if len(empleados) > 0:
                    empleados = {'message': "Consulta exitosa", 'empleados': empleados}
                else:
                    empleados = {'message': "No se encontraron los datos", 'empleados': []} 
                    return JsonResponse(empleados)
        else:
            empleados = list(Empleado.objects.values())
            if len(empleados) > 0:
                empleados = {'message': "Consulta exitosa", 'empleados': empleados}
            else:
                empleados = {'message': "No se encontraron los datos", 'empleados': []} 
        return JsonResponse(empleados)
    
#Agregar un registro de cargos
    def post(self, request):
        jd=json.loads(request.body)
        rsp_fechaNacimiento = datetime.date.fromisoformat(jd['fechaNacimiento'])
        if len(jd['nombre']) <= 0:
            empleados = {'message': "El nombre esta vacío."}
        elif len(jd['nombre']) < 3:
            empleados = {'message': "El nombre debe tener más de 3 caracteres."}
        elif not validar_cadena_espacios(jd['nombre']):
            empleados = {'message': "No se permiten mas de un espacio consecutivo."}
        elif validar_cadena_repeticion(jd['nombre']):
            empleados = {'message': "No se permiten mas de dos caracteres consecutivos del mismo tipo."}
        elif len(jd['nombre']) > 50:
            empleados = {'message': "El nombre debe tener menos de 50 caracteres."}
        elif len(jd['apellidos']) <= 0:
            empleados = {'message': "El apellido esta vacío."}
        elif len(jd['apellidos']) < 3:
            empleados = {'message': "El apellido debe tener más de 3 caracteres."}
        elif not validar_cadena_espacios(jd['apellidos']):
            empleados = {'message': "No se permiten mas de un espacio consecutivo."}
        elif validar_cadena_repeticion(jd['apellidos']):
            empleados = {'message': "No se permiten mas de dos caracteres consecutivos del mismo tipo."}      
        elif len(jd['apellidos']) > 50:
            empleados = {'message': "El apellido debe tener menos de 50 caracteres."}
        elif len(jd['email']) <= 0:
            empleados = {'message': "El email esta vacío."}
        elif len(jd['email']) < 5:
            empleados = {'message': "El email debe tener más de 5 caracteres."}
        elif len(jd['email']) > 30:
            empleados = {'message': "El email debe tener menos de 30 caracteres."}
        elif validar_email(jd['email']):
            empleados = {'message': "El email debe tener un formato válido."}

        elif validar_edad(jd['fechaNacimiento']):
            empleados = {'message': "El empleado no puede ser menor a 18 años."}
        
        elif len(str(jd['fechaNacimiento'])) <= 0:
            empleados = {'message': "La fecha de nacimiento esta vacía."}
        elif len(str(jd['fechaNacimiento'])) > 10:
            empleados = {'message': "La fecha de nacimiento debe tener menos de 10 caracteres."}
        elif (rsp_fechaNacimiento) is None:
            empleados = {'message': "La fecha esta vacía"}
        elif (rsp_fechaNacimiento) > datetime.date.today():
            empleados = {'message': "la fecha actual es incorrecta"}


        elif str(jd['telefono']).isalpha():
            empleados = {'message': "El teléfono solo puede contener numeros."}
        elif len(str(jd['telefono'])) <= 0:
            empleados = {'message': "El teléfono esta vacío."}
        elif len(str(jd['telefono'])) < 8:
            empleados = {'message': "El teléfono debe tener más de 8 caracteres."}
        elif len(str(jd['telefono'])) > 15:
            empleados = {'message': "El teléfono debe tener menos de 15 caracteres."}
        elif (str(jd['telefono']))[0] == '1':
            empleados = {'message': "El teléfono debe comenzar con 2, 3, 7, 8, 9."}
        elif (str(jd['telefono']))[0] == '4':
            empleados = {'message': "El teléfono debe comenzar con 2, 3, 7, 8, 9."}
        elif (str(jd['telefono']))[0] == '5':
            empleados = {'message': "El teléfono debe comenzar con 2, 3, 7, 8, 9."}
        elif (str(jd['telefono']))[0] == '6':
            empleados = {'message': "El teléfono debe comenzar con 2, 3, 7, 8, 9."}
        elif (str(jd['telefono']))[0] == '0':
            empleados = {'message': "El teléfono debe comenzar con 2, 3, 7, 8, 9."}
        elif len(jd['direccion']) <= 0:
            empleados = {'message': "La dirección esta vacía."}
        elif len(jd['direccion']) < 5:
            empleados = {'message': "La dirección debe tener más de 5 caracteres."}
        elif len(jd['direccion']) > 50:
            empleados = {'message': "La dirección debe tener menos de 50 caracteres."}
        elif (jd['idTipoDocumentos']) <= 0:
            empleados = {'message': "El tipo de documento esta vacío."}
        elif validar_id_documento(jd['idTipoDocumentos']):
            empleados = {'message': "El id de documento no existe."}
        elif len(jd['documento']) <= 0:
            empleados = {'message': "El documento esta vacío."}
        elif (validar_documento_repetido(jd['documento'])):
            empleados = {'message': "El documento esta en uso."}
        elif not len(jd['documento']) == (validar_documento(jd['idTipoDocumentos'])):
            empleados = {'message': "El documento debe cumplir la longitud asignada."}
        elif (jd['idCargoEmpleado']) <= 0:
            empleados = {'message': "El cargo esta vacío."}
        elif jd['activo'] < 0:
            empleados = {'message': "Activo debe ser positivo."}
        elif jd['activo'] > 1:
            empleados = {'message': "Activo unicamente puede ser 0 o 1."}
        else:
            empleados = {'message': "Registro Exitoso."}
            Empleado.objects.create(nombre=jd['nombre'], apellidos=jd['apellidos'],
                                    fechaNacimiento=(jd['fechaNacimiento']),
                                    email=jd['email'],
                                    telefono=str(jd['telefono']),
                                    direccion=jd['direccion'],
                                    idTipoDocumentos=(instanciar_documento(jd['idTipoDocumentos'])),
                                    documento=jd['documento'],
                                    idEspecialidadMedico=instanciar_especialidad(jd['idEspecialidadMedico']),
                                    idCargoEmpleado=instanciar_cargo(jd['idCargoEmpleado']),
                                    activo=jd['activo'])
            
            empleados = {'message':"Registro Exitoso."}
        return JsonResponse(empleados)

#Actualizar un registro de cargos
    def put(self, request,id):
        jd=json.loads(request.body)
        
        empleados = list(Empleado.objects.filter(id=id).values())
        rsp_fechaNacimiento = datetime.date.fromisoformat(jd['fechaNacimiento'])
        if len(empleados) > 0:
            empleado=Empleado.objects.get(id=id)
            if len(jd['nombre']) <= 0:
                empleados = {'message': "El nombre esta vacío."}
            elif len(jd['nombre']) < 3:
                empleados = {'message': "El nombre debe tener más de 3 caracteres."}
            elif not validar_cadena_espacios(jd['nombre']):
                empleados = {'message': "No se permiten mas de un espacio consecutivo."}
            elif validar_cadena_repeticion(jd['nombre']):
                empleados = {'message': "No se permiten mas de dos caracteres consecutivos del mismo tipo."}      
            elif len(jd['nombre']) > 50:
                empleados = {'message': "El nombre debe tener menos de 50 caracteres."}
            elif len(jd['apellidos']) <= 0:
                empleados = {'message': "El apellido esta vacío."}
            elif len(jd['apellidos']) < 3:
                empleados = {'message': "El apellido debe tener más de 3 caracteres."}
            elif not validar_cadena_espacios(jd['apellidos']):
                empleados = {'message': "No se permiten mas de un espacio consecutivo."}
            elif validar_cadena_repeticion(jd['apellidos']):
                empleados = {'message': "No se permiten mas de dos caracteres consecutivos del mismo tipo."}               
            elif len(jd['apellidos']) > 50:
                empleados = {'message': "El apellido debe tener menos de 50 caracteres."}
            elif len(jd['email']) <= 0:
                empleados = {'message': "El email esta vacío."}
            elif len(jd['email']) < 5:
                empleados = {'message': "El email debe tener más de 5 caracteres."}
            elif len(jd['email']) > 30:
                empleados = {'message': "El email debe tener menos de 30 caracteres."}
            elif validar_email(jd['email']):
                empleados = {'message': "El email debe tener un formato válido."}

            
            elif validar_edad(jd['fechaNacimiento']):
                empleados = {'message': "El empleado es menora 18 años."}
            elif len(str(jd['fechaNacimiento'])) <= 0:
                empleados = {'message': "La fecha de nacimiento esta vacía."}
            elif len(str(jd['fechaNacimiento'])) > 10:
                empleados = {'message': "La fecha de nacimiento debe tener menos de 10 caracteres."}
            elif (rsp_fechaNacimiento) is None:
                empleados = {'message': "La fecha esta vacía"}
            elif (rsp_fechaNacimiento) > datetime.date.today():
                empleados = {'message': "la fecha actual es incorrecta"}

            
            
            elif str(jd['telefono']).isalpha():
                empleados = {'message': "El teléfono solo puede contener numeros."}
            elif len(str(jd['telefono'])) <= 0:
                empleados = {'message': "El teléfono esta vacío."}
            elif len(str(jd['telefono'])) < 8:
                empleados = {'message': "El teléfono debe tener más de 8 caracteres."}
            elif len(str(jd['telefono'])) > 15:
                empleados = {'message': "El teléfono debe tener menos de 15 caracteres."}
            elif (str(jd['telefono']))[0] == '1':
                empleados = {'message': "El teléfono debe comenzar con 2, 3, 7, 8, 9."}
            elif (str(jd['telefono']))[0] == '4':
                empleados = {'message': "El teléfono debe comenzar con 2, 3, 7, 8, 9."}
            elif (str(jd['telefono']))[0] == '5':
                empleados = {'message': "El teléfono debe comenzar con 2, 3, 7, 8, 9."}
            elif (str(jd['telefono']))[0] == '6':
                empleados = {'message': "El teléfono debe comenzar con 2, 3, 7, 8, 9."}
            elif (str(jd['telefono']))[0] == '0':
                empleados = {'message': "El teléfono debe comenzar con 2, 3, 7, 8, 9."}
            elif len(jd['direccion']) <= 0:
                empleados = {'message': "La dirección esta vacía."}
            elif len(jd['direccion']) < 5:
                empleados = {'message': "La dirección debe tener más de 5 caracteres."}
            elif len(jd['direccion']) > 50:
                empleados = {'message': "La dirección debe tener menos de 50 caracteres."}
            elif (jd['idTipoDocumentos']) <= 0:
                empleados = {'message': "El tipo de documento esta vacío."}
            elif validar_id_documento(jd['idTipoDocumentos']):
                empleados = {'message': "El id de documento no existe."}
            elif len(jd['documento']) <= 0:
                empleados = {'message': "El documento esta vacío."}
            elif not len(jd['documento']) == (validar_documento(jd['idTipoDocumentos'])):
                empleados = {'message': "El documento debe cumplir la longitud asignada."}
            elif (jd['idCargoEmpleado']) <= 0:
                empleados = {'message': "El cargo esta vacío."}
            elif jd['activo'] < 0:
                empleados = {'message': "Activo debe ser positivo."}
            elif jd['activo'] > 1:
                empleados = {'message': "Activo unicamente puede ser 0 o 1."}
            else:
                empleados = {'message': "Registro Exitoso."}
                empleado.nombre = jd['nombre']
                empleado.apellidos = jd['apellidos']
                empleado.email = jd['email']
                empleado.telefono = str(jd['telefono'])
                empleado.direccion = jd['direccion']
                empleado.fechaNacimiento = str(jd['fechaNacimiento'])
                empleado.idTipoDocumentos = instanciar_documento(jd['idTipoDocumentos'])
                empleado.documento = jd['documento']
                if jd['idEspecialidadMedico'] > 0:
                    empleado.idEspecialidadMedico = instanciar_especialidad(jd['idEspecialidadMedico'])
                empleado.idCargoEmpleado = instanciar_cargo(jd['idCargoEmpleado'])
                empleado.activo = jd['activo']
                print(empleado)
                empleado.save()
                empleados = {'message': "El actualización fue exitosa."}
        return JsonResponse(empleados)
        
        
#Eliminar un registro de cargos
    def delete(self, request,id):
        empleados = list(Empleado.objects.filter(id=id).values())
        if len(empleados) > 0:
            Empleado.objects.filter(id=id).delete()
            datos = {'message':"Registro Eliminado"}
        else:
            datos = {'message':"No se encontraró el registro", 'empleados': []}
        return JsonResponse(datos)
    

#validaciones metodos
def validar_email(correo):
    expresion_regular = r"^[a-zA-Z0-9._%+-]{4,30}@[a-zA-Z0-9]{2,20}\.[a-zA-Z]{2,20}(?:\.[a-zA-Z]{2,20})?$"
    return re.match(expresion_regular, correo) is None

def validar_documento(id):
    if (id>0):
        documento = TipoDocumentos.objects.get(id=id)
        return documento.longitud
    return False

def validar_documento_repetido(documento):
    if (documento):
        documentos = Empleado.objects.filter(documento=documento)
        if len(documentos) > 0:
            return True
        else:
            return False
    return False

def instanciar_especialidad(id):
    if (id>0):
        especialidad = EspecialidadMedico.objects.get(id=id)
        if especialidad:
            return especialidad
        else:
            None

def instanciar_cargo(id):
    if (id>0):
        cargo = CargoEmpleado.objects.get(id=id)
        if cargo:
            return cargo
        
def instanciar_documento(id):
    if (id>0):
        documentos = TipoDocumentos.objects.get(id=id)
        if documentos:
            return documentos

def validar_id_documento(id):
    if (id>0):
        documento = TipoDocumentos.objects.filter(id=id)
        if documento:
            return False
        else:
            return True
        
def validar_cadena_repeticion(cadena):
    patron = r'([a-zA-Z])\1\1'
    return bool(re.search(patron, cadena))

def validar_cadena_espacios(cadena):
    patron = r'^[^ ]+(?: {0,1}[^ ]+)*$'
    return bool(re.match(patron,cadena))





def validar_edad(fechaNacimiento):
    fecha=datetime.date.fromisoformat(fechaNacimiento)
    fecha_actual = datetime.date.today()
    edad= fecha_actual.year - fecha.year
    edad -=((fecha_actual.month, fecha_actual.day)< (fecha.month,fecha.day))
    if edad > 18:
        return False
    else:
        return True
   

def validar_edad_maxima(fechaNacimiento):
    fecha=datetime.date.fromisoformat(fechaNacimiento)
    edad = (date.today() - fecha) // timedelta(days=365.2425)
    if edad > 80:
        return False
    else:
        return True
        