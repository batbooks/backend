from django.test import SimpleTestCase
from django.urls import reverse, resolve
from book import views

class TestBookUrls(SimpleTestCase):
    def test_book_list_url(self):
        url = reverse('book:book-list')
        self.assertEqual(resolve(url).func.view_class, views.BookListAPIView)

    def test_book_detail_url(self):
        url = reverse('book:book-detail', args=[1])
        self.assertEqual(resolve(url).func.view_class, views.BookDetailAPIView)

    def test_book_create_url(self):
        url = reverse('book:book-create')
        self.assertEqual(resolve(url).func.view_class, views.BookCreateAPIView)

    def test_chapter_detail_url(self):
        url = reverse('book:Chapter-list', args=[1])
        self.assertEqual(resolve(url).func.view_class, views.ChapterDetailUpdateDeleteAPIView)

    def test_chapter_create_url(self):
        url = reverse('book:Chapter-create')
        self.assertEqual(resolve(url).func.view_class, views.ChapterCreateAPIView)

    def test_book_search_url(self):
        url = reverse('book:book-search', args=["test-book"])
        self.assertEqual(resolve(url).func.view_class, views.BookSearchAPIView)

    def test_user_book_url(self):
        url = reverse('book:user-detail', args=[1])
        self.assertEqual(resolve(url).func.view_class, views.UserBookAPIView)

    def test_my_book_url(self):
        url = reverse('book:my-detail')
        self.assertEqual(resolve(url).func.view_class, views.MyBookAPIView)

    def test_upload_pdf_url(self):
        url = reverse('book:upload_pdf')
        self.assertEqual(resolve(url).func.view_class, views.PDFUploadAPIView)

    def test_user_book_progress_list_url(self):
        url = reverse('book:user-book-progress-list')
        self.assertEqual(resolve(url).func.view_class, views.UserBookProgressListCreateView)

    def test_user_book_progress_detail_url(self):
        url = reverse('book:user-book-progress-detail', args=[1])
        self.assertEqual(resolve(url).func.view_class, views.UserBookProgressDetailView)
