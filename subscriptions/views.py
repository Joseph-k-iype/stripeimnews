from collections import UserList
import email
from email import message
import stripe
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User  # new
from django.http.response import JsonResponse, HttpResponse  # updated
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib import messages
from subscriptions.forms import *
from subscriptions.models import  *
import requests 

import ipaddress
import feedparser


from subscriptions.models import task as Task



def index(request):
    apiKey = "20ca105d900e4b7aa72e8e86f0e0d208"
    url = "https://newsapi.org/v2/top-headlines?sources=google-news-in&apiKey=20ca105d900e4b7aa72e8e86f0e0d208"
    news = requests.get(url).json()['articles']
    ip = request.META['REMOTE_ADDR']
    #get the ip address of the client
    ip_address = ipaddress.ip_address(ip)
    #save the ip address in the database
    IpAddress.objects.create(ip=ip_address)
    #get the ip address of the client
    count = IpAddress.objects.count()+2500
    #get total number of users
    noofusers = User.objects.count()+100
    print(noofusers)
    return(render(request, "index.html", {'news' : news, 'count': count, 'noofusers': noofusers}))

def index2(request):
    # url of blog feed
    feed_url = "https://news.google.com/rss/search?q=Business+News&hl=en-US&gl=US&ceid=US:en"

    blog_feed = feedparser.parse(feed_url)
        # returns title of the blog site
    blog_feed.feed.title

    # returns the link of the blog
    # and number of entries(blogs) in the site.
    blog_feed.feed.link
    print(len(blog_feed.entries))
    a = len(blog_feed.entries)

    # Details of individual blog can
    # be accessed by using attribute name
    for i in range(a):
        print(blog_feed.entries[i].title)
        print(blog_feed.entries[i].link)
        print(blog_feed.entries[i].description)



    return(render(request, "index2.html"))

@login_required
def home(request):
    if(request.user.is_superuser):
        return(redirect("/admin"))
    elif(request.user.is_staff):
        return(redirect("/operations"))
    try:
        # Retrieve the subscription & product
        stripe_customer = StripeCustomer.objects.get(user=request.user)
        stripe.api_key = settings.STRIPE_SECRET_KEY
        subscription = stripe.Subscription.retrieve(
            stripe_customer.stripeSubscriptionId)
        product = stripe.Product.retrieve(subscription.plan.product)

        # Feel free to fetch any additional data from 'subscription' or 'product'
        # https://stripe.com/docs/api/subscriptions/object
        # https://stripe.com/docs/api/products/object

        return render(request, 'home.html', {
            'subscription': subscription,
            'product': product,
        })

    except StripeCustomer.DoesNotExist:
        return render(request, 'home.html')

@login_required
def application(request):
    try:
        stripe_customer = StripeCustomer.objects.get(user=request.user)
        stripe.api_key = settings.STRIPE_SECRET_KEY
        subscription = stripe.Subscription.retrieve(
            stripe_customer.stripeSubscriptionId)
        product = stripe.Product.retrieve(subscription.plan.product)

        # get article data of the logged in user
        articles = formforsubmit.objects.filter(user=request.user)

        return render(request, 'application.html', {
            'subscription': subscription,
            'product': product,
            'articles': articles
        })
    except StripeCustomer.DoesNotExist:
        return redirect('/home')

@login_required
def payment_info(request):
    return(render(request, "payment_info.html"))

@login_required
def postform(request):
    try:
        stripe_customer = StripeCustomer.objects.get(user=request.user)
        stripe.api_key = settings.STRIPE_SECRET_KEY
        subscription = stripe.Subscription.retrieve(
            stripe_customer.stripeSubscriptionId)
        product = stripe.Product.retrieve(subscription.plan.product)
        articles = formforsubmit.objects.filter(user=request.user)
        #generate a form for the user to post their article
        #error 'QueryDict' object has no attribute 'user'

        form = submitform(request.POST, request.FILES)
        print("FORM VALID = ",form.is_valid())
        if form.is_valid():
            form = form.save(commit=False)
            form.user = request.user
            form.save()
            messages.success(request, "Article posted successfully")
            return redirect("/application")
        

        return render(request, 'postform.html', {
            'subscription': subscription,
            'product': product,
            'articles': articles,
            'form': form
        })
    except StripeCustomer.DoesNotExist:
        return redirect("/home")
          
@login_required
def responseform(request):
    try:
        stripe_customer = StripeCustomer.objects.get(user=request.user)
        stripe.api_key = settings.STRIPE_SECRET_KEY
        subscription = stripe.Subscription.retrieve(
            stripe_customer.stripeSubscriptionId)
        product = stripe.Product.retrieve(subscription.plan.product)
        articles = formforsubmit.objects.filter(user=request.user)
        #generate a form for the user to post their article
        #error 'QueryDict' object has no attribute 'user'

        form = submitform(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.user = request.user
            form.save()
            messages.success(request, "Article posted successfully")
            return render(request, 'application_form.html', {
                'subscription': subscription,
                'product': product,
                'articles': articles,
                'form': form
            })
        return render(request, 'postform.html', {
            'subscription': subscription,
            'product': product,
            'articles': articles,
            'form': form
        })
    except StripeCustomer.DoesNotExist:
        return render(request, 'home.html')

@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)

@csrf_exempt
def create_checkout_session(request):
    if request.method == 'GET':
        domain_url = 'http://localhost:8000/'
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            checkout_session = stripe.checkout.Session.create(
                client_reference_id=request.user.id if request.user.is_authenticated else None,
                success_url=domain_url +
                'success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=domain_url + 'cancel/',
                payment_method_types=['card'],
                mode='subscription',
                line_items=[
                    {
                        'price': settings.STRIPE_PRICE_ID,
                        'quantity': 1,
                    }
                ]
            )
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})

@login_required
def success(request):
    return render(request, 'success.html')

@login_required
def cancel(request):
    return render(request, 'cancel.html')

@csrf_exempt
def stripe_webhook(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    endpoint_secret = settings.STRIPE_ENDPOINT_SECRET
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        # Fetch all the required data from session
        client_reference_id = session.get('client_reference_id')
        stripe_customer_id = session.get('customer')
        stripe_subscription_id = session.get('subscription')

        # Get the user and create a new StripeCustomer
        user = User.objects.get(id=client_reference_id)
        StripeCustomer.objects.create(
            user=user,
            stripeCustomerId=stripe_customer_id,
            stripeSubscriptionId=stripe_subscription_id,
        )
        print(user.username + ' just subscribed.')

    return HttpResponse(status=200)

# @login_required
# def tasksview(request):
#     #view for the tasks assigned to the user if user is a staff member
#     if request.user.is_staff:
#         tasks = task.objects.filter(user=request.user)
#         return render(request, 'tasklist.html', {'tasks': tasks})
# @login_required
# def taskdetailview(request, id):
#     #staff should view only thier tasks
#     form = tasksforoperationsform(request.POST, request.FILES)
#     if request.user.is_staff:
#         task = task.objects.get(id=id)
#         if request.method == 'POST':
#             if form.is_valid():
#                 form = form.save(commit=False)
#                 form.user = request.user
#                 form.save()
#                 messages.success(request, "Task updated successfully")
#                 return redirect('/task_detail/'+str(id))
#             else:
#                 messages.error(request, "Error updating task")
#                 return redirect('/task_detail/'+str(id))
#         return render(request, 'task_detail.html', {'task': task, 'form': form})

#     else:
#         task = task.objects.get(id=id)
#         return render(request, 'task_detail.html', {'task': task})
#         return redirect('/')
#     return render(request, 'task_detail.html', {'task': tassk, 'id': id, 'form': form})

@login_required
def tasksview(request):
    #view for the tasks assigned to the user if user is a staff member
    if request.user.is_staff:
        tasks = task.objects.filter(user=request.user)
        return render(request, 'tasklist.html', {'tasks': tasks})
    else:
        return redirect('/')

@login_required
def taskdetailview(request, id):
    #staff should view only thier tasks
    form = tasksforoperationsform(request.POST, request.FILES)
    if request.user.is_staff:
        
        mTask = Task.objects.get(id=id)
        if request.method == 'POST':
            if form.is_valid():
                form = form.save(commit=False)
                form.user = request.user
                form.save()
                messages.success(request, "Task updated successfully")
                return redirect('/task_detail/'+str(id))
            else:
                messages.error(request, "Error updating task")
                return redirect('/task_detail/'+str(id))
        return render(request, 'task_detail.html', {'task': mTask, 'form': form})

    else:
        task = task.objects.get(id=id)
        return render(request, 'task_detail.html', {'task': task})
        return redirect('/')
    return render(request, 'task_detail.html', {'task': tassk, 'id': id, 'form': form})

@login_required
def showConversationsToAdmin(request):
    if(request.user.is_superuser):
        # TODO Seperate staffConversations using foreign Key
        userConv = Conversation.objects.filter(user__is_staff__lt=True).order_by('seenByAdmin')
        staffConv = Conversation.objects.filter(user__is_staff__gte=True).order_by('seenByAdmin')
        return(render(request,"mail_list.html",{"userConv" : userConv, "staffConv" : staffConv}))
    else:
        return(redirect("/"))


def getMessages(request, mEmail = ""):
    if(request.user.is_superuser):
        # messages are for admin
        mUser = User.objects.filter(email = mEmail).get()
        userConv = Conversation.objects.filter(user = mUser).get()
        if(userConv.seenByAdmin == False):
            userConv.seenByAdmin = True
            userConv.save()
            messageList = Messages.objects.filter(user = mUser, seenByAdmin = False)
            resp = JsonResponse({"messages" : list(messageList.values())})
            for i in messageList:
                i.seenByAdmin = True
                i.save()
            return(resp)
        else:
            return(JsonResponse({"messages" : ""}))
    else:
        userConv = Conversation.objects.filter(user = request.user).get()
        if(userConv.seenByUser == False):
            userConv.seenByUser = True
            userConv.save()
            messageList = Messages.objects.filter(user = request.user, seenByUser = False)
            resp = JsonResponse({"messages" : list(messageList.values())})
            print(resp)
            for i in messageList:
                i.seenByUser = True
                i.save()
            return(resp)
        else:
            return(JsonResponse({"messages" : ""}))


@login_required
def messagePage(request, mEmail = ""):
    
    if(request.user.is_superuser):
        # Message from and to the admin
        mUser = User.objects.filter(email = mEmail).get()
        userConv = Conversation.objects.filter(user = mUser).get()
        if(request.method == "POST"):
            userConv.seenByUser = False
            userConv.save()
            message = request.POST["message"]
            newMessage = Messages(user = mUser, message = message, fromAdmin = True, seenByAdmin = True, seenByUser = False, timeSent = datetime.now())
            newMessage.save()
            return(JsonResponse({'messages' : message}))
        else:
            # List the messages
            userConv.seenByAdmin = True
            userConv.save()
            messageList = Messages.objects.filter(user = mUser).order_by('timeSent')
            for i in messageList:
                i.seenByAdmin = True
                i.save()
            return(render(request, "messages.html", {"messages" : messageList}))
    else:
        try:
            userConv = Conversation.objects.filter(user = request.user).get()
        except:
            userConv = Conversation(user = request.user, seenByUser = True, seenByAdmin = True)
            userConv.save()
        if(request.method == "POST"):
            userConv.seenByAdmin = False
            userConv.save()
            message = request.POST["message"]
            newMessage = Messages(user = request.user, message = message, fromAdmin = False, seenByAdmin = False, seenByUser = True, timeSent = datetime.now())
            newMessage.save()
            return(JsonResponse({'messages' : message}))
        else:
            userConv.seenByUser = True
            userConv.save()
            messageList = Messages.objects.filter(user = request.user).order_by('timeSent')
            for i in messageList:
                i.seenByUser = True
                i.save()
            return(render(request, "messages.html", {"messages" : messageList}))


@login_required
def newConversation(request):
    if(request.user.is_superuser):
        if(request.method == "POST"):
            mUser = User.objects.filter(email = request.POST["email"]).get()
            message = request.POST["message"]
            # Check if conversation exists 
            try:
                userConv = Conversation.objects.filter(user = mUser).get()
                userConv.seenByUser = False
            except:
                userConv = Conversation(user = mUser, seenByAdmin = True, seenByUser = False)
            finally:
                userConv.save()
                newMessage = Messages(user = mUser, message = message, fromAdmin = True, seenByAdmin = True, seenByUser = False, timeSent = datetime.now())
                newMessage.save()
                return(redirect("/admin/subscriptions/message/"+mUser.email))
        else:
            # TODO seperate userList and staffList
            userList = list(User.objects.filter(is_staff = False).values())
            staffList = list(User.objects.filter(is_staff = True).filter(is_superuser = False).values())
            return(render(request, "startchat.html", {'userList' : userList , 'staffList' : staffList}))
    else:
        return(redirect("/"))
