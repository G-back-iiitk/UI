from django.shortcuts import render

# Create your views here.
def index(request):
    Stock_name =['SnP 500','Tesla','Boring Co.','Genral Motors', 'Tata Steels']
    Stock_price =['300','400','250','800','600']
    Stock = zip(Stock_name,Stock_price)
    return render(request,'home/index.html',{'stocks':Stock})
