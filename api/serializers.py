from rest_framework import serializers
from .models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    imagen_usuario = serializers.ImageField(required=False)

    class Meta:
        model = CustomUser
        fields = ('dni', 'apel_nomb', 'tipo_usuarioapp', 'password', 'imagen_usuario', 'descripcion', 'fecha_nacimiento', 'telefono', 'gmail')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        imagen_usuario = validated_data.pop('imagen_usuario', None)
        user = CustomUser.objects.create_user(**validated_data)
        if imagen_usuario:
            user.imagen_usuario = imagen_usuario
            user.save()
        return user

    def update(self, instance, validated_data):
        imagen_usuario = validated_data.pop('imagen_usuario', None)
        instance.apel_nomb = validated_data.get('apel_nomb', instance.apel_nomb)
        instance.tipo_usuarioapp = validated_data.get('tipo_usuarioapp', instance.tipo_usuarioapp)
        instance.descripcion = validated_data.get('descripcion', instance.descripcion)
        instance.fecha_nacimiento = validated_data.get('fecha_nacimiento', instance.fecha_nacimiento)
        instance.telefono = validated_data.get('telefono', instance.telefono)
        instance.gmail = validated_data.get('gmail', instance.gmail)
        
        # No actualizar la contraseña
        # instance.password = validated_data.get('password', instance.password)
        
        if imagen_usuario:
            instance.imagen_usuario = imagen_usuario
        instance.save()
        return instance
    
from rest_framework import serializers
from .models import Empresa

class EmpresaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empresa
        fields = ('idempresa', 'nombre')
        read_only_fields = ('idempresa',)  # Esto hace que idempresa no sea requerido en la solicitud

    def create(self, validated_data):
        return Empresa.objects.create(**validated_data)


from rest_framework import serializers
from .models import TipoEnvio

class TipoEnvioSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoEnvio
        fields = '__all__'


from .models import Responsable
class ResponsableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Responsable
        fields = ('idresponsable', 'nombre_apellido')
        read_only_fields = ('idresponsable',)  # Esto hace que idempresa no sea requerido en la solicitud

    def create(self, validated_data):
        return Responsable.objects.create(**validated_data)

from rest_framework import serializers
from .models import Planilla

class PlanillaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Planilla
        fields = ['idplanilla', 'nombre']

from rest_framework import serializers
from .models import Emisor

class EmisorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Emisor
        fields = ('idemisor', 'nombre')
        read_only_fields = ('idemisor',)  # Esto hace que idempresa no sea requerido en la solicitud

    def create(self, validated_data):
        return Emisor.objects.create(**validated_data)
    

    from rest_framework import serializers
from .models import Especie

class EspecieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Especie
        fields = ('idespecie', 'nombre')
        read_only_fields = ('idespecie',)  # Esto hace que idempresa no sea requerido en la solicitud

    def create(self, validated_data):
        return Especie.objects.create(**validated_data)

from .models import Turno

class TurnoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Turno
        fields = ('idturno', 'nombre')
        read_only_fields = ('idturno',)  # Esto hace que idempresa no sea requerido en la solicitud

    def create(self, validated_data):
        return Turno.objects.create(**validated_data)



    

from .models import Consumidor
class ConsumidorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consumidor
        fields = ('idconsumidor', 'nombre_apellido')
        read_only_fields = ('idconsumidor',)  # Esto hace que idempresa no sea requerido en la solicitud

    def create(self, validated_data):
        return Consumidor.objects.create(**validated_data)


# ------------------------------------------------------------------------------------
# ImportarAsistenciaDetalleSerializer
from rest_framework import serializers
from .models import ImportarAsistenciaDetalle

class ImportarAsistenciaDetalleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImportarAsistenciaDetalle
        fields = '__all__'

    def create(self, validated_data):
        # Crear y devolver la instancia del modelo ImportarAsistenciaDetalle
        return ImportarAsistenciaDetalle.objects.create(**validated_data)

    def update(self, instance, validated_data):
        # Actualizar y devolver la instancia del modelo ImportarAsistenciaDetalle
        instance.idcodigogeneral = validated_data.get('idcodigogeneral', instance.idcodigogeneral)
        instance.idactividad = validated_data.get('idactividad', instance.idactividad)
        instance.idlabor = validated_data.get('idlabor', instance.idlabor)
        instance.idconsumidor = validated_data.get('idconsumidor', instance.idconsumidor)
        instance.cantidad = validated_data.get('cantidad', instance.cantidad)
        instance.save()
        return instance


# ------------------------------------------------------------------------------------
from rest_framework import serializers
from .models import ImportarAsistencia

class AsistenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImportarAsistencia
        fields = '__all__'

#---------------------------------------------------
from rest_framework import serializers
from .models import ImportarAsistencia, ImportarAsistenciaDetalle
from datetime import datetime

class ImportarAsistenciaSerializer(serializers.ModelSerializer):
    detalle = serializers.SerializerMethodField()

    class Meta:
        model = ImportarAsistencia
        fields = ['id', 'idempresa', 'tipo_envio', 'idresponsable', 'idplanilla', 'idemisor', 'idturno', 'fecha', 'hora', 'idsucursal', 'idespecie', 'tipo_empleado', 'detalle']

    def get_detalle(self, obj):
        detalle_queryset = obj.detalle.all()
        return AsistenciaDetalleSerializer(detalle_queryset, many=True).data

    def create(self, validated_data):
        # Obtener la fecha actual en formato YYYYMMdd
        fecha_actual = datetime.now().strftime('%Y%m%d')
        hora_actual = datetime.now().strftime('%H:%M:%S')
        # Asignar la fecha actual al campo 'fecha' en los datos validados
        validated_data['fecha'] = fecha_actual
        
        # Crear y devolver la instancia del modelo ImportarAsistencia
        return ImportarAsistencia.objects.create(**validated_data)


class AsistenciaDetalleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImportarAsistenciaDetalle
        fields = ['item', 'idcodigogeneral', 'idactividad', 'idlabor', 'idconsumidor', 'cantidad', 'tipo_empleado', 'importar_asistencia']


#--------------------------------------------------------------------------------
from .models import Registro

class RegistroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registro
        fields = ['id', 'FechaAbierto', 'HoraAbierto', 'estado', 'FechaCerrado', 'HoraCerrado']
        

# serializers.py
from rest_framework import serializers

class TipoUsuarioSerializer(serializers.Serializer):
    tipo_usuarioapp = serializers.CharField()

#---------------------------------------------------
class DetalleImportacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImportarAsistenciaDetalle
        fields = ['item', 'idcodigogeneral', 'idactividad', 'idlabor', 'idconsumidor', 'cantidad']


#---------------------------------------------------
from rest_framework import serializers
from .models import EnviosNisira
from django.utils import timezone
from .models import EnviosNisira

class EnviosNisiraSerializer(serializers.ModelSerializer):
    FechaEnviado = serializers.DateField(format='%Y%m%d', read_only=True)
    HoraEnvio = serializers.TimeField(format='%H:%M:%S', read_only=True)
    FechaNisira = serializers.DateField(format='%Y%m%d', input_formats=['%Y%m%d'])

    def create(self, validated_data):
        validated_data['FechaEnviado'] = timezone.now().strftime('%Y%m%d')
        return super().create(validated_data)

    def validate(self, data):
        if 'IdEnvio' not in data or data['IdEnvio'] is None:
            raise serializers.ValidationError("El campo IdEnvio es obligatorio.")
        return data

    class Meta:
        model = EnviosNisira
        fields = '__all__'

#------------------------------------------------
# serializers.py
from rest_framework import serializers
from .models import CustomUser

class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('apel_nomb', 'imagen_usuario', 'gmail')


#EXTERNOS----------------------------------------------------
from rest_framework import serializers
from .models import Externos

class ExternosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Externos
        fields = ['dni', 'apellido_paterno', 'apellido_materno', 'nombres', 'nombre_apellido']

    def create(self, validated_data):
        nombre_apellido = f"{validated_data['nombres']} {validated_data['apellido_paterno']} {validated_data['apellido_materno']}"
        validated_data['nombre_apellido'] = nombre_apellido
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        instance.nombres = validated_data.get('nombres', instance.nombres)
        instance.apellido_paterno = validated_data.get('apellido_paterno', instance.apellido_paterno)
        instance.apellido_materno = validated_data.get('apellido_materno', instance.apellido_materno)
        instance.nombre_apellido = f"{instance.nombres} {instance.apellido_paterno} {instance.apellido_materno}"
        instance.save()
        return instance
