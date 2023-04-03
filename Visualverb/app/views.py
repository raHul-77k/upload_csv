import pandas as pd
from django.shortcuts import render, redirect
from datetime import datetime
from .models import Transaction
from .forms import CSVUploadForm

def upload_csv(request):
    Transaction.objects.all().delete()

    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Parse the uploaded CSV file using pandas
            csv_file = request.FILES['file']
            df = pd.read_csv(csv_file, encoding='iso-8859-1')

            # Select only the desired columns
            df = df[['Invoice ID', 'Product line', 'Unit price', 'Quantity', 'Tax 5%', 'Total', 'Date', 'Time']][:60]

            # Rename the columns to match the Transaction model fields
            df = df.rename(columns={
                'Invoice ID': 'invoice_id',
                'Product line': 'product_line',
                'Unit price': 'unit_price',
                'Quantity': 'quantity',
                'Tax 5%': 'tax',
                'Total': 'total',
                'Date': 'date',
                'Time': 'time',
            })

            # Convert date and time columns to datetime objects
            df['date'] = pd.to_datetime(df['date']).dt.date
            df['time'] = pd.to_datetime(df['time'], format='%H:%M').dt.time

            # Save the new transactions to the database
            df_dict = df.to_dict('records')
            Transaction.objects.bulk_create([
                Transaction(
                    invoice_id=row['invoice_id'],
                    product_line=row['product_line'],
                    unit_price=row['unit_price'],
                    quantity=row['quantity'],
                    tax=row['tax'],
                    total=row['total'],
                    date=row['date'],
                    time=row['time']
                ) for row in df.to_dict('records') if 'quantity' in row
            ])

            # Retrieve the transactions for Health and Beauty product line
            transactions = Transaction.objects.filter(product_line='Health and beauty')

            # Pass the transactions to the template for rendering
            return render(request, 'templates/transactions.html', {'transactions': transactions})
    else:
        form = CSVUploadForm()

    return render(request, 'templates/upload.html', {'form': form})
