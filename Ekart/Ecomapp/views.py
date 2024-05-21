from django.shortcuts import render,redirect
from .models import product,cart,Order
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.db.models import Q
import razorpay
import random
 

from django.contrib.auth import authenticate,login,logout
# Create your views here.

def hello(request):
    context={}
    prod = product.objects.all()
    context["data"] = prod
    print(prod)
    print("my current request id is",request.user.id)
    print(request.user.is_authenticated)

    return render(request,"index.html",context)

# def register(request):
#     context={}
#     if request.method=='POST':
#         un=request.POST["uname"]
#         un1=request.POST['password']
#         un2=request.POST['cpassword']

        
#         if un=="" or un1=="" or un2=="":
#             context["errmsg"]="Field can not be empty"
#             return render(request,"register.html",context)
        
#         elif un1 !=un2:
#             context["errmsg"]="password and cpassword didnt match"
#             return render(request,"register.html",context)
        
#         else:
#             u=User.objects.create(username=un,email=un)
#             u.set_password(un1)
#             u.save()
#             context["success"]="Registration successfull !!!"
#             return render(request,"register.html",context)
        
#     else:
#         return render(request,'register.html',)
    

# def ulogin(request):
#     if request.method=="POST":

#         context={}
#         nm=request.POST["uname"]
#         p=request.POST["password"]
#         print(nm,p)
#         u=authenticate(username=nm,password=p)
#         print(u)

#         if u is not None:
#             login(request,u)
#             #return redirect("/index")
#             return redirect(request,"login.html")

#         else:
#             context["errmsg"]="Invalid user name and password"
#             return render(request,"login.html",context)
        
#     return render(request,"login.html")


    
    


# def ulogout(request):
#     logout(request)
#     return redirect('/index')

def register(request):
    context={}
    if request.method=="GET":
        return render(request,"register.html")
    else:
        nm=request.POST['uname']
        p=request.POST['password']
        cp=request.POST['cpassword']
        print(nm,p,cp)
        if nm =='' or p=='' or cp=='':
            context["errmsg"]="Fields can not be empty"
            return render(request,"register.html",context)
        
        elif p!=cp:
            context["errmsg"]="p and cp is not matching "
            return render(request,"register.html",context)
        
        else:
            
            context['success']="Registration successfull please login now"
            #obj=modelname.objects.create(colnames=values)
            u=User.objects.create(username=nm,email=nm)
            u.set_password(p)# used to encript password
            u.save()
            return render(request,'register.html',context)
        
        
def ulogin(request):
    context={}
    if request.method == "POST":
        un=request.POST["uname"]
        p=request.POST["password"]
        print(un,p)
        u=authenticate(username=un,password=p)
        print(u)
        
        if u is not None:
            login(request,u)
            return redirect("/hello")
        
        else:
            context["errmsg"]="Invalid user name and password"
            return render(request,"login.html",context)
        

    return render(request,"login.html")
        

def ulogout(request):
    logout(request)
    return redirect('/login')


def catfilter(request,cv):
    p=product.objects.filter(cat=cv)
    context={}
    context["data"]=p
    return render(request,"index.html",context)
            


def sort(request,pv):
    context={}
    if pv == "1":
        p=product.objects.order_by("-price").filter(is_active=True)

    else:
        p=product.objects.order_by("price").filter(is_active=True)
    context["data"]=p

    return render(request,"index.html",context)

def filterbyprice(request):
    mn=request.GET["min"]
    mx=request.GET["max"]

    q1=Q(price__gte=mn)
    q2=Q(price__lte=mx)
    p=product.objects.filter(q1 & q2)
    context={"data":p}

    return render(request,"index.html",context)  


def prodcutdetails(request,rid):
    print(rid)
    p=product.objects.filter(id=rid)
    context={}
    context["data"]=p
    print(p)
    return render(request,"productdetails.html",context) 

def viewscart(request):
    context={}
    c=cart.objects.filter(userid=request.user.id)

    q1=c[0].qty
    context["carts"]=c
    sum=0
    for x in c:
        sum=sum+x.pid.price*x.qty
        


    print(sum)
    context["total"]=sum
    context["items"]=len(c)
    return render(request,"cart.html",context)




def addtocart(request,pid):
    #print(pid)
    context={}
    if request.user.is_authenticated:

        u=User.objects.filter(id=request.user.id)
        p=product.objects.filter(id=pid)
        context["data"]=p
        q1=Q(userid=u[0])
        q2=Q(pid=p[0])
        c=cart.objects.filter(q1 & q2)
        n=len(c)
        if n==1:
            context["msg"]="product already exist in cart"
            return render(request,"productdetails.html",context)
        
        else:
            c=cart.objects.create(pid=p[0],userid=u[0])
            c.save()
            context["msg"]="product added in cart successfully"

            return render(request,"productdetails.html",context)
        
        
        

        return render(request,"productdetails.html",context)
    else:
        return redirect('/ulogin')
    

def updateqty(request,x,cid):
    c=cart.objects.filter(id=cid)
    q=c[0].qty
    print(q)
    if x=="1":
        q=q+1
    elif q>1:
        q=q-1
    c.update(qty=q)

    return redirect("/viewscart")


def placeorder(request):
    c=cart.objects.filter(userid=request.user.id)
    orderid=random.randrange(1000,9999)
    for x in c:
        amount=x.qty* x.pid.price
        o=Order.objects.create(order_id=orderid,amt=amount,p_id=x.pid,user_id=x.userid)
        o.save()
        x.delete()
    
    return redirect("/fetchorder")

def fetchorder(request):
    orders=Order.objects.filter(user_id=request.user.id)
    context={}
    context["orders"]=orders
    sum=0
    for x in orders:
        sum=sum+x.amt
    context["totalamount"]=sum
    context["n"]=len(orders)
    

    return render(request,"placeorder.html",context)



def fetchorder(request):
    orders=Order.objects.filter(user_id=request.user.id)
    context={}
    context["orders"]=orders
    sum=0
    for x in orders:
        sum=sum+x.amt
    context["totalamount"]=sum
    context["n"]=len(orders)
    

    return render(request,"placeorder.html",context)


def makepayment(request):
    client = razorpay.Client(auth=("rzp_test_RH6U8LJAePggOS", "KqBgO7262Jou6hT2DALD8VYs"))
    orders=Order.objects.filter(user_id=request.user.id)
    context={}
    context["orders"]=orders
    sum=0

    for x in orders:
        sum=sum+x.amt
        orderid=x.order_id
    

    data = { "amount": 500, "currency": "INR", "receipt": "order_rcptid_11" }
    payment = client.order.create(data=data)
    print(payment)
    context={}
    context["payments"]=payment
    return render(request,"pay.html")