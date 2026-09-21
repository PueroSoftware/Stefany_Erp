from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from django.db import transaction
from core.permissions import IsOwnerOrFabril
from .models import (
    Pedido,
    Carrito,
    Venta,
    DetalleVenta,
    Pago,
    Envio,
    HistorialNavegacion,
)
from .serializers import (
    PedidoSerializer,
    CarritoSerializer,
    VentaSerializer,
    DetalleVentaSerializer,
    PagoSerializer,
    EnvioSerializer,
    HistorialNavegacionSerializer,
)


class PedidoViewSet(viewsets.ModelViewSet):
    # A1: cliente solo ve/modifica SUS pedidos; fabril ve todo
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer
    permission_classes = [IsOwnerOrFabril]

    def get_queryset(self):
        qs = Pedido.objects.all()
        if getattr(self.request.user, "tipo", None) != "fabril":
            qs = qs.filter(id_usuario=self.request.user)
        return qs

    def perform_create(self, serializer):
        # A1: el dueño es SIEMPRE el usuario autenticado (evita suplantación)
        serializer.save(id_usuario=self.request.user)

    # A3: al confirmar el pedido descontamos stock_disponible (una sola vez)
    def perform_update(self, serializer):
        instance = self.get_object()
        nuevo_estado = serializer.validated_data.get("estado", instance.estado)
        if nuevo_estado == "confirmado" and not instance.stock_descontado:
            with transaction.atomic():
                pedido = serializer.save()
                for item in pedido.carrito.all():
                    prod = item.id_producto
                    prod.stock_disponible -= item.cantidad
                    prod.save()
                pedido.stock_descontado = True
                pedido.save()
        else:
            serializer.save()


class CarritoViewSet(viewsets.ModelViewSet):
    queryset = Carrito.objects.all()
    serializer_class = CarritoSerializer
    permission_classes = [IsOwnerOrFabril]

    def get_queryset(self):
        qs = Carrito.objects.all()
        if getattr(self.request.user, "tipo", None) != "fabril":
            qs = qs.filter(id_pedido__id_usuario=self.request.user)
        return qs

    def perform_create(self, serializer):
        # A1: el carrito debe pertenecer a un pedido del propio usuario
        pedido = serializer.validated_data.get("id_pedido")
        if pedido.id_usuario_id != self.request.user.id_usuario:
            raise PermissionDenied("No puedes crear sobre un pedido ajeno")
        serializer.save()


class VentaViewSet(viewsets.ModelViewSet):
    queryset = Venta.objects.all()
    serializer_class = VentaSerializer
    permission_classes = [IsOwnerOrFabril]

    def get_queryset(self):
        qs = Venta.objects.all()
        if getattr(self.request.user, "tipo", None) != "fabril":
            qs = qs.filter(id_pedido__id_usuario=self.request.user)
        return qs

    def perform_create(self, serializer):
        # A1: la venta debe pertenecer a un pedido del propio usuario
        pedido = serializer.validated_data.get("id_pedido")
        if pedido.id_usuario_id != self.request.user.id_usuario:
            raise PermissionDenied("No puedes crear una venta sobre un pedido ajeno")
        # A3: descontar stock al crear la venta (si el pedido aún no lo hizo)
        with transaction.atomic():
            venta = serializer.save()
            if not venta.id_pedido.stock_descontado:
                for item in venta.id_pedido.carrito.all():
                    prod = item.id_producto
                    prod.stock_disponible -= item.cantidad
                    prod.save()
                venta.id_pedido.stock_descontado = True
                venta.id_pedido.save()


class DetalleVentaViewSet(viewsets.ModelViewSet):
    queryset = DetalleVenta.objects.all()
    serializer_class = DetalleVentaSerializer
    permission_classes = [IsOwnerOrFabril]

    def get_queryset(self):
        qs = DetalleVenta.objects.all()
        if getattr(self.request.user, "tipo", None) != "fabril":
            qs = qs.filter(id_venta__id_pedido__id_usuario=self.request.user)
        return qs

    def perform_create(self, serializer):
        venta = serializer.validated_data.get("id_venta")
        if venta.id_pedido.id_usuario_id != self.request.user.id_usuario:
            raise PermissionDenied("No puedes crear sobre una venta ajena")
        serializer.save()


class PagoViewSet(viewsets.ModelViewSet):
    queryset = Pago.objects.all()
    serializer_class = PagoSerializer
    permission_classes = [IsOwnerOrFabril]

    def get_queryset(self):
        qs = Pago.objects.all()
        if getattr(self.request.user, "tipo", None) != "fabril":
            qs = qs.filter(id_pedido__id_usuario=self.request.user)
        return qs

    def perform_create(self, serializer):
        pedido = serializer.validated_data.get("id_pedido")
        if pedido.id_usuario_id != self.request.user.id_usuario:
            raise PermissionDenied("No puedes crear sobre un pedido ajeno")
        serializer.save()


class EnvioViewSet(viewsets.ModelViewSet):
    queryset = Envio.objects.all()
    serializer_class = EnvioSerializer
    permission_classes = [IsOwnerOrFabril]

    def get_queryset(self):
        qs = Envio.objects.all()
        if getattr(self.request.user, "tipo", None) != "fabril":
            qs = qs.filter(id_pedido__id_usuario=self.request.user)
        return qs

    def perform_create(self, serializer):
        pedido = serializer.validated_data.get("id_pedido")
        if pedido.id_usuario_id != self.request.user.id_usuario:
            raise PermissionDenied("No puedes crear sobre un pedido ajeno")
        serializer.save()


class HistorialNavegacionViewSet(viewsets.ModelViewSet):
    queryset = HistorialNavegacion.objects.all()
    serializer_class = HistorialNavegacionSerializer
    permission_classes = [IsOwnerOrFabril]

    def get_queryset(self):
        qs = HistorialNavegacion.objects.all()
        if getattr(self.request.user, "tipo", None) != "fabril":
            qs = qs.filter(id_usuario=self.request.user)
        return qs

    def perform_create(self, serializer):
        serializer.save(id_usuario=self.request.user)
