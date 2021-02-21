from django.urls import path, include

from rest_framework.routers import DefaultRouter, Route

from protein_search.views import ProteinSearchJobViewSet


router = DefaultRouter()
router.register('protein-search', ProteinSearchJobViewSet, basename="protein_search")


urlpatterns = [
    path('', include(router.urls)),
]
