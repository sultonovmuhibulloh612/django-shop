from io import BytesIO
from celery import shared_task
import weasyprint
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
from shop.recommender import Recommender 
from orders.models import Order

@shared_task
def payment_completed(order_id):
    """
    Task to send email notification after successful order payment
    and update recommendations.
    """
    try:
        order = Order.objects.get(id=order_id)
        
    
        products = [item.product for item in order.items.all()]
        if products:
            Recommender().products_bought(products)
            print(f"Recommendations updated for order {order_id}")
        
   
        subject = f'My Shop – Invoice no. {order.id}'
        message = 'Please, find attached the invoice for your recent purchase.'
        email = EmailMessage(subject,
                             message,
                             'admin@myshop.com',
                             [order.email])
   
        html = render_to_string('orders/order/pdf.html', {'order': order})
        out = BytesIO()
        stylesheets = [weasyprint.CSS(settings.STATIC_ROOT / 'css/pdf.css')]
        weasyprint.HTML(string=html).write_pdf(out,
                                               stylesheets=stylesheets)
        

        email.attach(f'order_{order.id}.pdf',
                     out.getvalue(),
                     'application/pdf')
        

        email.send()
        print(f"Email sent for order {order_id}")
        
    except Order.DoesNotExist:
        print(f"Order {order_id} not found")
    except Exception as e:
        print(f"Error processing order {order_id}: {e}")