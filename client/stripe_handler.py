import stripe
from django.conf import settings
from .models import Subscription

stripe.api_key = settings.STRIPE_SECRET_KEY

def create_checkout_session(user, plan_id):
    price_id = settings.STRIPE_PRICES.get(plan_id)
    if not price_id:
        return None

    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{'price': price_id, 'quantity': 1}],
            mode='subscription',
            success_url=f"{settings.SITE_URL}/client/subscription-success/?session_id={{CHECKOUT_SESSION_ID}}",
            cancel_url=f"{settings.SITE_URL}/client/subscription-cancel/",
            customer_email=user.email,
            metadata={'user_id': user.id, 'plan_id': plan_id}
        )
        return checkout_session
    except stripe.error.StripeError as e:
        print(f"Stripe error: {e}")
        return None

def handle_checkout_session(session):
    user_id = session.metadata.get('user_id')
    plan_id = session.metadata.get('plan_id')
    
    try:
        subscription = stripe.Subscription.retrieve(session.subscription)
        Subscription.objects.create(
            user_id=user_id,
            stripe_subscription_id=subscription.id,
            status=subscription.status,
            plan_id=plan_id,
            current_period_end=subscription.current_period_end
        )
        return True
    except Exception as e:
        print(f"Error handling checkout: {e}")
        return False
    

def create_donation_session(user):
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price': settings.STRIPE_DONATION_PRICE_ID,  # One-time Price ID
                'quantity': 1,
            }],
            mode='payment',
            customer_email=user.email,
            success_url=f"{settings.SITE_URL}/client/donation-success/",
            cancel_url=f"{settings.SITE_URL}/client/donation-cancel/",
        )
        return session
    except Exception as e:
        print(f"Donation error: {e}")
        return None
