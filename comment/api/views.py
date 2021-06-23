from .pagination import CommentPagination
from comment.models import Comment
from .serializers import CommentSerializer,CommentCreateSerializer
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated

class CommentListAPIView(ListAPIView):
    serializer_class = CommentSerializer
    pagination_class = CommentPagination

    def get_queryset(self):
        queryset = Comment.objects.all()
        query = self.request.GET.get("q")
        
        if query:
            query = queryset.filter(product = query)
        return query

class CommentCreateAPIView(CreateAPIView):
    serializer_class = CommentCreateSerializer
    queryset =Comment.objects.all()

    #Satıl almışsa permissionu eklenecek
    permission_classes =[IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
