from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget, ManyToManyWidget
from .models import HistoriasClinicas, Mascotas, Empleados

class HistoriasClinicasResource(resources.ModelResource):
    # Traer el nombre del campo 'mascotas' en lugar del ID
    mascotas = fields.Field(
        column_name='mascotas',
        attribute='mascotas',
        widget=ForeignKeyWidget(Mascotas, 'nombreMas')  # Aquí defines el campo que quieres mostrar
    )
    
    # Para el ManyToManyField, puedes concatenar los nombres de los veterinarios
    veterinario = fields.Field(
        column_name='veterinarios',
        attribute='veterinario',
        readonly=True,
    )

    def dehydrate_veterinario(self, obj):
        # Concatenar los nombres de los veterinarios (user.first_name) separados por comas
        return ', '.join([vet.user.first_name for vet in obj.veterinario.all()])

    class Meta:
        model = HistoriasClinicas
        fields = (
            'mascotas', 'fecha', 'hora', 'quejaPrincipal', 'tratamientosPrevios', 
            'enfermedadesAnteriores', 'cirugiasAnteriores', 'dieta', 
            'medicinaPreventiva', 'temperatura', 'pulso', 'respiracion', 
            'inspeccion', 'TLIC', 'hidratacion', 'peso', 'ganglios', 
            'sistDigestivo', 'sistRespiratorio', 'sistCardiovascular', 
            'sistUrinario', 'sistGenital', 'sistNervioso', 'sistLocomotor', 
            'pielAnexos', 'hallazgos', 'examenesSolicitados', 'examenesAutorizados',
            'impresionDiagnostica', 'pronostico', 'tratamientoIdeal', 'cotizacion1',
            'tratamientoInstaurado', 'cotizacion2', 'observaciones', 'consideraciones', 
            'veterinario',
        )
        export_order = fields
