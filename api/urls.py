# api/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.conf.urls.static import static
from django.conf import settings
from .views import *
from . import views

router = DefaultRouter()
router.register(r'usuarios', CustomUserViewSet, basename='usuario')



urlpatterns = [
    path('', include(router.urls)),

    path('default-image/', default_image_view, name='default_image_view'),

    path('actualizar-usuario/<str:dni>/', UserUpdateAPIView.as_view(), name='actualizar_usuario'),

    path('token/', ObtainTokenView.as_view(), name='obtain_token'),
    path('current-user/', getCurrentUser, name='current_user'),
    path('usuarios/eliminar/<str:dni>/', views.eliminar_usuario, name='eliminar_usuario'),
    path('usuarios/actualizar/<str:dni>/', actualizar_usuario, name='actualizar_usuario'),
    path('usuarios/dni/<str:dni>/', UserByDniAPIView.as_view(), name='user-by-dni'),
    path('empresas/', EmpresaListCreateAPIView.as_view(), name='empresa-list-create'),
    path('tipoUsuarios/', obtener_tipos_usuarios, name='obtener_tipos_usuarios'),
    path('usuarios/', CustomUserViewSet.as_view({'post': 'create'}), name='create_user'),
    path('obtener/usuarios/', UserListAPIView.as_view(), name='user-list-api'),

    path('tiposenvio/', TipoEnvioListCreate.as_view(), name='tiposenvio-list-create'),
    path('responsables/', views.responsable_list),
    path('responsables/<str:pk>/', views.responsable_detail),
    path('planillas/', PlanillaAPIView.as_view(), name='planilla-list'),
    path('planillas/<str:id>/', PlanillaAPIView.as_view(), name='planilla-detail'),
    path('emisor/', EmisorListCreateAPIView.as_view(), name='emisor-list-create'),
    path('turno/', TurnoListCreateAPIView.as_view(), name='turno-list-create'),
    path('consumidor/', ConsumidorListCreateAPIView.as_view(), name='consumidor-list-create'),
    path('estado/', DiaAPIView.as_view(), name='abrir-dia'),
    path('registros/', views.registros_lista, name='todos-los-registros'),

    path('importar-asistencia/', importar_asistencia_Post, name='importar_asistencia_list'),
    path('importar-asistencia-detalle/', views.importar_asistencia_list, name='importar_asistencia_list'),
    path('asistencia/<str:idcodigogeneral>/<str:idlabor>/', MerluzasistenciaUpdateByCodigoGeneralView.as_view(), name='update_asistencia'),
    path('pota/importarasistencia/', POTAAsistenciaUpdateByCodigoGeneralView.as_view(), name='importar_asistencia_list'),
    path('pota/importarasistencia/<str:idcodigogeneral>/', POTAAsistenciaUpdateByCodigoGeneralView.as_view()),
    path('ingresos-dia-actual/', ingresos_del_dia_actual, name='importaciones_activas'),
    path('ingresos-dia-actual/<str:idcodigogeneral>/', views.ingresos_del_dia_actual, name='ingresos-dia-actual-detalle'),

    path('importaciones-fechas/<str:fecha_abierto>/', importaciones_por_fecha, name='importaciones_por_fecha'),
    
    path('importaciones_clasificadas/<str:fecha_abierto>/', views.importaciones_clasificadas_por_fecha_sin_encabezado, name='importaciones_por_fecha'),

    path('importaciones_clasificadas/<str:fecha_abierto>/<str:encabezado>/', views.importaciones_clasificadas_por_fecha, name='importaciones_clasificadas'),
    
    path('ultimo-registro/', UltimoRegistroView.as_view(), name='ultimo_registro'),
    
    path('ActualizarImportacion/<str:fecha_abierto>/<str:idcodigogeneral>/<str:idlabor>/', views.actualizar_importacion),
    path('EliminarDetalleImportacion/<str:fecha_abierto>/<str:idcodigogeneral>/<str:idlabor>/', views.eliminar_detalle_importacion),


    path('envios_nisira/create/', views.create_envio_nisira),
    path('envios_nisira/', views.envios_nisira_list, name='envios_nisira_list'),
    path('envios_nisira/<str:fecha_nisira>/', views.envios_nisira_list, name='envios_nisira_list_fecha'),

    path('importaciones/', views.importaciones_todas, name='importaciones_todas'),
    path('importaciones/<str:idcodigogeneral>/', views.importaciones_todas, name='importaciones_todas'),
    path('importaciones/<str:idcodigogeneral>/<str:fecha_abierto>/', views.importaciones_todas, name='importaciones_todas'),



#EXTERNOS-----------------------------------------------------
    path('externos/', create_externo, name='create_externo'),
    path('externos/list/', views.get_externo, name='get_all_externos'),
    path('externos/<str:dni>/', get_externo, name='get_externo'),
    path('externos/update/<str:dni>/', update_externo, name='update_externo'),
    path('externos/delete/<str:dni>/', delete_externo, name='delete_externo'),

     ]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)