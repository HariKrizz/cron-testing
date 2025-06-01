from datetime import timedelta, timezone
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Books, StudentBooks, BooksStatus
from students.models import Student
from . serializers import BookCreateSerializer

# Create your views here.

class CreateBooksView(APIView):
    """
    View to create a new book.
    """
    def post(self, request):
        serializer = BookCreateSerializer(data=request.data)
        print(request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)  


class UpdateBooksView(APIView):
    def patch(self,request):
        """
        Update an existing book.
        """
        book = Books.objects.get(pk=request.data.get('id'))
        if not book:
            return Response({"error": "Book not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.get_serializer(book, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        book.status = request.data.get('status', book.status)
        book = serializer.save()
        return Response(BookCreateSerializer(book).data, status=status.HTTP_200_OK)
    

class DeleteBooksView(APIView):
    def delete(self, request, id):
        """
        Delete a book.
        """
        try:
            book = Books.objects.get(pk=id)
            book.staus = 5
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Books.DoesNotExist:
            return Response({"error": "Book not found"}, status=status.HTTP_404_NOT_FOUND)
        

class BookDetailView(APIView):
    def get(self, request):
        """
        Retrieve a book's details.
        """
        try:
            id = request.query_params.get('id')
            book = Books.objects.get(pk=id, status__in=[1, 2, 3, 4])
            serializer = BookCreateSerializer(book)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Books.DoesNotExist:
            return Response({"error": "Book not found"}, status=status.HTTP_404_NOT_FOUND)
        

class ListBooksView(APIView):
    def get(self, request):
        """
        List all books.
        """
        books = Books.objects.filter(status__in=[1, 2, 3, 4]).all()
        serializer = BookCreateSerializer(books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class AssignBookView(APIView):
    def post(self, request):
        """
        Assign a book to a student.
        """
        try:
            if not request.data.get('book_id'):
                return Response({"error": "Book ID is required"}, status=status.HTTP_400_BAD_REQUEST)
            book = Books.objects.get(id=request.data.get('book_id'), status=1)

            # Assuming we have a student ID in the request data
            student_id = request.data.get('student_id')
            if not student_id:
                return Response({"error": "Student ID is required"}, status=status.HTTP_400_BAD_REQUEST)
            
            student = Student.objects.get(pk=student_id)
            if not student:
                return Response({"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND)
            
            # Check if the book is already assigned to any student
            if StudentBooks.objects.filter(book=book, status=BooksStatus.ASSIGNED).exists():
                return Response({"error": f"Book : {book.title} is already assigned to a student"}, 
                                                            status=status.HTTP_400_BAD_REQUEST)

            student_books = StudentBooks.objects.create(
                book=book,
                student_id=student_id
            )
            student_books.return_date = student_books.assign_date + timedelta(days=7)
            student_books.save()
        
            return Response(
                {"message": f"Book: {book.title} assigned to {student.first_name} successfully."}, 
                                                                        status=status.HTTP_200_OK)
        except Books.DoesNotExist:
            return Response({"error": "Book not found"}, status=status.HTTP_404_NOT_FOUND)