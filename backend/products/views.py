from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied
from .models import Product
from .serializers import ProductSerializer


# class IsFarmer(permissions.BasePermission):
#     def has_permission(self, request, view):
#         return request.user.role == 'FARMER'
#
#
# class ProductListCreateView(generics.ListCreateAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#     permission_classes = [permissions.IsAuthenticated, IsFarmer]
#
#     def get_queryset(self):
#         # Farmers see their products; buyers see all (read-only)
#         if self.request.user.role == 'FARMER':
#             return Product.objects.filter(farmer=self.request.user)
#         return Product.objects.all()
#
#     def create(self, request, *args, **kwargs):
#         if request.user.role != 'FARMER':
#             raise PermissionDenied("Only farmers can post products")
#         return super().create(request, *args, **kwargs)
#
#
# class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#     permission_classes = [permissions.IsAuthenticated, IsFarmer]  # Updated
#
#     def perform_update(self, serializer):
#         if serializer.instance.farmer != self.request.user:
#             raise PermissionDenied("You do not own this product")
#         serializer.save()


class IsFarmerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.role == 'FARMER'


class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated, IsFarmerOrReadOnly]  # Updated

    def get_queryset(self):
        queryset = Product.objects.filter(farmer__is_active=True)  # farmers can see only their own p
        if self.request.user.role == 'FARMER':
            return queryset.filter(farmer=self.request.user)
        return queryset

    def create(self, request, *args, **kwargs):
        if request.user.role != 'FARMER':
            raise PermissionDenied("Only farmers can post products")
        return super().create(request, *args, **kwargs)


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated, IsFarmerOrReadOnly]

    def perform_update(self, serializer):
        if serializer.instance.farmer != self.request.user:
            raise PermissionDenied("You do not own this product")
        serializer.save()