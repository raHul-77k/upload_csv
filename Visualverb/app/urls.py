from django.urls import path
from .views import upload_csv

urlpatterns = [
    path('upload-csv/', upload_csv, name='upload_csv'),
    # path('transactions/', view_transactions, name='view_transactions'),
]