from datetime import datetime, timedelta
from django.http.response import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
import re
from ..models import *
from django.views.decorators.http import require_http_methods

@method_decorator(require_http_methods(['POST','PUT','GET','DELETE']), name='dispatch')
class DatosPermisos(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        usuarios = Usuario.objects.filter(sesion=1).select_related('idEmpleado')
        if usuarios:
            empleados = list(Empleado.objects.filter(id=usuarios[0].idEmpleado.id).values())
        permisos = Permisos.objects.filter(idCargoEmpleado=empleados[0]['idCargoEmpleado_id'],activo=1).select_related('idAcciones','idCargoEmpleado','idPantallas').order_by('idPantallas__nombre')

        output = {"permisos": []}
        acciones_por_cargo = {}
        for permiso in permisos:
            id_cargo_empleado = permiso.idCargoEmpleado.nombre
            nombre_pantalla = permiso.idPantallas.nombre
            id_accion = permiso.idAcciones.nombre

            if id_cargo_empleado in acciones_por_cargo:
                acciones_pantalla = acciones_por_cargo[id_cargo_empleado]
                if nombre_pantalla in acciones_pantalla:
                    acciones_pantalla[nombre_pantalla].append(id_accion)
                else:
                    acciones_pantalla[nombre_pantalla] = [id_accion]
            else:
                acciones_por_cargo[id_cargo_empleado] = {nombre_pantalla: [id_accion]}

        for id_cargo_empleado, acciones_pantalla in acciones_por_cargo.items():
            output["permisos"].append({
                "idCargoEmpleado": id_cargo_empleado,
                "idPantallas": acciones_pantalla
            })

        return JsonResponse(output)