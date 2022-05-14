import stripe
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User  # new
from django.http.response import JsonResponse, HttpResponse  # updated
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib import messages
from subscriptions.models import StripeCustomer, formforsubmit  # new
from .forms import submitform, sendmailform


def index(request):
    return(render(request, "index.html"))



@login_required
def home(request):
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

        form = submitform(request.POST)
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




        #get data from the form and save it to the database
    #     if request.method == 'POST':
    #         form = postform(request.POST)
    #         if form.is_valid():
    #             article = form.save(commit=False)
    #             article.url = form.data['headline']
    #             article.save()
    #             return render(request, 'application.html')
    #     else:
    #         form = postform()
    #     return render(request, 'postform.html', {'form': form})
    # except StripeCustomer.DoesNotExist:
    #     return render(request, 'home.html')


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


#send email to the user when they submit an article
def send_email(request):
    if request.method == 'POST':
        form = sendmailform(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.user = request.user
            form.save()
            messages.success(request, "Email sent successfully")
            return render(request, 'response_form.html', {'form': form})
        
        return render(request, 'response_form.html', {'form': form})
    else:
        form = sendmailform()
        return render(request, 'response_form.html', {'form': form})

