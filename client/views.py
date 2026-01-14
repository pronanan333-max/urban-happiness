from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.conf import settings 
from django.utils import timezone
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse


from .forms import UpdateUserForm
from writer.models import Article
from account.models import CustomUser
from django.db.models import Q

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .stripe_handler import create_checkout_session, handle_checkout_session, create_donation_session
from .models import Subscription

import stripe
stripe.api_key = settings.STRIPE_SECRET_KEY




@login_required(login_url='my-login')
def client_dashboard(request):
    query = request.GET.get('q', '')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    location = request.GET.get('location')

    articles = Article.objects.all()

    # Search keyword
    if query:
        articles = articles.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(location__icontains=query)
        )

    # Filter location
    if location:
        articles = articles.filter(location__icontains=location)

    # Filter price
    if min_price:
        articles = articles.filter(price__gte=min_price)
    if max_price:
        articles = articles.filter(price__lte=max_price)

    # ส่ง location ทั้งหมดแบบไม่ซ้ำ
    all_locations = Article.objects.values_list('location', flat=True).distinct()

    context = {
        'AllClientArticles': articles,
        'all_locations': all_locations,
    }
    return render(request, 'client/client-dashboard.html', context)
    
@login_required(login_url='my-login')
def account_management(request):
    form = UpdateUserForm(instance=request.user)

    if request.method == 'POST':
        form = UpdateUserForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('client-dashboard')

    context = {'UpdateUserForm': form}
    return render(request, 'client/account-management.html', context)


@login_required(login_url='my-login')
def delete_account(request):
    if request.method == 'POST':
        request.user.delete()
        return redirect('home')  # เปลี่ยน 'home' ตามชื่อ URL ของหน้าหลักคุณ

    return render(request, 'client/delete-account.html')


@login_required(login_url='my-login')
def client_article_detail(request, pk):
    try:
        article = Article.objects.get(id=pk)
    except:
        return redirect('browse-articles')

    context = {'article': article}
    return render(request, 'client/article-detail.html', context)


login_required
def create_stripe_checkout(request, plan_id):
    session = create_checkout_session(request.user, plan_id)
    if session:
        return JsonResponse({'sessionId': session.id})
    return JsonResponse({'error': 'Could not create checkout session'}, status=400)

@login_required(login_url='my-login')
def subscription_success(request):
    session_id = request.GET.get('session_id')
    if session_id:
        return render(request, 'client/subscription-success.html')
    return redirect('subscription-request')

@login_required(login_url='my-login')
def subscription_cancel(request):
    return render(request, 'client/subscription-cancel.html')

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
        if event['type'] == 'checkout.session.completed':
            session = event['data']['object']
            handle_checkout_session(session)
        return HttpResponse(status=200)
    except Exception as e:
        return HttpResponse(status=400)
    

@login_required(login_url='my-login')
def subscription_request(request):
    # ดึง subscription ตัวแรกของ user ที่ยัง active
    active_sub = Subscription.objects.filter(
        user=request.user, 
        status='active'
    ).first()

    if active_sub:
        context = {
            'subscription': active_sub
        }
        return render(request, 'client/subscription-active.html', context)

    # ถ้ายังไม่มี subscription
    context = {
        'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY
    }
    return render(request, 'client/subscription-request.html', context)

@login_required(login_url='my-login')
def donation_request(request):
    return render(request, 'client/donation.html', {
        'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY
    })

@login_required(login_url='my-login')
def create_donation_checkout(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            amount = int(float(data.get('amount', 0)) * 100)  # แปลงเป็นสตางค์

            if amount < 1000:  # น้อยกว่า 10 บาท
                return JsonResponse({'error': 'Minimum amount is 10 THB'}, status=400)

            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                mode='payment',
                line_items=[{
                    'price_data': {
                        'currency': 'thb',
                        'product_data': {
                            'name': 'Custom Donation',
                        },
                        'unit_amount': amount,
                    },
                    'quantity': 1,
                }],
                success_url=settings.SITE_URL + '/client/donation-success/',
                cancel_url=settings.SITE_URL + '/client/donation-cancel/',
                customer_email=request.user.email
            )
            return JsonResponse({'sessionId': session.id})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        
# views.py (ถ้ายังไม่มี)
@login_required(login_url='my-login')
def donation_success(request):
    return render(request, 'client/donation-success.html')

@login_required(login_url='my-login')
def donation_cancel(request):
    return render(request, 'client/donation-cancel.html')






