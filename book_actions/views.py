from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from book.models import Book
class BookToggleFavoriteView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request,book_id, *args, **kwargs):
        book = Book.objects.get(pk=book_id)
        if