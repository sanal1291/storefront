from django.db.models.fields import IntegerField
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.db.models import Q, F, ExpressionWrapper, Value, Func
from django.db.models.functions import Concat
from django.db.models.aggregates import Avg, Count, Max,  Min
from store.models import Collection, Customer, Order, OrderItem, Product
from tags.models import TaggedItem
from django.contrib.contenttypes.models import ContentType
from django.db import transaction

# Create your views here.
# def say_hello(request):
#     # query_set = Product.objects.all()
#     # product = Product.objects.get(pk=1)
#     # try:
#     #     product = Product.objects.get(pk=0)
#     # except ObjectDoesNotExist:
#     #     pass
#     # product = Product.objects.filter(pk=0).first()
#     # exists = Product.objects.filter(pk=0).exists()
#     return render(request, 'hello.html',{'name':"sanal"})

# def say_hello(request):
#     # queryset = Product.objects.filter(unit_price__gt=20)
#     # queryset = Product.objects.filter(unit_price__range=(20,300))
#     # queryset = Product.objects.filter(collection__id__range=(2,2))
#     # queryset = Product.objects.filter(title__icontains='coffe')
#     # queryset = Product.objects.filter(last_update__year=2021)
#     queryset = Product.objects.filter(description__isnull=True)
#     return render(request, 'hello.html',{'name':"sanal", 'products': list(queryset)})

# # ////complex
# def say_hello(request):
#     # products: inventory < 10 and price <100
#     # queryset = Product.objects.filter(collection__lt=10,unit_price__lt=100)
#     # queryset = Product.objects.filter(collection__lt=10).filter(unit_price__lt=100)
#     # queryset = Product.objects.filter(Q(collection__lt=20)& Q(unit_price__lt=100))
#     # products: inventory < 10 or price <100///////////////////// ~=not
#     # queryset = Product.objects.filter(Q(collection__lt=20)| Q(unit_price__lt=100))
#     return render(request, 'hello.html',{'name':"sanal", 'products': list(queryset)})

# def say_hello(request):
#     # products: inventory = price
#     # queryset = Product.objects.filter(inventory=F('unit_price'))
#     queryset = Product.objects.filter(inventory=F('collection__id'))
#     return render(request, 'hello.html',{'name':"sanal", 'products': list(queryset)})

# def say_hello(request):
#     # queryset = Product.objects.order_by('unit_price','-title').reverse()
#     # product = Product.objects.order_by('unit_price')[0]
#     # product = Product.objects.earliest('unit_price')
#     # product = Product.objects.latest('unit_price')
#     return render(request, 'hello.html',{'name':"sanal", 'products': list(queryset)})

# def say_hello(request):
#     queryset = Product.objects.all()[5:10]
#     return render(request, 'hello.html',{'name':"sanal", 'products': list(queryset)})

# def say_hello(request):
#     queryset = Product.objects.values('id','title','collection__title')
#     queryset = Product.objects.values_list('id','title','collection__title')
#     return render(request, 'hello.html',{'name':"sanal", 'products': list(queryset)})

# products that have been orderd ie in orderitem table and then sort them by title
# def say_hello(request):
#     # arr,queryset = {},[]
#     # arr = set([item.product_id for item in list(OrderItem.objects.all())])
#     queryset = Product.objects.filter(id__in=OrderItem.objects.values('product_id').distinct()).order_by('title')
#     return render(request, 'hello.html',{'name':"sanal", 'products': list(queryset)})


# def say_hello(request):
#     # result = Product.objects.only('id','title')
#     result = Product.objects.defer('title','description')
#     return render(request, 'hello.html',{'name':"sanal", 'products': list(result)})

# def say_hello(request):
#     # select_related 1 (1 relation)
#     # prefetc_related (n) multtiple relation
#     # result = Product.objects.select_related('collection').all()
#     # result = Product.objects.select_related('collection__featured_product').all()
#     result = Product.objects.prefetch_related('promotions').select_related('collection').all()
#     return render(request, 'hello.html',{'name':"sanal", 'result': list(result)})
# get the last 5 orders with their customer and items (incl product)
# def say_hello(request):
#     result = Order.objects.select_related('customer').prefetch_related('orderitem_set__product').order_by('placed_at').all()[:5]
#     return render(request, 'hello.html',{'name':"sanal", 'result': list(result)})

# def say_hello(request):
#     result = Product.objects.filter(collection__id=1).aggregate(count =Count('id'), min_prpice=Min('unit_price'))
#     return render(request, 'hello.html',{'name':"sanal", 'result': result})
#
# def say_hello(request):
# result = Product.objects.annotate(sanalz=F('id'))
#     idx2= ExpressionWrapper(F('id')+Value(2), output_field='idx2')
#     result = Product.objects.annotate(idx2=idx2)
#     return render(request, 'hello.html',{'name':"sanal", 'result': result})


# calling database functions
# def say_hello(request):
#     # result = Customer.objects.annotate(
#     #     full_name=Func(F('first_name'),Value(' '),F('last_name'), function='CONCAT')
#     # )
#     # result = Customer.objects.annotate(
#     #     full_name=Concat('first_name',Value(' ') ,'last_name')
#     # )
#     # result = Customer.objects.annotate(
#     #     orders_count = Count('order')
#     # )
#     discount_price = ExpressionWrapper(F('unit_price') *Value( 0.8),output_field=IntegerField())
#     result = Product.objects.annotate(
#         discount_price = discount_price
#     )
#     return render(request, 'hello.html',{'name':"sanal", 'result': result})

# def say_hello(request):
#     contentType = ContentType.objects.get_for_model(Product)
#     result =TaggedItem.objects \
#         .select_related('tag') \
#         .filter(content_type= contentType,
#             object_id = 1).all()
#     return render(request, 'hello.html',{'name':"sanal", 'result': result})
# def say_hello(request):
#     result = TaggedItem.objects.get_tags_for(Product,2)
#     return render(request, 'hello.html',{'name':"sanal", 'result': result})

# def say_hello(request):
#     collection = Collection()
#     # collection = Collection(title='Video games',featured_product=Product(pk=1)) #not preffered
#     collection.title = "Video games"
#     collection.featured_product = Product(pk=1)
#     # collection.featured_product_id = 1
#     collection.save()
#     # collection = Collection.objects.create(name='a', featured_product=Product(pk=1))
#     return render(request, 'hello.html', {'name': "sanal"})

# def say_hello(request):
#     # collection = Collection.objects.get(pk=11)  # dont use constructor with pk
#     # collection.featured_product = None
#     # collection.save()
#     # best 1 less db query than that of above
#     Collection.objects.filter(pk=11).update(featured_product=None)
#     # collection = Collection.objects.create(name='a', featured_product=Product(pk=1))
#     return render(request, 'hello.html', {'name': "sanal"})

# def say_hello(request):
#     collection = Collection.objects.get(pk=11)  # dont use constructor with pk
#     collection.delete()
#     # Collection.objects.filter(id__gt=5).delete()
#     # collection = Collection.objects.create(name='a', featured_product=Product(pk=1))
#     return render(request, 'hello.html', {'name': "sanal"})

# transaction
# @transaction.atomic() #means either both works or none works, ie db operations
# def say_hello(request):
#     with transaction.atomic():
#         order = Order()
#         order.customer_id = 1
#         order.save()

#         item = OrderItem()
#         item.order = order
#         item.product_id = 1
#         item.quantity = 2
#         item.unit_price = 200
#         item.save()
#     return render(request, 'hello.html', {'name': "sanal"})

def say_hello(request):
    with transaction.atomic():
        order = Order()
        order.customer_id = 1
        order.save()

        item = OrderItem()
        item.order = order
        item.product_id = 1
        item.quantity = 2
        item.unit_price = 200
        item.save()
    return render(request, 'hello.html', {'name': "sanal"})
