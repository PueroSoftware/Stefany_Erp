from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from core.permissions import IsFabril, IsFabrilOrReadOnly
from .models import ObjectStorage, Usuario
from .serializers import ObjectStorageSerializer, UsuarioSerializer, RegisterSerializer


class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [IsFabril]


# A2: endpoint "Mi perfil" - el usuario logueado gestiona sus propios datos
class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Devuelve los datos del usuario autenticado (request.user)
        serializer = UsuarioSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        # Permite actualizar sus propios datos (nombre, dirección, etc.)
        serializer = UsuarioSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class RegisterView(APIView):
    # Público: sin token para poder registrarse
    permission_classes = []

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        usuario = serializer.save()
        refresh = RefreshToken.for_user(usuario)
        return Response(
            {
                "message": "Usuario creado",
                "token": str(refresh.access_token),
                "usuario": serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )


class ObjectStorageViewSet(viewsets.ReadOnlyModelViewSet):
    """Catálogo público de imágenes R2.
    - GET (sin token): cualquier visitante lista las imágenes del frontend.
    - Escritura (POST/PUT/DELETE): no existen (ReadOnlyModelViewSet) —
      los objetos los siembra el management command sync_r2, no la API.
    - Filtro por grupo vía query param: ?grupo=esencia
    """

    queryset = ObjectStorage.objects.filter(activo=True)
    serializer_class = ObjectStorageSerializer
    permission_classes = [IsFabrilOrReadOnly]
    filterset_fields = ["grupo"]
