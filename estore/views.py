from rest_framework.views import Response, status, APIView
from .models import Order, Product, Reviews
from .serializers import OrderSerializer, ProductSerializer, ProductDetailSerializer, ReviewListAPI
from rest_framework.permissions import IsAuthenticated
from django.db.models import Avg

class ProductListAPIView(APIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        products = Product.objects.all()
        data = self.serializer_class(products, many=True).data
        content = {"Categories": data}
        return Response(content, status=status.HTTP_200_OK)


class ProductDetailAPIView(APIView):
    serializer_class = ProductDetailSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            product = Product.objects.all().get(id=kwargs["id"])
        except:
            return Response({'data': 'Page not found'}, status=status.HTTP_404_NOT_FOUND)

        # Calculate average rating
        average_rating = Reviews.objects.filter(product=product).aggregate(Avg('rating'))['rating__avg']

        serializer = self.serializer_class(product)
        reviews = product.product_reviews.all()
        review_api = ReviewListAPI(reviews, many=True)
        content = {"Product Info": serializer.data,
                   "Reviews": review_api.data,
                   "Average Rating": average_rating}

        return Response(content, status=status.HTTP_200_OK)


class ReviewCreateAPIView(APIView):
    serializer_class = ReviewListAPI
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        request.data['product'] = kwargs['id']
        request.data['reviewer'] = request.user.id
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"data": serializer.data, "message": "Review has been submitted successfully!"},
                            status=status.HTTP_201_CREATED)
        return Response({"error": serializer.errors, "message": "There is an error"},
                        status=status.HTTP_400_BAD_REQUEST)


class OrderCreateAPIView(APIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            product = Product.objects.all().get(id=kwargs["id"])
        except:
            return Response({'data': 'Page not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, product=product)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
