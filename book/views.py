from django.shortcuts import render
import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from rest_framework.parsers import MultiPartParser, FormParser
from datetime import datetime
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
from .models import Book, Chapter
from permissions import BookIsOwnerOrReadOnly, ChapterIsOwnerOrReadOnly, IsOwnerOrReadOnly
from .serializers import BookSerializer, BookGetAllSerializer, ChapterGetSerializer, ChapterCreateSerializer, \
    BookAllGetSerializer, BookGetSerializer, User
from book_actions.models import Blocked
from paginations import CustomPagination
from rest_framework import generics
import fitz


class BookListAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = BookAllGetSerializer

    def get(self, request):
        user = request.user

        if user.is_authenticated:
            try:
                blocked_books = Blocked.objects.get(user=user).book.all()
            except Blocked.DoesNotExist:
                blocked_books = Book.objects.none()

            books = Book.objects.select_related('Author').exclude(
                id__in=blocked_books.values_list('id', flat=True)
            )
        else:
            books = Book.objects.select_related('Author').all()

        serializer = BookAllGetSerializer(books, many=True)
        return Response(serializer.data)


class BookCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BookSerializer

    def post(self, request):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(Author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookDetailAPIView(APIView):
    permission_classes = [BookIsOwnerOrReadOnly]
    serializer_class = BookGetAllSerializer

    def get(self, request, pk):
        try:
            book = Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            return Response(
                {"error": "کتاب مورد نظر پیدا نشد."},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = BookGetAllSerializer(book)
        return Response(serializer.data)

    def put(self, request, pk):
        try:
            book = Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            return Response(
                {"error": "کتاب مورد نظر پیدا نشد."},
                status=status.HTTP_404_NOT_FOUND
            )
        self.check_object_permissions(request, book)
        serializer = BookSerializer(book, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChapterDetailUpdateDeleteAPIView(APIView):
    permission_classes = [ChapterIsOwnerOrReadOnly]
    serializer_class = ChapterGetSerializer

    def get(self, request, id):
        try:
            chapter = Chapter.objects.get(pk=id)
        except Chapter.DoesNotExist:
            return Response(
                {"error": "چپتر مورد نظر پیدا نشد."},
                status=status.HTTP_404_NOT_FOUND
            )
        if chapter.is_approved:
            ser_data = ChapterGetSerializer(chapter, context={'request': request})
            return Response(ser_data.data, status=status.HTTP_200_OK)
        return Response({'error': 'چپتر پیدا نشد'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, id):
        try:
            chapter = Chapter.objects.get(pk=id)
        except Chapter.DoesNotExist:
            return Response(
                {"error": "چپتر مورد نظر پیدا نشد."},
                status=status.HTTP_404_NOT_FOUND
            )
        self.check_object_permissions(request, chapter)
        serializer = ChapterCreateSerializer(data=request.data, instance=chapter, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        try:
            chapter = Chapter.objects.get(pk=id)
        except Chapter.DoesNotExist:
            return Response(
                {"error": "چپتر مورد نظر پیدا نشد."},
                status=status.HTTP_404_NOT_FOUND
            )
        self.check_object_permissions(request, chapter)
        chapter.delete()
        return Response({'messege': 'چپتر با موفقیت پاک شد'}, status=status.HTTP_204_NO_CONTENT)


class ChapterCreateAPIView(APIView):
    permission_classes = [BookIsOwnerOrReadOnly]
    serializer_class = ChapterCreateSerializer

    def post(self, request):

        try:
            book = Book.objects.get(pk=request.data['book'])
        except Book.DoesNotExist:
            return Response(
                {"error": "کتاب مورد نظر پیدا نشد."},
                status=status.HTTP_404_NOT_FOUND
            )

        self.check_object_permissions(request, book)
        ser_data = ChapterCreateSerializer(data=request.data)
        if ser_data.is_valid():
            ser_data.save()
            return Response(ser_data.data, status=status.HTTP_201_CREATED)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


class BookSearchAPIView(APIView):
    serializer_class = BookGetSerializer

    def get(self, request, book_name):
        book_name = book_name.strip()
        if len(book_name) < 3:
            return Response({"error": 'اسم کتاب باید حداقل سه حرف باشد.'}, status=status.HTTP_400_BAD_REQUEST)
        books = Book.objects.filter(name__icontains=book_name)
        paginator = CustomPagination()
        page = paginator.paginate_queryset(books, request)
        data = BookGetSerializer(page, context={"hide_field": ['email']}, many=True).data
        return paginator.get_paginated_response(data)


##  with generic

class UserBookAPIView(generics.ListAPIView):
    serializer_class = BookSerializer

    def get_queryset(self):
        user = get_object_or_404(User, id=self.kwargs.get('id'))
        return user.books.all().order_by('-id')


class MyBookAPIView(generics.ListAPIView):
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return user.books.all().order_by('-id')


class PDFUploadAPIView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [BookIsOwnerOrReadOnly]

    def post(self, request, *args, **kwargs):
        pdf_file = request.FILES.get('pdf')
        book_id = request.data.get('book')
        title = request.data.get('title', None)

        if not pdf_file or not book_id:
            return Response({'error': 'فایل pdf  یا کتاب مورد نظر موجود نیست.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            book = Book.objects.get(pk=book_id)
            self.check_object_permissions(request, book)
        except Book.DoesNotExist:
            return Response({'error': 'کتاب پیدا نشد'}, status=status.HTTP_404_NOT_FOUND)

        doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
        images_to_save = []
        content = ""

        for page_num, page in enumerate(doc, start=1):
            page_dict = page.get_text("dict")
            page_content = ""

            for block in page_dict["blocks"]:
                if block["type"] == 0:
                    for line in block["lines"]:
                        for span in line["spans"]:
                            page_content += span["text"]
                    page_content += "\n"

                elif block["type"] == 1:
                    try:
                        images = page.get_images(full=True)
                        for img_index, img in enumerate(images):
                            xref = img[0]
                            base_image = doc.extract_image(xref)
                            image_bytes = base_image["image"]
                            ext = base_image["ext"]

                            image_name = f"chapter_{datetime.now().timestamp()}_page{page_num}_img{img_index}.{ext}"
                            image_rel_path = f"chapter_images/{image_name}"
                            image_abs_path = os.path.join(settings.MEDIA_ROOT, image_rel_path)
                            os.makedirs(os.path.dirname(image_abs_path), exist_ok=True)

                            with open(image_abs_path, "wb") as f:
                                f.write(image_bytes)

                            image_url = request.build_absolute_uri(settings.MEDIA_URL + image_rel_path)

                            page_content += f'<img src="{image_url}" alt="Image on page {page_num}">\n'

                            images_to_save.append({
                                "image": image_rel_path,
                                "page_number": page_num
                            })
                            break

                    except Exception as e:
                        print(f"در هنگام استخراج عکس به مشکل برخورد کردیم.: {e}")
                        continue

            content += page_content + "\n"

        title = pdf_file.name.rsplit('.', 1)[0] if not title else title
        chapter = Chapter.objects.create(
            title=title,
            book=book,
            body=content.strip(),
            is_approved=False
        )

        return Response({
            'message': 'pdf  با موفقیت اپلود شد.',
            'chapter_id': chapter.id
        }, status=status.HTTP_201_CREATED)
