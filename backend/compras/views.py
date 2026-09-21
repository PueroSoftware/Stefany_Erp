from core.permissions import IsFabril
from django.db import transaction
from inventario.models import MovimientoStock, StockMateriaPrima
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import CompraMateriaPrima, DetalleCompra, Proveedor
from .serializers import (
    CompraMateriaPrimaSerializer,
    DetalleCompraSerializer,
    ProveedorSerializer,
)


class ProveedorViewSet(viewsets.ModelViewSet):
    queryset = Proveedor.objects.all()
    serializer_class = ProveedorSerializer
    permission_classes = [IsFabril]


class CompraMateriaPrimaViewSet(viewsets.ModelViewSet):
    queryset = CompraMateriaPrima.objects.all()
    serializer_class = CompraMateriaPrimaSerializer
    permission_classes = [IsFabril]


class DetalleCompraViewSet(viewsets.ModelViewSet):
    queryset = DetalleCompra.objects.all()
    serializer_class = DetalleCompraSerializer
    permission_classes = [IsFabril]


class RegistrarCompraView(APIView):
    permission_classes = [IsFabril]

    @transaction.atomic
    def post(self, request):
        data = request.data

        compra = CompraMateriaPrima.objects.create(
            id_proveedor_id=data["id_proveedor"],
            numero_factura=data["numero_factura"],
            tipo_factura=data.get("tipo_factura", "factura"),
        )

        total = 0
        for item in data["detalles"]:
            detalle = DetalleCompra.objects.create(
                id_compra=compra,
                id_insumo_id=item["id_insumo"],
                cantidad=item["cantidad"],
                precio_unitario=item["precio_unitario"],
                lote=item.get("lote", ""),
                observaciones=item.get("observaciones", ""),
            )
            total += float(detalle.subtotal)

            stock = StockMateriaPrima.objects.get(id_insumo=item["id_insumo"])
            anterior = float(stock.cantidad_disponible)
            stock.cantidad_disponible += item["cantidad"]
            stock.save()

            MovimientoStock.objects.create(
                id_insumo_id=item["id_insumo"],
                tipo_movimiento="entrada",
                motivo="compra",
                cantidad=item["cantidad"],
                stock_anterior=anterior,
                stock_nuevo=float(stock.cantidad_disponible),
                referencia_id=compra.id_compra,
                referencia_tabla="compra_materia_prima",
            )

        compra.total = total
        compra.estado = "recibida"
        compra.save()

        return Response(
            {
                "message": "Compra registrada",
                "data": {"id_compra": compra.id_compra, "total": total},
            },
            status=status.HTTP_201_CREATED,
        )
