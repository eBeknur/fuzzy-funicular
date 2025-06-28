from django.urls import path
from .views import LinksView , UserLinksView , LinkDetailView
urlpatterns = [
    path('', LinksView.as_view(), name='upload-link'),
    path('my-links/',UserLinksView.as_view() , name='user-links'),
    path('link/<str:url>/', LinkDetailView.as_view(), name='link-detail'),
]
