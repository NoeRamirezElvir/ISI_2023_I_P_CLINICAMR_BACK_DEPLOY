from datetime import datetime, timedelta
from decimal import Decimal
import decimal 
from django.http.response import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
import re
from ..models import *
from django.views.decorators.http import require_http_methods

@method_decorator(require_http_methods(['POST','PUT','GET','DELETE']), name='dispatch')
class MedicamentosViews(View):
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
                    medicamentos = Medicamento.objects.filter(id=campo).select_related('idImpuesto','idTipo','idProveedor')
                    if medicamentos is not None:
                        medicamentos_values = []
                        for medicamento in medicamentos:
                            medicamento_dict = {
                                'id': medicamento.id,
                                'nombre': medicamento.nombre,
                                'fechaRegistro': formato_fecha(medicamento.fechaRegistro),
                                'activo': medicamento.activo,
                                'stockActual': medicamento.stockActual,
                                'stockMinimo': medicamento.stockMinimo,
                                'stockMaximo': medicamento.stockMaximo,
                                'costoCompra': medicamento.costoCompra,
                                'precioVenta': medicamento.precioVenta,
                                'idTipo': {
                                    'id': medicamento.idTipo.id,
                                    'nombre': medicamento.idTipo.nombre
                                },
                                'idProveedor': {
                                    'id': medicamento.idProveedor.id,
                                    'nombre': medicamento.idProveedor.nombre
                                },
                                'idImpuesto': {
                                    'id': medicamento.idImpuesto.id,
                                    'nombre': medicamento.idImpuesto.valor
                                }
                            }
                            medicamentos_values.append(medicamento_dict)
                        context = {
                            'message': "Consulta exitosa",
                            'medicamentos': medicamentos_values
                        }
                        return JsonResponse(context)
                    else:
                        context = {
                            'message': "No se encontraron los datos",
                            'medicamentos': []
                        }
                        return JsonResponse(context)
                elif criterio == "nombre":
                    medicamentos = Medicamento.objects.filter(nombre=campo).select_related('idImpuesto','idTipo','idProveedor')
                    if medicamentos is not None:
                        medicamentos_values = []
                        for medicamento in medicamentos:
                            medicamento_dict = {
                                'id': medicamento.id,
                                'nombre': medicamento.nombre,
                                'fechaRegistro': formato_fecha(medicamento.fechaRegistro),
                                'activo': medicamento.activo,
                                'stockActual': medicamento.stockActual,
                                'stockMinimo': medicamento.stockMinimo,
                                'stockMaximo': medicamento.stockMaximo,
                                'costoCompra': medicamento.costoCompra,
                                'precioVenta': medicamento.precioVenta,
                                'idTipo': {
                                    'id': medicamento.idTipo.id,
                                    'nombre': medicamento.idTipo.nombre
                                },
                                'idProveedor': {
                                    'id': medicamento.idProveedor.id,
                                    'nombre': medicamento.idProveedor.nombre
                                },
                                'idImpuesto': {
                                    'id': medicamento.idImpuesto.id,
                                    'nombre': medicamento.idImpuesto.valor
                                }
                            }
                            medicamentos_values.append(medicamento_dict)
                        context = {
                            'message': "Consulta exitosa",
                            'medicamentos': medicamentos_values
                        }
                        return JsonResponse(context)
                    else:
                        context = {
                            'message': "No se encontraron los datos",
                            'medicamentos': []
                        }
                        return JsonResponse(context)
            else:
                medicamentos = Medicamento.objects.select_related('idImpuesto','idTipo','idProveedor')
                if medicamentos is not None:
                    medicamentos_values = []
                    for medicamento in medicamentos:
                        medicamento_dict = {
                            'id': medicamento.id,
                            'nombre': medicamento.nombre,
                            'fechaRegistro': formato_fecha(medicamento.fechaRegistro),
                            'activo': medicamento.activo,
                            'stockActual': medicamento.stockActual,
                            'stockMinimo': medicamento.stockMinimo,
                            'stockMaximo': medicamento.stockMaximo,
                            'costoCompra': medicamento.costoCompra,
                            'precioVenta': medicamento.precioVenta,
                            'idTipo': {
                                'id': medicamento.idTipo.id,
                                'nombre': medicamento.idTipo.nombre
                            },
                            'idProveedor': {
                                'id': medicamento.idProveedor.id,
                                'nombre': medicamento.idProveedor.nombre
                            },
                            'idImpuesto': {
                                'id': medicamento.idImpuesto.id,
                                'nombre': medicamento.idImpuesto.valor
                            }
                        }
                        medicamentos_values.append(medicamento_dict)
                    context = {
                        'message': "Consulta exitosa",
                        'medicamentos': medicamentos_values
                    }
                    return JsonResponse(context)
                else:
                    context = {
                        'message': "No se encontraron los datos",
                        'medicamentos': []
                    }
                    return JsonResponse(context)
            return JsonResponse(medicamentos)
        except Exception as e:
            mensaje_delete = {'message': f"Error: {e}"}
            return JsonResponse(mensaje_delete)

#Agregar un registro de cargos
#nombre, idTipo,fechaRegistro,stockActual,stockMinimo,stockMaximo,idProveedor,idImpuesto,costoCompra,precioVenta
    def post(self, request):
        #try:
            jd=json.loads(request.body)

            if len(jd['nombre']) <= 0:
                mensaje_post = {'message': "El nombre esta vacío."}
            elif len(jd['nombre']) < 4:
                mensaje_post = {'message': "El nombre debe tener mas de 4 caracteres."}
            elif not validar_cadena_espacios(jd['nombre']):
                mensaje_post = {'message': "No se permiten mas de un espacio consecutivo.[nombre]"}
            elif validar_cadena_repeticion(jd['nombre']):
                mensaje_post = {'message': "No se permiten mas de dos caracteres consecutivos del mismo tipo.[nombre]"}
            elif len(jd['nombre']) > 50:
                mensaje_post = {'message': "El nombre debe tener menos de 50 caracteres."}
            elif validar_medicamento_repetido(jd['nombre']):
                mensaje_post = {'message': "El nombre de medicamento ya esta en uso."}
            elif jd['idTipo'] is None:
                mensaje_post = {'message': "Seleccione un tipo existente."}
            elif int(jd['idTipo']) == 0:
                mensaje_post = {'message': "Seleccione un tipo existente."}
            elif validar_id_tipo(int(jd['idTipo'])):
                mensaje_post = {'message': "El tipo no existe."}
            elif int(jd['activo']) < 0:
                mensaje_post = {'message': "Activo debe ser positivo."}
            elif int(jd['activo']) > 1:
                mensaje_post = {'message': "Activo unicamente puede ser 0 o 1."}
            elif (jd['stockActual']) is None:
                mensaje_post = {'message': "El stock actual esta vacío."}
            elif str(jd['stockActual']) == "":
                mensaje_post = {'message': "El stock actual esta vacío."}
            elif int(jd['stockActual']) < 0:
                mensaje_post = {'message': "El stock actual debe ser positivo."}
            elif len(str(int(jd['stockActual']))) > 10:
                mensaje_post = {'message': "El stock actual debe tener menos de 10 digitos."}
            elif int(jd['stockActual']) > 9999999999:
                mensaje_post = {'message': "El stock actual debe tener menos de 10 digitos."}
            elif int((jd['stockActual'])) < int((jd['stockMinimo'])):
                mensaje_post = {'message': "El stock actual debe ser mayor o igual al  stock minimo."}
            elif int((jd['stockActual'])) > int((jd['stockMaximo'])):
                mensaje_post = {'message': "El stock actual debe ser menor o igual al stock maximo."}
            elif (jd['stockMinimo']) is None:
                mensaje_post = {'message': "El stock minimo esta vacío."}
            elif str(jd['stockMinimo']) == "":
                mensaje_post = {'message': "El stock minimo esta vacío."}
            elif int(jd['stockMinimo']) < 0:
                mensaje_post = {'message': "El stock minimo debe ser positivo."}
            elif len(str(int(jd['stockMinimo']))) > 10:
                mensaje_post = {'message': "El stock minimo debe tener menos de 10 digitos."}
            elif int(jd['stockMinimo']) > 9999999999:
                mensaje_post = {'message': "El stock minimo debe tener menos de 10 digitos."}
            elif int((jd['stockMinimo'])) > int((jd['stockActual'])):
                mensaje_post = {'message': "El stock minimo debe ser menor o igual al  stock actual."}
            elif int((jd['stockMinimo'])) >= int((jd['stockMaximo'])):
                mensaje_post = {'message': "El stock minimo debe ser menor al stock maximo."}
            elif (jd['stockMaximo']) is None:
                mensaje_post = {'message': "El stock maximo esta vacío."}
            elif str(jd['stockMaximo']) == "":
                mensaje_post = {'message': "El stock maximo esta vacío."}
            elif int(jd['stockMaximo']) < 0:
                mensaje_post = {'message': "El stock maximo debe ser positivo."}
            elif len(str(int(jd['stockMaximo']))) > 10:
                mensaje_post = {'message': "El stock maximo debe tener menos de 10 digitos."}
            elif int(jd['stockMaximo']) > 9999999999:
                mensaje_post = {'message': "El stock maximo debe tener menos de 10 digitos."}
            elif int((jd['stockMaximo'])) < int((jd['stockActual'])):
                mensaje_post = {'message': "El stock maximo debe ser mayor o igual al  stock actual."}
            elif int((jd['stockMaximo'])) <= int((jd['stockMinimo'])):
                mensaje_post = {'message': "El stock maximo debe ser mayor al stock minimo."}
            elif jd['idProveedor'] is None:
                mensaje_post = {'message': "Seleccione un proveedor existente."}
            elif int(jd['idProveedor']) == 0:
                mensaje_post = {'message': "Seleccione un proveedor existente."}
            elif validar_id_proveedor(int(jd['idProveedor'])):
                mensaje_post = {'message': "El proveedor no existe."}
            elif jd['idImpuesto'] is None:
                mensaje_post = {'message': "Seleccione un impuesto existente."}
            elif int(jd['idImpuesto']) == 0:
                mensaje_post = {'message': "Seleccione un impuesto existente."}
            elif validar_id_impuesto(int(jd['idImpuesto'])):
                mensaje_post = {'message': "El impuesto no existe."}
            elif Decimal(jd['costoCompra']) <= 0:
                mensaje_post = {'message': "El costo debe ser mayor a 0."}
            elif len(str(jd['costoCompra'])) > 11:
                mensaje_post = {'message': "El costo debe tener menos de 10 digitos."}
            elif round(Decimal(jd['costoCompra'])) > 99999999.99:
                mensaje_post = {'message': "El costo es muy alto."}
            elif round(Decimal(jd['costoCompra']), 2) > round(Decimal(jd['precioVenta']), 2):
                mensaje_post = {'message': "El costo debe ser menor al precio de venta."}
            elif Decimal(jd['precioVenta']) <= 0:
                mensaje_post = {'message': "El precio debe ser mayor a 0."}
            elif len(str(jd['precioVenta'])) > 11:
                mensaje_post = {'message': "El precio debe tener menos de 10 digitos."}
            elif round(Decimal(jd['precioVenta'])) > 99999999.99:
                mensaje_post = {'message': "El precio es muy alto."}
            elif round(Decimal(jd['precioVenta']), 2) < round(Decimal(jd['costoCompra']), 2):
                mensaje_post = {'message': "El precio debe ser mayor al costo de compra."}
            else:
                #Se crea el objeto Medicamento
                costoCompra = Decimal(jd['costoCompra'])
                precioVenta = Decimal(jd['precioVenta'])

                Medicamento.objects.create(nombre=jd['nombre'], 
                                        idTipo=instanciar_tipo(int(jd['idTipo'])), 
                                        fechaRegistro=datetime.now(),
                                        activo=int((jd['activo'])),
                                        stockActual=int((jd['stockActual'])),
                                        stockMinimo=int((jd['stockMinimo'])),
                                        stockMaximo=int((jd['stockMaximo'])),
                                        idProveedor=instanciar_proveedor(int(jd['idProveedor'])),
                                        idImpuesto=instanciar_impuesto(int(jd['idImpuesto'])),
                                        costoCompra= costoCompra,
                                        precioVenta= precioVenta,)
                # Se crea un historico para el costo y precio, la fecha inicial es la fecha actual de registro
                # la fecha final no se agrega, este historico se guarda con el id del medicamento recien registrado,
                # que se toma despues de buscarlo segun su nombre
                CostoHistoricoMedicamento.objects.create(idmedicamento=instanciar_medicamento(jd['nombre']),
                                                        fechaInicio=datetime.now(),
                                                        activo=1,
                                                        costo=jd['costoCompra'])
                PrecioHistoricoMedicamento.objects.create(idmedicamento=instanciar_medicamento(jd['nombre']),
                                                        fechaInicio=datetime.now(),
                                                        activo=1,
                                                        precio=jd['precioVenta'])
                mensaje_post = {'message':"Registro Exitoso."}
            return JsonResponse(mensaje_post)

#Actualizar un registro de cargos
#nombre, idTipo,fechaRegistro,activo,stockActual,stockMinimo,stockMaximo,idProveedor,idImpuesto,costoCompra,precioVenta
    def put(self, request,id):
        #try:
            jd=json.loads(request.body)
            mensaje_put = list(Medicamento.objects.filter(id=id).values())
            if len(mensaje_put) > 0:
                medicamento_actualizar=Medicamento.objects.get(id=id)

                if len(jd['nombre']) <= 0:
                    mensaje_put = {'message': "El nombre esta vacío."}
                elif len(jd['nombre']) < 4:
                    mensaje_put = {'message': "El nombre debe tener mas de 4 caracteres."}
                elif not validar_cadena_espacios(jd['nombre']):
                    mensaje_put = {'message': "No se permiten mas de un espacio consecutivo.[nombre]"}
                elif validar_cadena_repeticion(jd['nombre']):
                    mensaje_put = {'message': "No se permiten mas de dos caracteres consecutivos del mismo tipo.[nombre]"}
                elif len(jd['nombre']) > 50:
                    mensaje_put = {'message': "El nombre debe tener menos de 50 caracteres."}
                elif jd['idTipo'] is None:
                    mensaje_put = {'message': "Seleccione un tipo existente."}
                elif int(jd['idTipo']) == 0:
                    mensaje_put = {'message': "Seleccione un tipo existente."}
                elif validar_id_tipo(int(jd['idTipo'])):
                    mensaje_put = {'message': "El tipo no existe."}
                elif int(jd['activo']) < 0:
                    mensaje_put = {'message': "Activo debe ser positivo."}
                elif int(jd['activo']) > 1:
                    mensaje_put = {'message': "Activo unicamente puede ser 0 o 1."}
                elif (jd['stockActual']) is None:
                    mensaje_put = {'message': "El stock actual esta vacío."}
                elif str(jd['stockActual']) == "":
                    mensaje_put = {'message': "El stock actual esta vacío."}
                elif int(jd['stockActual']) < 0:
                    mensaje_put = {'message': "El stock actual debe ser positivo."}
                elif len(str(int(jd['stockActual']))) > 10:
                    mensaje_put = {'message': "El stock actual debe tener menos de 10 digitos."}
                elif int(jd['stockActual']) > 9999999999:
                    mensaje_put = {'message': "El stock actual debe tener menos de 10 digitos."}
                elif int((jd['stockActual'])) < int((jd['stockMinimo'])):
                    mensaje_put = {'message': "El stock actual debe ser mayor o igual al  stock minimo."}
                elif int((jd['stockActual'])) > int((jd['stockMaximo'])):
                    mensaje_put = {'message': "El stock actual debe ser menor o igual al stock maximo."}
                elif (jd['stockMinimo']) is None:
                    mensaje_put = {'message': "El stock minimo esta vacío."}
                elif str(jd['stockMinimo']) == "":
                    mensaje_put = {'message': "El stock minimo esta vacío."}
                elif int(jd['stockMinimo']) < 0:
                    mensaje_put = {'message': "El stock minimo debe ser positivo."}
                elif len(str(int(jd['stockMinimo']))) > 10:
                    mensaje_put = {'message': "El stock minimo debe tener menos de 10 digitos."}
                elif int(jd['stockMinimo']) > 9999999999:
                    mensaje_put = {'message': "El stock minimo debe tener menos de 10 digitos."}
                elif int((jd['stockMinimo'])) > int((jd['stockActual'])):
                    mensaje_put = {'message': "El stock minimo debe ser menor o igual al  stock actual."}
                elif int((jd['stockMinimo'])) >= int((jd['stockMaximo'])):
                    mensaje_put = {'message': "El stock minimo debe ser menor al stock maximo."}
                elif (jd['stockMaximo']) is None:
                    mensaje_put = {'message': "El stock maximo esta vacío."}
                elif str(jd['stockMaximo']) == "":
                    mensaje_put = {'message': "El stock maximo esta vacío."}
                elif int(jd['stockMaximo']) < 0:
                    mensaje_put = {'message': "El stock maximo debe ser positivo."}
                elif len(str(int(jd['stockMaximo']))) > 10:
                    mensaje_put = {'message': "El stock maximo debe tener menos de 10 digitos."}
                elif int(jd['stockMaximo']) > 9999999999:
                    mensaje_put = {'message': "El stock maximo debe tener menos de 10 digitos."}
                elif int((jd['stockMaximo'])) < int((jd['stockActual'])):
                    mensaje_put = {'message': "El stock maximo debe ser mayor o igual al  stock actual."}
                elif int((jd['stockMaximo'])) <= int((jd['stockMinimo'])):
                    mensaje_put = {'message': "El stock maximo debe ser mayor al stock minimo."}
                elif jd['idProveedor'] is None:
                    mensaje_put = {'message': "Seleccione un proveedor existente."}
                elif int(jd['idProveedor']) == 0:
                    mensaje_put = {'message': "Seleccione un proveedor existente."}
                elif validar_id_proveedor(int(jd['idProveedor'])):
                    mensaje_put = {'message': "El proveedor no existe."}
                elif jd['idImpuesto'] is None:
                    mensaje_put = {'message': "Seleccione un impuesto existente."}
                elif int(jd['idImpuesto']) == 0:
                    mensaje_put = {'message': "Seleccione un impuesto existente."}
                elif validar_id_impuesto(int(jd['idImpuesto'])):
                    mensaje_put = {'message': "El impuesto no existe."}
                elif Decimal(jd['costoCompra']) <= 0:
                    mensaje_put = {'message': "El costo debe ser mayor a 0."}
                elif len(str(jd['costoCompra'])) > 11:
                    mensaje_put = {'message': "El costo debe tener menos de 10 digitos."}
                elif round(Decimal(jd['costoCompra'])) > 99999999.99:
                    mensaje_put = {'message': "El costo es muy alto."}
                elif round(Decimal(jd['costoCompra']), 2) > round(Decimal(jd['precioVenta']), 2):
                    mensaje_put = {'message': "El costo debe ser menor al precio de venta."}
                elif Decimal(jd['precioVenta']) <= 0:
                    mensaje_put = {'message': "El precio debe ser mayor a 0."}
                elif len(str(jd['precioVenta'])) > 11:
                    mensaje_put = {'message': "El precio debe tener menos de 10 digitos."}
                elif round(Decimal(jd['precioVenta'])) > 99999999.99:
                    mensaje_put = {'message': "El precio es muy alto."}
                elif round(Decimal(jd['precioVenta']), 2) < round(Decimal(jd['costoCompra']), 2):
                    mensaje_put = {'message': "El precio debe ser mayor al costo de compra."}

                else:
                    nombre_temp=medicamento_actualizar.nombre

                    medicamento_actualizar.nombre = jd['nombre']
                    medicamento_actualizar.idTipo = instanciar_tipo(int(jd['idTipo']))
                    medicamento_actualizar.fechaRegistro = datetime.now()
                    medicamento_actualizar.activo = int(jd['activo'])
                    medicamento_actualizar.stockActual = int(jd['stockActual'])
                    medicamento_actualizar.stockMinimo = int(jd['stockMinimo'])
                    medicamento_actualizar.stockMaximo = int(jd['stockMaximo'])
                    medicamento_actualizar.idProveedor = instanciar_proveedor(int(jd['idProveedor']))
                    medicamento_actualizar.idImpuesto = instanciar_impuesto(int(jd['idImpuesto']))
                    medicamento_actualizar.costoCompra = Decimal(jd['costoCompra'])
                    medicamento_actualizar.precioVenta = Decimal(jd['precioVenta'])
                    #if float(medicamento_actualizar.id) == float(id):
                        #Se busca el ultimo costo historico que tenga relacion con el medicamento(nombre de este),
                        #Para actualizar su fecha final
                    costo_historico = CostoHistoricoMedicamento.objects.filter(idmedicamento=id).last()
                    if costo_historico is not None:
                        if not round(Decimal(costo_historico.costo), 2) == round(Decimal(medicamento_actualizar.costoCompra), 2):
                            costo_historico.fechaFinal = fecha_final()
                            costo_historico.save()
                            CostoHistoricoMedicamento.objects.create(idmedicamento=instanciar_medicamento(nombre_temp), fechaInicio=datetime.now(),costo=jd['costoCompra'], activo=1)
                    else:
                        CostoHistoricoMedicamento.objects.create(idmedicamento=instanciar_medicamento(nombre_temp), fechaInicio=datetime.now(),costo=jd['costoCompra'], activo=1)
                    #Se busca el ultimo precio historico que tenga relacion con el medicamento(nombre de este),
                    #Para actualizar su fecha final
                    precio_historico = PrecioHistoricoMedicamento.objects.filter(idmedicamento=id).last()
                    if precio_historico is not None:
                        if not round(Decimal(precio_historico.precio), 2) == round(Decimal(medicamento_actualizar.precioVenta), 2):
                            precio_historico.fechaFinal = fecha_final()
                            precio_historico.save()
                            PrecioHistoricoMedicamento.objects.create(idmedicamento=instanciar_medicamento(nombre_temp), fechaInicio=datetime.now(),precio=jd['precioVenta'], activo=1)
                    else:
                        PrecioHistoricoMedicamento.objects.create(idmedicamento=instanciar_medicamento(nombre_temp), fechaInicio=datetime.now(),precio=jd['precioVenta'], activo=1)
                    medicamento_actualizar.save()
                    mensaje_put = {'message': "La actualización fue exitosa."}
            return JsonResponse(mensaje_put)
        #except Exception as e:
            #mensaje_delete = {'message': f"Error: {e}"}
            #return JsonResponse(mensaje_delete)
        
        
#Eliminar un registro de cargos
    def delete(self, request,id):
        medicamentos = list(Medicamento.objects.filter(id=id).values())
        if len(medicamentos) > 0:
            Medicamento.objects.filter(id=id).delete()
            datos = {'message':"Registro Eliminado"}
            return JsonResponse(datos) 
        else:
            datos = {'message':"No se encontró el registro", 'medicamentos': []}
            return JsonResponse(datos)



def instanciar_tipo(id):
    if (id>0):
        registro = Tipo.objects.get(id=id)
        if registro:
            return registro

def instanciar_proveedor(id):
    if (id>0):
        registro = Proveedor.objects.get(id=id)
        if registro:
            return registro
        
def instanciar_impuesto(id):
    if (id>0):
        registro = Impuesto.objects.get(id=id)
        if registro:
            return registro
        
def instanciar_medicamento(nombre):
    if len(nombre)>0:
        registro = Medicamento.objects.filter(nombre=nombre).last()
        if registro:
            return registro
         
def validar_medicamento_repetido(nombre): 
    if (nombre):
        registros = Medicamento.objects.filter(nombre=nombre)
        if len(registros) > 0:
            return True
        else:
            return False
    return False



def fecha_final():
    fecha_menos_un_dia=datetime.today()+timedelta(days=-1)
    return fecha_menos_un_dia

def validar_cadena_repeticion(cadena):
    patron = r'([a-zA-Z])\1\1'
    return bool(re.search(patron, cadena))

def validar_cadena_espacios(cadena):
    patron = r'^[^ ]+(?: {0,1}[^ ]+)*$'
    return bool(re.match(patron,cadena))

def validar_id_tipo(id):
    if (id>0):
        subtipo = Tipo.objects.filter(id=id)
        if subtipo:
            return False
        else:
            return True
        
def validar_id_proveedor(id):
    if (id>0):
        subtipo = Proveedor.objects.filter(id=id)
        if subtipo:
            return False
        else:
            return True
        
def validar_id_impuesto(id):
    if (id>0):
        subtipo = Impuesto.objects.filter(id=id)
        if subtipo:
            return False
        else:
            return True

def formato_fecha(fecha):
    if fecha is not None:
        fecha_formateada = fecha.strftime("%d-%m-%Y")
        return fecha_formateada
    else:
        return None    


