import csv
from datetime import datetime
from django.shortcuts import render, redirect
from io import TextIOWrapper
from .models import Transaction
from .forms import CSVUploadForm

def upload_csv(request):
    Transaction.objects.all().delete()

    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Parse the uploaded CSV file
            csv_file = request.FILES['file']
            data = csv.reader(TextIOWrapper(csv_file.file, encoding='iso-8859-1'))
            next(data) # Skip the header row
            
            # Save the new transactions to the database
            count = 0
            for row in data:
                if count < 10:
                    invoice_id = row[0]
                    product_line = row[5]
                    unit_price = float(row[6])
                    quantity = int(row[7])
                    tax = float(row[8])
                    total = float(row[9])
                    date = datetime.strptime(row[10], '%m/%d/%Y').date()
                    time = datetime.strptime(row[11], '%H:%M').time()
                    
                    # Check if transaction already exists in the database
                    if not Transaction.objects.filter(invoice_id=invoice_id).exists():
                        # Save only these required fields to the database
                        Transaction.objects.create(
                        invoice_id=invoice_id,
                        product_line=product_line,
                        unit_price=unit_price,
                        quantity=quantity,
                        tax=tax,
                        total=total,
                        date=date,
                        time=time,
                        )
                        count += 1
                    
            # Retrieve the transactions for Health and Beauty product line
            transactions = Transaction.objects.filter(product_line='Health and beauty')
            
            # Pass the transactions to the template for rendering
            return render(request, 'templates/transactions.html', {'transactions': transactions})
    else:
        form = CSVUploadForm()
    
    return render(request, 'templates/upload.html', {'form': form})


# Checking database data 

from django.http import JsonResponse
from .models import Transaction

def view_transactions(request):
    transactions = Transaction.objects.all()
    data = {'transactions': list(transactions.values())}
    return JsonResponse(data)