import json
from django.shortcuts import render

from django.http import HttpResponse
from .models import Product
from math import ceil
from .models import ContactUs, Orders, OrderUpdate


# Create your views here.

def index(request):
    # allProducts = Product.objects.all()
    # print(allProducts)
    # n = len(allProducts)
    # slide = n//4 + ceil((n/4)-(n//4))
    # params = {'no_of_slides': slide, 'products': allProducts, 'range': range(1, slide)}
    #
    # return render(request, 'shop/index.html', params)
    allProds = []
    catprods = Product.objects.values('category', 'id')
    print(catprods)
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])

    # params = {'no_of_slides':nSlides, 'range': range(1,nSlides),'product': products}
    # allProds = [[products, range(1, nSlides), nSlides],
    #             [products, range(1, nSlides), nSlides]]
    params = {'allProds': allProds}
    return render(request, 'shop/index.html', params)


def searchMatch(query, item):
    """return true only if query matches the item"""
    if query in item.desc.lower() or query in item.product_name.lower() or query in item.category.lower():
        return True
    else:
        return False


def search(request):
    query = request.GET.get('search')
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prodtemp = Product.objects.filter(category=cat)
        prod = [item for item in prodtemp if searchMatch(query, item)]

        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        if len(prod) != 0:
            allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds': allProds, "msg": ""}
    if len(allProds) == 0 or len(query) < 4:
        params = {'msg': "No Such item please try something else!"}
    return render(request, 'shop/search.html', params)


def about(request):
    return render(request, 'shop/aboutUs.html')


def contact(request):
    thank = False
    if request.method == "POST":
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        desc = request.POST.get('desc', '')
        if not name == '':
            contactUs = ContactUs(name=name, email=email, phone=phone, desc=desc)
            if not ContactUs.objects.filter(name=name, email=email, phone=phone, desc=desc).exists():

                contactUs.save()
                thank = True
            else:
                print('already Set Data')
        else:
            print('blank Data')
    return render(request, 'shop/contactUs.html', {'thank': thank})


# noinspection PyBroadException
def tracker(request):
    if request.method == "POST":
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email', '')
        try:
            order = Orders.objects.filter(order_id=orderId, email=email)
            if len(order) > 0:
                update = OrderUpdate.objects.filter(order_id=orderId)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timestamp})
                    response = json.dumps({"status": "success", "updates": updates, "itemsJson": order[0].items_json},
                                          default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{"status":"noitem"}')
        except Exception as e:
            return HttpResponse('{"status":"error"}')

    return render(request, 'shop/tracker.html')


def productView(request, myId):
    product = Product.objects.filter(id=myId)

    return render(request, 'shop/productView.html', {'product': product[0]})


def checkout(request):
    if request.method == "POST":
        items_json = request.POST.get('itemsJson', '')
        amount = request.POST.get('amount', '')
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address1', '') + " " + request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')

        if not name == '':
            order = Orders(items_json=items_json, name=name, email=email, address=address, city=city,
                           state=state, zip_code=zip_code, phone=phone, amount=amount)
            if not Orders.objects.filter(items_json=items_json, name=name, email=email, address=address, city=city,
                                         state=state, zip_code=zip_code, phone=phone).exists():

                order.save()
                update = OrderUpdate(order_id=order.order_id, update_desc="The order has been placed")
                update.save()
                thank = True
                myOrder_id = order.order_id
                return render(request, 'shop/checkout.html', {'thank': thank, 'id': myOrder_id})
            else:
                print('already Set Data')
        else:
            print('blank Data')

    return render(request, 'shop/checkout.html')
