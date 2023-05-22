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
class RecaudoView(View):
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
                    recaudos = Recaudo.objects.filter(id=campo).select_related('idCorrelativo','idEmpleado','idMetodoPago','idPaciente','idConsulta','idDescuento')
                    if recaudos is not None:
                        recaudos_values = []
                        for recaudo in recaudos:
                            recaudo_dict = {
                                'id': recaudo.id,
                                'noFactura': recaudo.noFactura,
                                'fechaFacturacion': recaudo.fechaFacturacion,
                                'efectivo': recaudo.efectivo,
                                'tarjeta': mascara_tarjeta(recaudo.tarjeta),
                                'fechaEntrega': formato_fecha(recaudo.fechaEntrega),
                                'estado': recaudo.estado,
                                'activa': recaudo.activa,
                                'total': recaudo.total,
                                'subtotal':recaudo.subtotal,
                                'cambio': recaudo.cambio,
                                'descuento': recaudo.descuento,
                                'impuesto': recaudo.impuesto,
                                'idDescuento': {},
                                'idCorrelativo':{
                                    'id': recaudo.idCorrelativo.id,
                                    'cai': recaudo.idCorrelativo.cai,
                                    'rangoInicial': recaudo.idCorrelativo.rangoInicial,
                                    'rangoFinal': recaudo.idCorrelativo.rangoFinal,
                                    'consecutivo': recaudo.idCorrelativo.consecutivo,
                                    'fechaLimiteEmision': recaudo.idCorrelativo.fechaLimiteEmision,
                                    'fechaInicio': recaudo.idCorrelativo.fechaInicio
                                },
                                'idConsulta':{
                                },
                                'idPaciente':{},
                                'idEmpleado':{
                                    'id':recaudo.idEmpleado.id,
                                    'nombre':recaudo.idEmpleado.nombre,
                                    'documento':recaudo.idEmpleado.documento
                                },
                                'idMetodoPago':{
                                    'id':recaudo.idMetodoPago.id,
                                    'nombre':recaudo.idMetodoPago.nombre
                                },
                                'medicamentos':{},
                                'tratamientos':{},
                                'examenes':{}
                            }
                            if(recaudo.idDescuento):
                                descuento_dict = {
                                    'id':recaudo.idDescuento.id,
                                    'valor':recaudo.idDescuento.valor,

                                }
                                recaudo_dict['idDescuento'] = descuento_dict
                            if(recaudo.idConsulta):
                                consulta_dict = {
                                    'id':recaudo.idConsulta.id,
                                    'precio':recaudo.idConsulta.idTipo.precio,
                                    'impuesto':recaudo.idConsulta.idTipo.idImpuesto.valor,
                                    'tipo':recaudo.idConsulta.idTipo.nombre,
                                    'paciente':recaudo.idConsulta.idCita.idPaciente.documento,
                                }
                                recaudo_dict['idConsulta'] = consulta_dict
                            if (recaudo.idPaciente):
                                recaudo_dict = buscar_paciente(recaudo_dict,recaudo.idPaciente.id)
                            else:
                                recaudo_dict = buscar_paciente(recaudo_dict,0)
                            medicamentos = RecaudoDetalleMedicamento.objects.filter(idRecaudo = recaudo.id).select_related('idMedicamento')
                            medicamento_dict = {}
                            for medicamento in medicamentos:
                                medicamento_dict = {
                                    'id': medicamento.idMedicamento.id,
                                    'nombre': medicamento.idMedicamento.nombre
                                }
                                recaudo_dict['medicamentos'][medicamento.idMedicamento.id] = medicamento_dict
                            tratamientos = RecaudoDetalleTratamiento.objects.filter(idRecaudo = recaudo.id).select_related('idTratamiento')
                            tratamientos_dict = {}
                            for tratamiento in tratamientos:
                                tratamientos_dict = {
                                    'id': tratamiento.idTratamiento.id,
                                    'nombre': tratamiento.idTratamiento.idTipo.nombre
                                }
                                recaudo_dict['tratamientos'][tratamiento.idTratamiento.id] = tratamientos_dict
                            examenes = RecaudoDetalleExamen.objects.filter(idRecaudo = recaudo.id).select_related('idExamen')
                            examenes_dict = {}
                            for examen in examenes:
                                examenes_dict = {
                                    'id': examen.idExamen.id,
                                    'nombre': examen.idExamen.idTipo.nombre
                                }
                                recaudo_dict['examenes'][examen.idExamen.id] = examenes_dict
                            recaudos_values.append(recaudo_dict)
                        context = {
                            'message': "Consulta exitosa",
                            'recaudo': recaudos_values
                        }
                        return JsonResponse(context)
                    else:
                        context = {
                            'message': "No se encontraron los datos",
                            'enfermedades': examenes_dict
                        }
                        return JsonResponse(context)
                elif criterio == "numeroFactura":
                    recaudos = Recaudo.objects.filter(noFactura=campo).select_related('idCorrelativo','idEmpleado','idMetodoPago','idPaciente','idConsulta','idDescuento')
                    if recaudos is not None:
                        recaudos_values = []
                        for recaudo in recaudos:
                            recaudo_dict = {
                                'id': recaudo.id,
                                'noFactura': recaudo.noFactura,
                                'fechaFacturacion': recaudo.fechaFacturacion,
                                'efectivo': recaudo.efectivo,
                                'tarjeta': mascara_tarjeta(recaudo.tarjeta),
                                'fechaEntrega':formato_fecha(recaudo.fechaEntrega),
                                'estado': recaudo.estado,
                                'activa': recaudo.activa,
                                'total': recaudo.total,
                                'subtotal':recaudo.subtotal,
                                'cambio': recaudo.cambio,
                                'descuento': recaudo.descuento,
                                'impuesto': recaudo.impuesto,
                                'idDescuento': {},
                                'idCorrelativo':{
                                    'id': recaudo.idCorrelativo.id,
                                    'cai': recaudo.idCorrelativo.cai,
                                    'rangoInicial': recaudo.idCorrelativo.rangoInicial,
                                    'rangoFinal': recaudo.idCorrelativo.rangoFinal,
                                    'consecutivo': recaudo.idCorrelativo.consecutivo,
                                    'fechaLimiteEmision': recaudo.idCorrelativo.fechaLimiteEmision,
                                    'fechaInicio': recaudo.idCorrelativo.fechaInicio
                                },
                                'idConsulta':{
                                },
                                'idPaciente':{},
                                'idEmpleado':{
                                    'id':recaudo.idEmpleado.id,
                                    'nombre':recaudo.idEmpleado.nombre,
                                    'documento':recaudo.idEmpleado.documento
                                },
                                'idMetodoPago':{
                                    'id':recaudo.idMetodoPago.id,
                                    'nombre':recaudo.idMetodoPago.nombre
                                },
                                'medicamentos':{},
                                'tratamientos':{},
                                'examenes':{}
                            }
                            if(recaudo.idDescuento):
                                descuento_dict = {
                                    'id':recaudo.idDescuento.id,
                                    'valor':recaudo.idDescuento.valor,

                                }
                                recaudo_dict['idDescuento'] = descuento_dict
                            if(recaudo.idConsulta):
                                consulta_dict = {
                                    'id':recaudo.idConsulta.id,
                                    'precio':recaudo.idConsulta.idTipo.precio,
                                    'impuesto':recaudo.idConsulta.idTipo.idImpuesto.valor,
                                    'tipo':recaudo.idConsulta.idTipo.nombre,
                                    'paciente':recaudo.idConsulta.idCita.idPaciente.documento,
                                }
                                recaudo_dict['idConsulta'] = consulta_dict
                            if (recaudo.idPaciente):
                                recaudo_dict = buscar_paciente(recaudo_dict,recaudo.idPaciente.id)
                            else:
                                recaudo_dict = buscar_paciente(recaudo_dict,0)
                            medicamentos = RecaudoDetalleMedicamento.objects.filter(idRecaudo = recaudo.id).select_related('idMedicamento')
                            medicamento_dict = {}
                            for medicamento in medicamentos:
                                medicamento_dict = {
                                    'id': medicamento.idMedicamento.id,
                                    'nombre': medicamento.idMedicamento.nombre
                                }
                                recaudo_dict['medicamentos'][medicamento.idMedicamento.id] = medicamento_dict
                            tratamientos = RecaudoDetalleTratamiento.objects.filter(idRecaudo = recaudo.id).select_related('idTratamiento')
                            tratamientos_dict = {}
                            for tratamiento in tratamientos:
                                tratamientos_dict = {
                                    'id': tratamiento.idTratamiento.id,
                                    'nombre': tratamiento.idTratamiento.idTipo.nombre
                                }
                                recaudo_dict['tratamientos'][tratamiento.idTratamiento.id] = tratamientos_dict
                            examenes = RecaudoDetalleExamen.objects.filter(idRecaudo = recaudo.id).select_related('idExamen')
                            examenes_dict = {}
                            for examen in examenes:
                                examenes_dict = {
                                    'id': examen.idExamen.id,
                                    'nombre': examen.idExamen.idTipo.nombre
                                }
                                recaudo_dict['examenes'][examen.idExamen.id] = examenes_dict
                            recaudos_values.append(recaudo_dict)
                        context = {
                            'message': "Consulta exitosa",
                            'recaudo': recaudos_values
                        }
                        return JsonResponse(context)
                    else:
                        context = {
                            'message': "No se encontraron los datos",
                            'enfermedades': examenes_dict
                        }
                        return JsonResponse(context)
            else:
                recaudos = Recaudo.objects.select_related('idCorrelativo','idEmpleado','idMetodoPago','idPaciente','idConsulta','idDescuento').order_by('-id')
                if recaudos is not None:
                    recaudos_values = []
                    for recaudo in recaudos:
                        recaudo_dict = {
                            'id': recaudo.id,
                            'noFactura': recaudo.noFactura,
                            'fechaFacturacion': recaudo.fechaFacturacion,
                            'fechaEntrega': formato_fecha(recaudo.fechaEntrega), 
                            'efectivo': recaudo.efectivo,
                            'tarjeta': mascara_tarjeta(recaudo.tarjeta),
                            'estado': recaudo.estado,
                            'activa': recaudo.activa,
                            'total': recaudo.total,
                            'subtotal':recaudo.subtotal,
                            'cambio': recaudo.cambio,
                            'descuento': recaudo.descuento,
                            'impuesto': recaudo.impuesto,
                            'idDescuento': {},
                            'idCorrelativo':{
                                'id': recaudo.idCorrelativo.id,
                                'cai': recaudo.idCorrelativo.cai,
                                'rangoInicial': recaudo.idCorrelativo.rangoInicial,
                                'rangoFinal': recaudo.idCorrelativo.rangoFinal,
                                'consecutivo': recaudo.idCorrelativo.consecutivo,
                                'fechaLimiteEmision': recaudo.idCorrelativo.fechaLimiteEmision,
                                'fechaInicio': recaudo.idCorrelativo.fechaInicio
                            },
                            'idConsulta':{
                            },
                            'idPaciente':{},
                            'idEmpleado':{
                                'id':recaudo.idEmpleado.id,
                                'nombre':recaudo.idEmpleado.nombre,
                                'documento':recaudo.idEmpleado.documento
                            },
                            'idMetodoPago':{
                                'id':recaudo.idMetodoPago.id,
                                'nombre':recaudo.idMetodoPago.nombre
                            },
                            'medicamentos':{},
                            'tratamientos':{},
                            'examenes':{}
                        }
                        if(recaudo.idDescuento):
                            descuento_dict = {
                                'id':recaudo.idDescuento.id,
                                'valor':recaudo.idDescuento.valor,

                            }
                            recaudo_dict['idDescuento'] = descuento_dict
                        if(recaudo.idConsulta):
                            consulta_dict = {
                                'id':recaudo.idConsulta.id,
                                'precio':recaudo.idConsulta.idTipo.precio,
                                'impuesto':recaudo.idConsulta.idTipo.idImpuesto.valor,
                                'tipo':recaudo.idConsulta.idTipo.nombre,
                                'paciente':recaudo.idConsulta.idCita.idPaciente.documento,
                            }
                            recaudo_dict['idConsulta'] = consulta_dict
                        if (recaudo.idPaciente):
                            recaudo_dict = buscar_paciente(recaudo_dict,recaudo.idPaciente.id)
                        else:
                            recaudo_dict = buscar_paciente(recaudo_dict,0)
                        medicamentos = RecaudoDetalleMedicamento.objects.filter(idRecaudo = recaudo.id).select_related('idMedicamento')
                        medicamento_dict = {}
                        for medicamento in medicamentos:
                            medicamento_dict = {
                                'id': medicamento.idMedicamento.id,
                                'nombre': medicamento.idMedicamento.nombre
                            }
                            recaudo_dict['medicamentos'][medicamento.idMedicamento.id] = medicamento_dict
                        tratamientos = RecaudoDetalleTratamiento.objects.filter(idRecaudo = recaudo.id).select_related('idTratamiento')
                        tratamientos_dict = {}
                        for tratamiento in tratamientos:
                            tratamientos_dict = {
                                'id': tratamiento.idTratamiento.id,
                                'nombre': tratamiento.idTratamiento.idTipo.nombre
                            }
                            recaudo_dict['tratamientos'][tratamiento.idTratamiento.id] = tratamientos_dict
                        examenes = RecaudoDetalleExamen.objects.filter(idRecaudo = recaudo.id).select_related('idExamen')
                        examenes_dict = {}
                        for examen in examenes:
                            examenes_dict = {
                                'id': examen.idExamen.id,
                                'nombre': examen.idExamen.idTipo.nombre
                            }
                            recaudo_dict['examenes'][examen.idExamen.id] = examenes_dict
                        recaudos_values.append(recaudo_dict)

                    context = {
                        'message': "Consulta exitosa",
                        'recaudo': recaudos_values
                    }
                    return JsonResponse(context)
                else:
                    recaudo_values = []
                    context = {
                        'message': "No se encontraron los datos",
                        'recaudo': recaudo_values
                    }
                    return JsonResponse(context)
            return JsonResponse(context)


#Agregar un registro de cargos
    def post(self, request):
        jd=json.loads(request.body)

        estados_permitidos = ['Pendiente', 'Enviada', 'Pagada', 'Vencida', 'Anulada']
        if jd['estado'] not in estados_permitidos:
            mensaje_post = {'message': "Seleccione un estado existente."}
        elif int(jd['correlativo']) == 0:
            mensaje_post = {'message': "Seleccione el correlativo del SAR"}
        elif int(jd['idConsulta']) == 0 and jd['medicamentos'] == [] and jd['tratamientos'] == [] and jd['examenes'] == []:
            mensaje_post = {'message': "No hay detalles relacionados"}
        elif int(jd['idMetodo']) == 0:
            mensaje_post = {'message': "Seleccione un metodo de pago"}
        elif int(jd['idMetodo']) == 1 and (jd['numeroTarjeta'] is None or jd['numeroTarjeta'] == ''):
            mensaje_post = {'message': "El número de tarjeta está vacío"}
        elif int(jd['idMetodo']) == 1 and not (jd['numeroTarjeta']).isdigit():
            mensaje_post = {'message': "El número de tarjeta solo puede contener dígitos(Sin espacios o caracteres especiales)"}
        elif int(jd['idMetodo']) == 1 and not validar_cadena_tarjeta(jd['numeroTarjeta']):
            mensaje_post = {'message': "El número de tarjeta solo puede contener dígitos, min:16 y max:19"}
        elif int(jd['idMetodo']) == 1 and len(jd['numeroTarjeta']) < 13:
            mensaje_post = {'message': "El número de tarjeta es muy corto"}
        elif int(jd['idMetodo']) == 1 and len(jd['numeroTarjeta']) > 19:
            mensaje_post = {'message': "El número de tarjeta es muy largo"}
        elif int(jd['idMetodo']) == 1 and (jd['montoTarjeta'] is None or jd['montoTarjeta'] == ''):
            mensaje_post = {'message': "El monto de la tarjeta está vacío"}
        elif int(jd['idMetodo']) == 2 and (jd['montoEfectivo'] is None or jd['montoEfectivo'] == ''):
            mensaje_post = {'message': "El efectivo está vacío"}
        elif int(jd['idMetodo']) == 2 and round(Decimal(jd['montoEfectivo']),2) < 0:
            mensaje_post = {'message': "El efectivo debe ser positivo"}
        elif int(jd['idMetodo']) == 2 and round(Decimal(jd['montoEfectivo']),2) < round(Decimal(jd['total']),2):
            mensaje_post = {'message': "El efectivo debe ser mayor o igual al total"}
        elif int(jd['idMetodo']) == 2 and round(Decimal(jd['montoEfectivo']),2) > 999999999:
            mensaje_post = {'message': "El efectivo es muy grande"}
        elif int(jd['idMetodo']) == 3 and (jd['numeroTarjeta'] is None or jd['numeroTarjeta'] == '') and (jd['montoEfectivo'] is None or jd['montoEfectivo'] == ''):
            mensaje_post = {'message': "El Numero de tarjeta o Monto efectivo esta vacío"}
        elif int(jd['idMetodo']) == 3 and not (jd['numeroTarjeta']).isdigit():
            mensaje_post = {'message': "El número de tarjeta solo puede contener dígitos"}
        elif int(jd['idMetodo']) == 3 and not validar_cadena_tarjeta(jd['numeroTarjeta']):
            mensaje_post = {'message': "El número de tarjeta solo puede contener dígitos, min:16 y max:19"}
        elif int(jd['idMetodo']) == 3 and len(jd['numeroTarjeta']) < 13:
            mensaje_post = {'message': "El número de tarjeta es muy corto"}
        elif int(jd['idMetodo']) == 3 and len(jd['numeroTarjeta']) > 19:
            mensaje_post = {'message': "El número de tarjeta es muy largo"}
        elif int(jd['idMetodo']) == 3 and round(Decimal(jd['montoEfectivo']),2) < 0:
            mensaje_post = {'message': "El efectivo debe ser positivo"}
        elif int(jd['idMetodo']) == 3 and round(Decimal(jd['montoEfectivo']),2) >= round(Decimal(jd['total']),2):
            mensaje_post = {'message': "El efectivo debe ser menor total"}
        elif int(jd['idMetodo']) == 3 and round(Decimal(jd['montoEfectivo']),2) > 999999999:
            mensaje_post = {'message': "El efectivo es muy grande"}
        else:
            if jd['montoEfectivo']:
                efectivo = round(Decimal(jd['montoEfectivo']),2)
            else: 
                efectivo = None
            if jd['cambio']:
                cambio = round(Decimal(jd['cambio']),2)
            else: 
                cambio = None
            if jd['imp']:
                impuesto = round(Decimal(jd['imp']),2)
            else: 
                impuesto = None
            if jd['descuento']:
                descuento = round(Decimal(jd['descuento']),2)
            else: 
                descuento = None
            total = round(Decimal(jd['total']),2)
            subtotal = round(Decimal(jd['subtotal']),2)


            fecha = date.today()


            correlativo = instanciar_correlativo(int(jd['correlativo']))
            consecutivo = correlativo.consecutivo
            if(correlativo.activo == 0):
                mensaje_post = {'message': "El correlativo ha sido desactivado por motivos de seguridad"}
            elif not(correlativo.fechaLimiteEmision > date.today()):
                mensaje_post = {'message': "La fecha limite de emision del correlativo ha vencido, ha sido desactivado"}
                correlativo.activo = 0
                correlativo.save()
            elif (correlativo.consecutivo > correlativo.rangoFinal):
                mensaje_post = {'message': "El consecutivo de la factura superó el rango límite de facturación, ha sido desactivado"}
                correlativo.activo = 0
                correlativo.save()
            else:
                con = str(consecutivo).zfill(6)
                rInicio = str(correlativo.rangoInicial).zfill(6)
                rFinal = str(correlativo.rangoFinal).zfill(6)
                numeroFactura = f'{correlativo.rangoFinal} { correlativo.fechaLimiteEmision.day }-{ correlativo.fechaLimiteEmision.month }-{ correlativo.fechaLimiteEmision.year } { con }'
                rangoInicialF = f'{correlativo.rangoFinal} { correlativo.fechaLimiteEmision.day }-{ correlativo.fechaLimiteEmision.month }-{ correlativo.fechaLimiteEmision.year } { rInicio }'
                rangoFinalF = f'{correlativo.rangoFinal} { correlativo.fechaLimiteEmision.day }-{ correlativo.fechaLimiteEmision.month }-{ correlativo.fechaLimiteEmision.year } { rFinal }'
                datos_pdf = {}
                if instanciar_paciente(int(jd['idPaciente'])):
                    if instanciar_consulta(int(jd['idConsulta'])):
                        consulta = instanciar_consulta(int(jd['idConsulta']))
                        consulta.pagado = 1
                        consulta.save()
                    else:
                        consulta = None

                    condicion = 0
                    nombres = ''
                    for item in jd['medicamentos']:
                        registro = instanciar_medicamento(int(item['id']))
                        if (registro.stockActual - registro.stockMinimo) < int(item['cantidad']):
                            condicion += 1
                            nombres += item['nombre'] + ", "
                    if condicion != 0:
                        mensaje_post = {'message': f"Compruebe la cantidad de los productos en base al stock minimo y actual Productos:[{nombres}]"}
                    else:
                        if(correlativo.activo == 0):
                            mensaje_post = {'message': "El correlativo ha sido desactivado por motivos de seguridad"}
                        elif (correlativo.fechaLimiteEmision <= date.today()):
                            mensaje_post = {'message': "La fecha limite de emision del correlativo ha vencido, ha sido desactivado"}
                            correlativo.activo = 0
                            correlativo.save()
                        elif (correlativo.consecutivo > correlativo.rangoFinal):
                            mensaje_post = {'message': "El consecutivo de la factura superó el rango límite de facturación, ha sido desactivado"}
                            correlativo.activo = 0
                            correlativo.save()
                        else:
                            recaudo = Recaudo.objects.create(
                                idCorrelativo = instanciar_correlativo(int(jd['correlativo'])),
                                noFactura = numeroFactura,
                                idPaciente = instanciar_paciente(int(jd['idPaciente'])),
                                fechaFacturacion = jd['fechaActual'],
                                fechaEntrega = fecha,
                                idEmpleado = instanciar_empleado(int(jd['idEmpleado'])),
                                idMetodoPago = instanciar_metodo(int(jd['idMetodo'])),
                                idConsulta = consulta,
                                efectivo = efectivo,
                                tarjeta = jd['numeroTarjeta'],
                                estado = 'Pagada',
                                activa = 1,
                                total = total,
                                subtotal = subtotal,
                                descuento = descuento,
                                impuesto = impuesto,
                                idDescuento = instanciar_descuento(jd['idDescuento']),
                                cambio = cambio
                            )
                            if jd['medicamentos']:
                                for item in jd['medicamentos']:
                                    registro = instanciar_medicamento(int(item['id']))
                                    registro.stockActual -= int(item['cantidad'])
                                    registro.save()
                                    RecaudoDetalleMedicamento.objects.create(idRecaudo=recaudo, idMedicamento = registro, cantidad=int(item['cantidad']))

                            if jd['tratamientos']:
                                for item in jd['tratamientos']:
                                    registro = instanciar_tratamiento(int(item['id']))
                                    registro.pagado = 1
                                    registro.save()
                                    RecaudoDetalleTratamiento.objects.create(idRecaudo=recaudo, idTratamiento = registro)
                            if jd['examenes']:
                                for item in jd['examenes']:
                                    registro = instanciar_examen(int(item['id']))
                                    registro.pagado = 1
                                    registro.save()
                                    RecaudoDetalleExamen.objects.create(idRecaudo=recaudo, idExamen = registro)

                            correlativo.consecutivo += 1           
                            correlativo.save() 

                            nombreEmpresa = ParametrosGenerales.objects.filter(nombre = 'nombre').last()
                            direccionEmpresa = ParametrosGenerales.objects.filter(nombre = 'direccion').last()
                            telefonoEmpresa = ParametrosGenerales.objects.filter(nombre = 'telefono').last()
                            correoEmpresa = ParametrosGenerales.objects.filter(nombre = 'correo').last()
                            rtnEmpresa = ParametrosGenerales.objects.filter(nombre = 'rtn').last()
                            empleado = instanciar_empleado(int(jd['idEmpleado']))
                            metodo = instanciar_metodo(int(jd['idMetodo']))
                            cliente = instanciar_paciente(int(jd['idPaciente']))
                                
                            datos_pdf = {
                                'nombreEmpresa':nombreEmpresa.valor,
                                'direccionEmpresa':direccionEmpresa.valor,
                                'telefonoEmpresa':telefonoEmpresa.valor,
                                'correoEmpresa':correoEmpresa.valor,
                                'rtnEmpresa':rtnEmpresa.valor,
                                'caiEmpresa':correlativo.cai,
                                'numeroFactura':numeroFactura,
                                'fechaFactura':recaudo.fechaFacturacion,
                                'fechaLimite':formato_fecha(correlativo.fechaLimiteEmision),
                                'nombreEmpleado':empleado.nombre + " " + empleado.apellidos,
                                'nombreCliente':cliente.nombre + " " + cliente.apellido,
                                'documentoCliente':cliente.documento,
                                'telefonoCliente':cliente.telefono,
                                'correoCliente':cliente.correo,
                                'direccionCliente':cliente.direccion,
                                'metodoPago':metodo.nombre,
                                'rangoInicial':rangoInicialF,
                                'rangoFinal':rangoFinalF
                            }
                            mensaje_post = {'message':"Registro Exitoso.", 'numeroFactura': numeroFactura, 'datos_pdf':datos_pdf}
                else:
                    if instanciar_consulta(int(jd['idConsulta'])):
                        consulta = instanciar_consulta(int(jd['idConsulta']))
                        consulta.pagado = 1
                        consulta.save()
                    else:
                        consulta = None
                    if jd['cambio']:
                        cambio = round(Decimal(jd['cambio']),2)
                    else: 
                        cambio = None
                    if jd['imp']:
                        impuesto = round(Decimal(jd['imp']),2)
                    else: 
                        impuesto = None
                    if jd['descuento']:
                        descuento = round(Decimal(jd['descuento']),2)
                    else: 
                        descuento = None
                    total = round(Decimal(jd['total']),2)
                    subtotal = round(Decimal(jd['subtotal']),2)

                    condicion = 0
                    nombres = ''
                    for item in jd['medicamentos']:
                        registro = instanciar_medicamento(int(item['id']))
                        if (registro.stockActual - registro.stockMinimo) < int(item['cantidad']):
                            condicion += 1
                            nombres += item['nombre'] + ", "
                    if condicion != 0:
                        mensaje_post = {'message': f"Compruebe la cantidad de los productos en base al stock minimo y actual Productos:[{nombres}]"}
                    else:
                        if(correlativo.activo == 0):
                            mensaje_post = {'message': "El correlativo ha sido desactivado por motivos de seguridad"}
                        elif (correlativo.fechaLimiteEmision <= date.today()):
                            mensaje_post = {'message': "La fecha limite de emision del correlativo ha vencido, ha sido desactivado"}
                            correlativo.activo = 0
                            correlativo.save()
                        elif (correlativo.consecutivo > correlativo.rangoFinal):
                            mensaje_post = {'message': "El consecutivo de la factura superó el rango límite de facturación, ha sido desactivado"}
                            correlativo.activo = 0
                            correlativo.save()
                        else:
                            recaudo = Recaudo.objects.create(
                                idCorrelativo = instanciar_correlativo(int(jd['correlativo'])),
                                noFactura = numeroFactura,
                                fechaFacturacion = jd['fechaActual'],
                                fechaEntrega = fecha,
                                idEmpleado = instanciar_empleado(int(jd['idEmpleado'])),
                                idMetodoPago = instanciar_metodo(int(jd['idMetodo'])),
                                idConsulta = consulta,
                                efectivo = efectivo,
                                tarjeta = jd['numeroTarjeta'],
                                estado = 'Pagada',
                                activa = 1,
                                total = total,
                                subtotal = subtotal,
                                descuento = descuento,
                                impuesto = impuesto,
                                idDescuento = instanciar_descuento(jd['idDescuento']),
                                cambio = cambio
                            )
                            if jd['medicamentos']:
                                for item in jd['medicamentos']:
                                    registro = instanciar_medicamento(int(item['id']))
                                    registro.stockActual -= int(item['cantidad'])
                                    registro.save()
                                    RecaudoDetalleMedicamento.objects.create(idRecaudo=recaudo, idMedicamento = registro, cantidad=int(item['cantidad']))
                            if jd['tratamientos']:
                                for item in jd['tratamientos']:
                                    registro = instanciar_tratamiento(int(item['id']))
                                    registro.pagado = 1
                                    registro.save()
                                    RecaudoDetalleTratamiento.objects.create(idRecaudo=recaudo, idTratamiento = registro)
                            if jd['examenes']:
                                for item in jd['examenes']:
                                    registro = instanciar_examen(int(item['id']))
                                    registro.pagado = 1
                                    registro.save()
                                    RecaudoDetalleExamen.objects.create(idRecaudo=recaudo, idExamen = registro)

                            correlativo.consecutivo += 1
                            correlativo.save()

                            nombreEmpresa = ParametrosGenerales.objects.filter(nombre = 'nombre').last()
                            direccionEmpresa = ParametrosGenerales.objects.filter(nombre = 'direccion').last()
                            telefonoEmpresa = ParametrosGenerales.objects.filter(nombre = 'telefono').last()
                            correoEmpresa = ParametrosGenerales.objects.filter(nombre = 'correo').last()
                            rtnEmpresa = ParametrosGenerales.objects.filter(nombre = 'rtn').last()
                            empleado = instanciar_empleado(int(jd['idEmpleado']))
                            metodo = instanciar_metodo(int(jd['idMetodo']))
                                
                            datos_pdf = {
                                'nombreEmpresa':nombreEmpresa.valor,
                                'direccionEmpresa':direccionEmpresa.valor,
                                'telefonoEmpresa':telefonoEmpresa.valor,
                                'correoEmpresa':correoEmpresa.valor,
                                'rtnEmpresa':rtnEmpresa.valor,
                                'caiEmpresa':correlativo.cai,
                                'numeroFactura':numeroFactura,
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
                                'rangoFinal':rangoFinalF
                            }
                            mensaje_post = {'message':"Registro Exitoso.", 'numeroFactura': numeroFactura, 'datos_pdf':datos_pdf}
        return JsonResponse(mensaje_post)

#Actualizar un registro de cargos
    def put(self, request,id):
        try:
            jd=json.loads(request.body)
            mensaje_put = list(Recaudo.objects.filter(id=id).values())
            if len(mensaje_put) > 0:
                recaudo=Recaudo.objects.get(id=id)
                estados_permitidos = ['Pendiente', 'Enviada', 'Pagada', 'Vencida', 'Anulada']

                if jd['estado'] not in estados_permitidos:
                    mensaje_put = {'message': "Seleccione un estado existente."}
                else:
                    if jd['estado'] == 'Pendiente':
                        activa = 1
                        fecha = None
                    elif jd['estado'] == 'Enviada' or jd['estado'] == 'Pagada' or jd['estado'] == 'Vencida':
                        activa = 1
                        fecha = date.today()
                    elif jd['estado'] == 'Anulada':
                        activa = 0
                        fecha = None
                    else:
                        activa = 0
                        fecha = None
                        
                    recaudo.estado = jd['estado']
                    recaudo.activa = activa
                    recaudo.fechaEntrega = fecha
                    recaudo.save()
                    mensaje_put = {'message': "La actualización fue exitosa."}
            return JsonResponse(mensaje_put)
        except Exception as e:
            mensaje_put = {'message': f"Error: {e}"}
            return JsonResponse(mensaje_put)
        
#Eliminar un registro de cargos
    def delete(self, request,id):
        recaudos = list(Recaudo.objects.filter(id=id).values())
        if len(recaudos) > 0:
            examenes = list(RecaudoDetalleExamen.objects.filter(idRecaudo=id).values())
            if len(examenes) > 0:
                for item in examenes:
                    RecaudoDetalleExamen.objects.filter(id=item['id']).delete()
            tratamientos = list(RecaudoDetalleTratamiento.objects.filter(idRecaudo=id).values())
            if len(tratamientos) > 0:
                for item in tratamientos:
                    RecaudoDetalleTratamiento.objects.filter(id=item['id']).delete()
            medicamentos = list(RecaudoDetalleMedicamento.objects.filter(idRecaudo=id).values())
            if len(medicamentos) > 0:
                for item in medicamentos:
                    RecaudoDetalleMedicamento.objects.filter(id=item['id']).delete()
            Recaudo.objects.filter(id=id).delete()
            datos = {'message':"Registro Eliminado"}
        else:
            datos = {'message':"No se encontraron registros", 'enfermedades': []}
        return JsonResponse(datos)
    

def buscar_paciente(diccionario, id):
    registros = Paciente.objects.filter(id=id)
    if registros:
        for registro in registros:
            diagnostico_dict = {
                'id': registro.id,
                'nombre': registro.nombre + " " + registro.apellido,
                'documento': registro.documento
            }
            diccionario['idPaciente'] = diagnostico_dict
        return diccionario
    else:
        diagnostico_dict = {
            'id': 0,
            'nombre': 'Consumidor Final'
        }
        diccionario['idPaciente'] = diagnostico_dict
        return diccionario
    
def instanciar_correlativo(id):
    if (id > 0):
        item = CorrelativoSar.objects.filter(id=id).last()
        if item:
            return item
    
def instanciar_paciente(id):
    if (id > 0):
        item = Paciente.objects.filter(id=id).last()
        if item:
            return item
        else:
            return None

def instanciar_empleado(id):
    if (id > 0):
        item = Empleado.objects.filter(id=id).last()
    if item:
        return item
    else:
        return None

def instanciar_metodo(id):
    if (id > 0):
        item = MetodoDePago.objects.filter(id=id).last()
    if item:
        return item
    else:
        return None

def instanciar_descuento(id):
    if (id > 0):
        item = Descuento.objects.filter(id=id).last()
    if item:
        return item
    else:
        return None

def instanciar_consulta(id):
    if (id > 0):
        item = Consulta.objects.filter(id=id).last()
        if item:
            return item
        else:
            return None
    
def instanciar_medicamento(id):
    if (id > 0):
        item = Medicamento.objects.filter(id=id).last()
    if item:
        return item
    else:
        return None
    
def instanciar_tratamiento(id):
    if (id > 0):
        item = Tratamiento.objects.filter(id=id).last()
    if item:
        return item
    else:
        return None

def instanciar_examen(id):
    if (id > 0):
        item = Examen.objects.filter(id=id).last()
    if item:
        return item
    else:
        return None

def validar_cadena_tarjeta(cadena):
    patron = r'^[0-9]{13,19}$'
    return bool(re.search(patron, cadena))

def validar_cadena_repeticion(cadena):
    patron = r'([a-zA-Z])\1\1'
    return bool(re.search(patron, cadena))

def validar_cadena_espacios(cadena):
    patron = r'^[^ ]+(?: {0,1}[^ ]+)*$'
    return bool(re.match(patron,cadena))

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
