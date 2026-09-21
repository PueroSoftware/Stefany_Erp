from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsFabril(BasePermission):
    """Solo usuarios con tipo='fabril' y autenticados. CRUD completo."""

    def has_permission(self, request, view):
        u = request.user
        return bool(u and u.is_authenticated and getattr(u, "tipo", None) == "fabril")


class IsFabrilOrReadOnly(BasePermission):
    """GET/HEAD/OPTIONS para cualquiera (catálogo público); escritura solo fabril."""

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        u = request.user
        return bool(u and u.is_authenticated and getattr(u, "tipo", None) == "fabril")


class IsFabrilOrClienteWrite(BasePermission):
    """GET y POST para cualquier autenticado (cliente lee y escribe);
    PUT/DELETE/PATCH solo fabril."""

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS or request.method == "POST":
            return bool(request.user and request.user.is_authenticated)
        u = request.user
        return bool(u and u.is_authenticated and getattr(u, "tipo", None) == "fabril")


class IsOwnerOrFabril(BasePermission):
    """Cliente solo ve/modifica SUS datos; fabril ve todo."""

    def has_permission(self, request, view):
        # Solo usuarios autenticados entran; el detalle lo decide has_object_permission
        return bool(request.user and request.user.is_authenticated)

    def _owner_id(self, obj):
        # Resuelve el dueño según la estructura de cada modelo de ventas
        if getattr(obj, "id_usuario_id", None):
            return obj.id_usuario_id
        if getattr(obj, "id_pedido", None) is not None:
            return obj.id_pedido.id_usuario_id
        if getattr(obj, "id_venta", None) is not None:
            return obj.id_venta.id_pedido.id_usuario_id
        return None

    def has_object_permission(self, request, view, obj):
        if getattr(request.user, "tipo", None) == "fabril":
            return True
        return self._owner_id(obj) == request.user.id_usuario
