from datetime import date, datetime
from decimal import Decimal
from django.http.response import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
import re
from ..models import *
from django.views.decorators.http import require_http_methods

@method_decorator(require_http_methods(['POST','PUT','GET','DELETE']), name='dispatch')
class ReimprimirPdf(View):
    #Este metodo permite realizar las conultas que necesitan autentificacion. POST PUT DELETE
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    #Busquedas personalizadas y por defecto
    #las personalizadas varian segun el criterio ingresado, y por defecto muestra todos los objetos
    def get(self, request,id):
        recaudo = Recaudo.objects.get(id=id)

        nombreEmpresa = ParametrosGenerales.objects.get(nombre = 'nombre')
        direccionEmpresa = ParametrosGenerales.objects.get(nombre = 'direccion')
        telefonoEmpresa = ParametrosGenerales.objects.get(nombre = 'telefono')
        correoEmpresa = ParametrosGenerales.objects.get(nombre = 'correo')
        rtnEmpresa = ParametrosGenerales.objects.get(nombre = 'rtn')
        empleado = Empleado.objects.get(id=recaudo.idEmpleado.id)
        metodo = MetodoDePago.objects.get(id=recaudo.idMetodoPago.id)
        correlativo = CorrelativoSar.objects.get(id=recaudo.idCorrelativo.id)
        if recaudo.idPaciente:
            cliente = Paciente.objects.get(id=recaudo.idPaciente.id)
        else:
            cliente = None
    
        rInicio = str(correlativo.rangoInicial).zfill(6)
        rFinal = str(correlativo.rangoFinal).zfill(6)
        rangoInicialF = f'{correlativo.rangoFinal} { correlativo.fechaLimiteEmision.day }-{ correlativo.fechaLimiteEmision.month }-{ correlativo.fechaLimiteEmision.year } { rInicio }'
        rangoFinalF = f'{correlativo.rangoFinal} { correlativo.fechaLimiteEmision.day }-{ correlativo.fechaLimiteEmision.month }-{ correlativo.fechaLimiteEmision.year } { rFinal }'

        datos_pdf = {
                    'nombreEmpresa':nombreEmpresa.valor,
                    'direccionEmpresa':direccionEmpresa.valor,
                    'telefonoEmpresa':telefonoEmpresa.valor,
                    'correoEmpresa':correoEmpresa.valor,
                    'rtnEmpresa':rtnEmpresa.valor,
                    'caiEmpresa':correlativo.cai,
                    'numeroFactura':recaudo.noFactura,
                    'fechaFactura':recaudo.fechaFacturacion,
                    'fechaLimite':formato_fecha(correlativo.fechaLimiteEmision),
                    'nombreEmpleado':empleado.nombre + " " + empleado.apellidos,
                    'nombreCliente':'Consumidor Final',
                    'documentoCliente':'N/A',
                    'telefonoCliente':'N/A',
                    'correoCliente':'N/A',
                    'direccionCliente':'N/A',
                    'metodoPago':metodo.nombre,
                    'rangoInicial':rangoInicialF,
                    'rangoFinal':rangoFinalF,
                    'subtotalFactura':format(float(recaudo.subtotal),',.2f'),
                    'totalFactura':format(float(recaudo.total),',.2f'),
                    'impuestosFactura':format(float(recaudo.impuesto),',.2f'),
                    'montoTarjeta':'0.00',
                    'montoEfectivo':'0.00',
                    'cambio':'0.00',
                    'descuento':recaudo.descuento,
                    'numMasc':'N/A'
                }
        
        if cliente:
            datos_pdf['nombreCliente']= cliente.nombre + " " + cliente.apellido
            datos_pdf['documentoCliente']= cliente.documento
            datos_pdf['telefonoCliente']= cliente.telefono
            datos_pdf['correoCliente']= cliente.correo
            datos_pdf['direccionCliente']= cliente.direccion

        if recaudo.idMetodoPago.id == 1:
            datos_pdf['montoTarjeta']= format(float(recaudo.total),',.2f')
            datos_pdf['numMasc'] = mascara_tarjeta(recaudo.tarjeta)
        elif recaudo.idMetodoPago.id == 2:
            datos_pdf['montoEfectivo']= format(float(recaudo.efectivo),',.2f')
        elif recaudo.idMetodoPago.id == 3:
            datos_pdf['montoEfectivo']= format(float(recaudo.efectivo),',.2f')
            datos_pdf['montoTarjeta']= format(float(recaudo.total - recaudo.efectivo),',.2f')
            datos_pdf['numMasc'] = mascara_tarjeta(recaudo.tarjeta)
        else:
            datos_pdf['montoEfectivo']= '0.00'
            datos_pdf['montoTarjeta']= '0.00'
            datos_pdf['numMasc'] = 'N/A'

        if recaudo.cambio:
            datos_pdf['cambio'] = format(float(recaudo.cambio),',.2f')

        if recaudo.idConsulta:
            consulta_value = []
            consulta_dict = {
                'idTipo':{
                    'nombre':recaudo.idConsulta.idTipo.nombre,
                    'precio':recaudo.idConsulta.idTipo.precio,
                    'impuesto':recaudo.idConsulta.idTipo.idImpuesto.valor
                }
            }
            consulta_value.append(consulta_dict)
            datos_pdf['consulta'] = consulta_value

        medicamentos = RecaudoDetalleMedicamento.objects.filter(idRecaudo=id)
        medicamentos_values = []
        if medicamentos:
            for item in medicamentos:
                medicamento_dict = {
                    'nombre':item.idMedicamento.nombre,
                    'precio':item.idMedicamento.precioVenta,
                    'impuesto':item.idMedicamento.idImpuesto.valor,
                    'cantidad':item.cantidad
                }
                medicamentos_values.append(medicamento_dict)
        datos_pdf['medicamentos'] = medicamentos_values

        tratamientos = RecaudoDetalleTratamiento.objects.filter(idRecaudo=id)
        tratamiento_values = []
        if tratamientos:
            for item in tratamientos:
                tratamiento_dict = {
                    'nombre':item.idTratamiento.idTipo.nombre,
                    'precio':item.idTratamiento.idTipo.precio,
                    'impuesto':item.idTratamiento.idTipo.idImpuesto.valor
                }
                tratamiento_values.append(tratamiento_dict)
        datos_pdf['tratamientos'] = tratamiento_values

        examenes = RecaudoDetalleExamen.objects.filter(idRecaudo=id)
        examenes_values = []
        if examenes:
            for item in examenes:
                examen_dict = {
                    'nombre':item.idExamen.idTipo.nombre,
                    'precio':item.idExamen.idTipo.precio,
                    'impuesto':item.idExamen.idTipo.idImpuesto.valor
                }
                examenes_values.append(examen_dict)
        datos_pdf['examenes'] = examenes_values
        context = {
            'mensaje':'Datos para el PDF',
            'datos_pdf':datos_pdf
        }
        return JsonResponse(context)
    
    
def formato_fecha(fecha):
    if fecha is not None:
        fecha_formateada = fecha.strftime("%d-%m-%Y")
        fecha_formateada = fecha_formateada.replace('-', '/')
        return fecha_formateada
    else:
        return None
    
def mascara_tarjeta(str):
    if str is None or len(str) <= 4:
        return str
    else:
        ultimos_4_caracteres = str[-4:]
        asteriscos = "*" * (len(str) - 4)
        return "{}{}".format(asteriscos, ultimos_4_caracteres)