# models.py
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone

def validate_dni_length(value):
    if len(value) not in [8, 12]:
        raise ValidationError(
            ('El DNI debe tener 8 o 12 dígitos.'),
            code='invalid_dni_length'
        )
class CustomUserManager(BaseUserManager):
    def _create_user(self, dni, apel_nomb, password=None, **extra_fields):
        if not dni:
            raise ValueError('El campo DNI es obligatorio.')

        user = self.model(
            dni=dni,
            apel_nomb=apel_nomb,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, dni, apel_nomb, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(dni, apel_nomb, password, **extra_fields)

    def create_superuser(self, dni, apel_nomb, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(dni, apel_nomb, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    class TipoUsuario(models.TextChoices):
        ADMINISTRADOR = 'Administrador', 'Administrador'
        EMPLEADO_PROCESO = 'Proceso', 'Proceso'
        EMPLEADO_SUPERVISOR = 'Supervisor', 'Supervisor'

    # Aumenta el valor de max_length acomodando la longitud del valor más largo en choices
    tipo_usuarioapp = models.CharField(
        max_length=25,  # o el valor necesario para acomodar "EmpleadoProcesoMerloza"
        choices=TipoUsuario.choices,
        default=TipoUsuario.ADMINISTRADOR
    )

    id = models.BigAutoField(primary_key=True)
    dni = models.CharField(
        unique=True,
        max_length=12,
    )
    apel_nomb = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    imagen_usuario = models.ImageField(upload_to='usuarios', blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    gmail = models.EmailField(blank=True, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'dni'
    REQUIRED_FIELDS = ['apel_nomb', 'tipo_usuarioapp']

    def __str__(self):
        return f'{self.apel_nomb} ({self.dni})'
    

from django.db import models

class Empresa(models.Model):
    idempresa = models.CharField(max_length=3, primary_key=True)
    nombre = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        if not self.idempresa:  # Si no se proporciona un idempresa
            # Obtener el último idempresa en la base de datos
            ultimo_idempresa = Empresa.objects.order_by('-idempresa').first()

            # Si no hay registros en la base de datos, establecer el primer idempresa como "001"
            if not ultimo_idempresa:
                self.idempresa = "001"
            else:
                # Generar el siguiente idempresa
                ultimo_numero = int(ultimo_idempresa.idempresa)
                siguiente_numero = ultimo_numero + 1
                siguiente_idempresa = str(siguiente_numero).zfill(3)  # Rellenar con ceros a la izquierda si es necesario

                # Verificar si el siguiente idempresa ya existe
                while Empresa.objects.filter(idempresa=siguiente_idempresa).exists():
                    siguiente_numero += 1
                    siguiente_idempresa = str(siguiente_numero).zfill(3)

                self.idempresa = siguiente_idempresa

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.idempresa} - {self.nombre}"


from django.db import models

class TipoEnvio(models.Model):
    tipo_envio = models.CharField(max_length=1, blank=True)  # Campo no requerido
    nombre = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        # Convertir la primera letra del nombre a mayúscula antes de guardar
        self.nombre = self.nombre.capitalize()
        self.tipo_envio = self.nombre[0].upper() if self.nombre else ''  # Asignar la primera letra del nombre o una cadena vacía si no hay nombre
        super(TipoEnvio, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.tipo_envio} - {self.nombre}"

class Responsable(models.Model):
    idresponsable = models.CharField(max_length=6, primary_key=True)
    nombre_apellido = models.CharField(max_length=250)

    def save(self, *args, **kwargs):
        if not self.idresponsable: 
            ultimo_idresponsable = Responsable.objects.order_by('-idresponsable').first()

            if not ultimo_idresponsable:
                self.idresponsable = "000001"
            else:
                ultimo_numero = int(ultimo_idresponsable.idresponsable)
                siguiente_numero = ultimo_numero + 1
                siguiente_idresponsable = str(siguiente_numero).zfill(6)
                while Responsable.objects.filter(idresponsable=siguiente_idresponsable).exists():
                    siguiente_numero += 1
                    siguiente_idresponsable = str(siguiente_numero).zfill(6)

                self.idresponsable = siguiente_idresponsable

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.idresponsable} - {self.nombre_apellido}"


class Planilla(models.Model):
    idplanilla = models.CharField(max_length=3, unique=True)
    nombre = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.idplanilla} - {self.nombre}"



class Emisor(models.Model):
    idemisor = models.CharField(max_length=3, primary_key=True)
    nombre = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        if not self.idemisor:  # Si no se proporciona un idempresa
            # Obtener el último idempresa en la base de datos
            ultimo_idemisor = Emisor.objects.order_by('-idemisor').first()

            # Si no hay registros en la base de datos, establecer el primer idempresa como "001"
            if not ultimo_idemisor:
                self.idemisor = "001"
            else:
                # Generar el siguiente idempresa
                ultimo_numero = int(ultimo_idemisor.idemisor)
                siguiente_numero = ultimo_numero + 1
                siguiente_idemisor = str(siguiente_numero).zfill(3)  # Rellenar con ceros a la izquierda si es necesario

                # Verificar si el siguiente idempresa ya existe
                while Emisor.objects.filter(idemisor=siguiente_idemisor).exists():
                    siguiente_numero += 1
                    siguiente_idemisor = str(siguiente_numero).zfill(3)

                self.idemisor = siguiente_idemisor

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.idemisor} - {self.nombre}"
    

class Especie(models.Model):
    idespecie = models.CharField(max_length=3, primary_key=True)
    nombre = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        if not self.idespecie:  # Si no se proporciona un idempresa
            # Obtener el último idempresa en la base de datos
            ultimo_idespecie = Emisor.objects.order_by('-idespecie').first()

            # Si no hay registros en la base de datos, establecer el primer idempresa como "001"
            if not ultimo_idespecie:
                self.idespecie = "001"
            else:
                # Generar el siguiente idempresa
                ultimo_numero = int(ultimo_idespecie.idespecie)
                siguiente_numero = ultimo_numero + 1
                siguiente_idespecie = str(siguiente_numero).zfill(3)  # Rellenar con ceros a la izquierda si es necesario

                # Verificar si el siguiente idempresa ya existe
                while Especie.objects.filter(idespecie=siguiente_idespecie).exists():
                    siguiente_numero += 1
                    siguiente_idespecie = str(siguiente_numero).zfill(3)

                self.idespecie = siguiente_idespecie

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.idespecie} - {self.nombre}"
    


class Turno(models.Model):
    idturno = models.CharField(max_length=2, primary_key=True)
    nombre = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        if not self.idturno:  # Si no se proporciona un idempresa
            # Obtener el último idempresa en la base de datos
            ultimo_idturno = Turno.objects.order_by('-idturno').first()

            # Si no hay registros en la base de datos, establecer el primer idempresa como "001"
            if not ultimo_idturno:
                self.idturno = "01"
            else:
                # Generar el siguiente idempresa
                ultimo_numero = int(ultimo_idturno.idturno)
                siguiente_numero = ultimo_numero + 1
                siguiente_idturno = str(siguiente_numero).zfill(2)  # Rellenar con ceros a la izquierda si es necesario

                # Verificar si el siguiente idempresa ya existe
                while Turno.objects.filter(idturno=siguiente_idturno).exists():
                    siguiente_numero += 1
                    siguiente_idturno = str(siguiente_numero).zfill(2)

                self.idturno = siguiente_idturno

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.idturno} - {self.nombre}"
    

class Consumidor(models.Model):
    idconsumidor = models.CharField(max_length=6, primary_key=True)
    nombre_apellido = models.CharField(max_length=250)

    def save(self, *args, **kwargs):
        if not self.idconsumidor: 
            ultimo_idconsumidor = Consumidor.objects.order_by('-idconsumidor').first()

            if not ultimo_idconsumidor:
                self.idconsumidor = "000001"
            else:
                ultimo_numero = int(ultimo_idconsumidor.idconsumidor)
                siguiente_numero = ultimo_numero + 1
                siguiente_idconsumidor = str(siguiente_numero).zfill(6)
                while Consumidor.objects.filter(idconsumidor=siguiente_idconsumidor).exists():
                    siguiente_numero += 1
                    siguiente_idconsumidor = str(siguiente_numero).zfill(6)

                self.idconsumidor = siguiente_idconsumidor

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.idconsumidor} - {self.nombre_apellido}"






# ------------------------------------------------------------------------------------

class ImportarAsistencia(models.Model):
    idempresa = models.CharField(max_length=6, null=True)
    tipo_envio = models.CharField(max_length=1, null=True)
    idresponsable = models.CharField(max_length=6, null=True)
    idplanilla = models.CharField(max_length=3, null=True)
    idemisor = models.CharField(max_length=3, null=True)
    idturno = models.CharField(max_length=2, null=True)
    fecha = models.CharField(max_length=8, blank=True, null=True)
    idsucursal = models.CharField(max_length=3, null=True)
    hora = models.TimeField(blank=True, null=True)
    idespecie = models.CharField(max_length=3, null=True)
    tipo_empleado = models.CharField(max_length=10, null=True)


    class Meta:
        verbose_name = 'Importar Asistencia'
        verbose_name_plural = 'Importar Asistencias'

    def __str__(self):
        return self.idempresa + ' - ' + self.fecha
    

class ImportarAsistenciaDetalle(models.Model):
    importar_asistencia = models.ForeignKey('ImportarAsistencia', related_name='detalle', on_delete=models.CASCADE)
    item = models.AutoField(primary_key=True)
    idcodigogeneral = models.CharField(max_length=8, null=True)
    idactividad = models.CharField(max_length=3, null=True)
    idlabor = models.CharField(max_length=6, null=True)
    idconsumidor = models.CharField(max_length=6, null=True)
    cantidad = models.CharField(max_length=10, null=True)
    tipo_empleado = models.CharField(max_length=10, null=True)



    class Meta:
        unique_together = (('importar_asistencia', 'item'),)

    @staticmethod
    def generar_item(importar_asistencia):
        # Obtener la cantidad de labores para el trabajador asociado
        cantidad_labores = ImportarAsistenciaDetalle.objects.filter(importar_asistencia=importar_asistencia).count()
        
        # Generar un identificador único para la labor
        item = cantidad_labores + 1
        
        return item



#-------------------------------------------------------------------------------------

from django.db import models

class Registro(models.Model):
    ESTADO_CHOICES = [
        ('Abierto', 'Abierto'),
        ('Cerrado', 'Cerrado'),
    ]

    FechaAbierto = models.CharField(max_length=8)  
    HoraAbierto = models.TimeField()
    estado = models.CharField(max_length=7, choices=ESTADO_CHOICES)
    FechaCerrado = models.CharField(max_length=8, blank=True, null=True)  # YYYYMMdd
    HoraCerrado = models.TimeField(blank=True, null=True)

    def __str__(self):
        return f'{self.estado} - {self.FechaAbierto} - {self.HoraAbierto}'


#-------------------------------------------------------------------------------------from django.db import models
from django.db import models

class EnviosNisira(models.Model):
    IdEnvio = models.CharField(max_length=50, unique=True)
    FechaEnviado = models.DateField(auto_now_add=True)
    HoraEnvio = models.TimeField(auto_now_add=True)
    FechaNisira = models.DateField()
    Encabezado = models.CharField(max_length=100)
    KilosEnviados = models.CharField(max_length=50)  # Ajusta la longitud máxima según tus necesidades

    def __str__(self):
        return self.Encabezado



#EXTERNOS---------------------------------------------------------------------------
class Externos(models.Model):
    dni = models.CharField(max_length=8)
    apellido_paterno = models.CharField(max_length=255)
    apellido_materno = models.CharField(max_length=255)
    nombres = models.CharField(max_length=255)
    nombre_apellido = models.CharField(max_length=255, null=True, blank=True)
