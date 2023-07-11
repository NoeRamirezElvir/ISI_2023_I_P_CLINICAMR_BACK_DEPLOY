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
        #usuarios = Usuario.objects.filter(sesion=1).select_related('idEmpleado')
        #if(usuarios):
        #    empleados = Empleado.objects.filter(id=usuarios[0].idEmpleado.id).values()
        #cargo = CargoEmpleado.objects.filter(id=empleados[0].idCargoEmpleado.id).values()
        #permisos = Permisos.objects.filter(idCargoEmpleado=cargo[0].id).values()
        
        permisos = Permisos.objects.all()
        data = {'permisos':permisos}
        return JsonResponse(data)