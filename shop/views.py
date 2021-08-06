
from django.shortcuts import render
from .models import product,Contact,Order,OrderUpdate 
from django.http import HttpResponse
from math import ceil
import json
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
def index(request):
    allprods=[]
    catprods=product.objects.values('category','id')
    cats={item['category'] for item in catprods}
    for cat in cats:
        prod=product.objects.filter(category=cat)
        n=len(prod)
        nslides=n//4+ceil((n/4)-(n//4))
        allprods.append([prod,range(1,nslides),nslides])
    params={'allprods':allprods}
    return render(request,'shop/index.html',params)


def searchmatch(query, item):
    if query in item.product_name.lower():
        return True
    if query in item.category.lower():
        return True
    if query in item.desc.lower():
        return True
    else:
        return False


def search(request):
    query = request.GET.get('search')
    allprods = []
    catprods = product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prodtemp = product.objects.filter(category=cat)
        prod=[item for item in prodtemp if searchmatch(query,item)]
        n = len(prod)
        nslides = n // 4 + ceil((n / 4) - (n // 4))
        if len(prod) != 0:
            allprods.append([prod, range(1, nslides), nslides])
    params = {'allprods': allprods}
    # print(len(allprods))
    if len(allprods)==0 :
        # or len(query)<3
        params={'msg':"please make sure to enter relevent search query"}
    return render(request, 'shop/search.html', params)


def about(request):
    return render(request,'shop/about.html')

def contact(request):
    if request.method=='POST':
        # print(request)
        name=request.POST.get('name',"")
        email=request.POST.get('email',"")
        phone=request.POST.get('phone',"")
        desc=request.POST.get('desc',"")
        # print(name,email,phone,desc)
        contact=Contact(name=name,email=email,phone=phone,desc=desc)
        contact.save()
        thank = True
        return render(request, 'shop/contact.html', {'thank': thank})
    return render(request,'shop/contact.html')

def tracker(request):
    if request.method=="POST":
        orderId = request.POST.get('orderId', '') 
        email = request.POST.get('email', '')
        try:
            order = Order.objects.filter(order_id=orderId, email=email)
            if len(order)>0:
                update = OrderUpdate.objects.filter(order_id=orderId)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timestamp})
                    response = json.dumps({"status":"success","updates":updates,"itemsJson":order[0].items_json}, default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{"status":"noitem"}')
        except Exception as e:
            return HttpResponse('{"status":"error"}')

    return render(request, 'shop/tracker.html')

 

def productview(request, myid):
    #fetch the product using the id
    Product=product.objects.filter(id=myid)
    return render(request, 'shop/productview.html',{'product':Product[0]})


def checkout(request):
    if request.method=="POST":
        items_json=request.POST.get('itemsjson', '')
        name=request.POST.get('name', '')
        amount=request.POST.get('amount', '')
        email=request.POST.get('email', '')
        address=request.POST.get('address1', '') + " " + request.POST.get('address2', '')
        city=request.POST.get('city', '')
        state=request.POST.get('state', '')
        zip_code=request.POST.get('zip_code', '')
        phone=request.POST.get('phone', '')
        order = Order(items_json=items_json ,name=name, email=email, address= address, city=city, state=state, zip_code=zip_code, phone=phone,amount=amount)
        order.save()
        update=OrderUpdate(order_id=order.order_id,update_desc="the order has been placed")
        update.save()
        thank=True
        id=order.order_id
        # return render(request, 'shop/checkout.html',{'thank':thank,'id':id})
        # Request paytm to transfer the amount to your account after payment by user
    return render(request, 'shop/checkout.html')

@csrf_exempt
def handlerequest(request):
    # paytm will send you post request here
    pass
