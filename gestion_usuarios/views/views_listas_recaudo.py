from django.http.response import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
import re
from ..models import *
from django.views.decorators.http import require_http_methods

@method_decorator(require_http_methods(['POST','PUT','GET','DELETE']), name='dispatch')
class ListasRecaudo(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):

        pacientes  = list(Paciente.objects.values())
        if not pacientes:
            pacientes = []
        usuarios = Usuario.objects.filter(sesion=1).select_related('idEmpleado')
        if(usuarios):
            empleados = list(Empleado.objects.filter(id=usuarios[0].idEmpleado.id).values())
        else:
            empleados = []
            
        sar = list(CorrelativoSar.objects.filter(activo=1).values())
        if not sar:
            sar = []
        metodo = list(MetodoDePago.objects.values())
        if not metodo:
            metodo = []
        descuento = list(Descuento.objects.values())
        if not descuento:
            descuento = []
        consultas = consultas_metodo()
        tratamientos = tratamientos_metodo()
        examenes = examenes_metodo()
        medicamentos = medicamentos_metodo()

        context = {'mensaje':''}
        if not pacientes:
            mensaje = 'No se encontrarón pacientes'
        elif not empleados:
            mensaje = 'No se encontrarón empleados activos'
        elif not consultas and not medicamentos and not tratamientos and not examenes:
            mensaje = 'No se encontrarón los productos y servicios'
        elif not sar:
            mensaje = 'No se encontró el correlativo sar'
        elif not metodo:
            mensaje = 'No se encontrarón metodos de pago'
        elif not descuento:
            mensaje = 'No se encontrarón descuentos'
        else:

            context['pacientes_list'] = pacientes
            context['empleados_list'] = empleados
            context['sar_list'] = sar
            context['metodo_list'] = metodo
            context['descuento_list'] = descuento
            context['consultas_list'] = consultas
            context['medicamentos_list'] = medicamentos
            context['tratamientos_list'] = tratamientos
            context['examenes_list'] = examenes

            mensaje = 'Consulta Exitosa'
        context['mensaje'] = str(mensaje)
        return JsonResponse(context)

def consultas_metodo():
    consultas = Consulta.objects.filter(pagado=0).select_related('idCita','idTipo')
    consultas_values = []
    if consultas is not None:
        for consulta in consultas:
            consulta_dict = {
                'id': consulta.id,
                'fecha': formato_fecha(consulta.fecha),
                'recomendaciones': consulta.recomendaciones,
                'informacionAdicional': consulta.informacionAdicional,
                'idCita':{
                    'id':consulta.idCita.id,
                    'idPaciente': {
                        'id': consulta.idCita.idPaciente.id,
                        'nombre': consulta.idCita.idPaciente.nombre,
                        'documento': consulta.idCita.idPaciente.documento,
                        'id': consulta.idCita.id,
                        'fechaProgramada': formato_fecha(consulta.idCita.fechaProgramada),
                        'fechaMaxima': formato_fecha(consulta.idCita.fechaMaxima)
                    }
                },
                'idTipo':{
                    'id':consulta.idTipo.id,
                    'nombre':consulta.idTipo.nombre,
                    'precio':consulta.idTipo.precio,
                    'impuesto':consulta.idTipo.idImpuesto.valor,
                    'subtipo':consulta.idTipo.idsubtipo.nombre
                },
                'idDiagnostico':{}                        
            }
            diagnosticos = ConsultaDetalle.objects.filter(idConsulta=consulta.id).select_related('idDiagnostico')
            for diagnostico in diagnosticos:
                    diagnostico_dict = {
                        'id': diagnostico.idDiagnostico.id,
                        'descripcion': diagnostico.idDiagnostico.descripcion
                    }
                    consulta_dict['idDiagnostico'][diagnostico.idDiagnostico.id] = diagnostico_dict
            consultas_values.append(consulta_dict)

    return consultas_values

def tratamientos_metodo():
    reg = Tratamiento.objects.filter(pagado=0).select_related('idPaciente','idTipo')
    tratamientos_values = []
    if reg is not None:
        for tratamiento in reg:
            paciente = tratamiento.idPaciente
            tratamiento_dict = {
                'id': tratamiento.id,
                'fecha': formato_fecha(tratamiento.fecha),
                'diasTratamiento':tratamiento.diasTratamiento,
                'estado': tratamiento.estado,
                'idPaciente': {
                    'id': paciente.id,
                    'nombre': paciente.nombre  +' '+ paciente.apellido,
                    'documento': paciente.documento
                },
                'idTipo': {
                        'id': tratamiento.idTipo.id,
                        'nombre': tratamiento.idTipo.nombre,
                        'impuesto':tratamiento.idTipo.idImpuesto.valor,
                        'precio': tratamiento.idTipo.precio
                    }
            }
            tratamientos_values.append(tratamiento_dict)
    return tratamientos_values


def examenes_metodo():
    examenes = Examen.objects.filter(pagado=0).select_related('idMuestra','idTipo','idLaboratorio')
    examenes_values = []
    if examenes is not None:
        for examen in examenes:
            examen_dict = {
                    'id': examen.id,
                    'fecha': formato_fecha(examen.fecha),
                    'fechaProgramada': formato_fecha(examen.fechaProgramada),
                    'observacion': examen.observacion,
                    'idMuestra':{
                        'id':examen.idMuestra.id,
                        'idPaciente': {
                        'id': examen.idMuestra.idPaciente.id,
                        'nombre': examen.idMuestra.idPaciente.nombre +" "+ examen.idMuestra.idPaciente.apellido,
                        'documento': examen.idMuestra.idPaciente.documento,                              
                        }        
                    },   
                    'idTipo': {
                    'id': examen.idTipo.id,
                    'nombre': examen.idTipo.nombre,
                    'subtipo': examen.idTipo.idsubtipo.nombre,
                    'impuesto':examen.idTipo.idImpuesto.valor,
                    'precio': examen.idTipo.precio
                    
                    },
                    'idLaboratorio': {
                        'id': examen.idLaboratorio.id,
                        'nombre': examen.idLaboratorio.nombre,
                    }     
                }           
            examenes_values.append(examen_dict)

    return examenes_values

def medicamentos_metodo():
    medicamentos = Medicamento.objects.select_related('idImpuesto','idTipo','idProveedor')
    medicamentos_values = []
    if medicamentos is not None:
        for medicamento in medicamentos:
            medicamento_dict = {
                "id": medicamento.id,
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
     
    return medicamentos_values

def formato_fecha(fecha):
    if fecha is not None:
        fecha_formateada = fecha.strftime("%d-%m-%Y")
        return fecha_formateada
    else:
        return None