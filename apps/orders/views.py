from django.shortcuts import render
from django.views.generic import CreateView, ListView, DeleteView, RedirectView
from .models import Order, Item
from django.shortcuts import  get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.

# CLASS - ORDER CREATE VIEW#
class OrderCreateView (CreateView):
  model = Order
  fields = ['orderNumber','orderName', 'orderQuantity', 'orderManager','orderNotes']
  template_name = 'orders/orders_create.html'

  def form_valid(self, form):
    form.instance.author = self.request.user
    return super().form_valid(form)

# CLASS - ORDER LIST VIEW#
class OrderListView (ListView):
  model = Order # model to be used
  template_name = 'orders/orders_list.html'
  ordering = ['-orderDate']

#CLASS - ORDER FINISH VIEW#
class OrderFinishView(RedirectView):
  success_url = "/orders_list/" # Redirect user to the list of orders

  def get(self, request, *args, **kwargs):
      order_id = self.kwargs['pk_order']  # pk_order is the name of the argument in the URL
      order = get_object_or_404(Order, pk=order_id) # Get the order object
      order.isDone = True # Set the order to done
      order.save() # Save the order
      messages.success(request, 'POTWIERDZENIE - Zlecenie #{} {} zostało wykonane.'.format(order.orderNumber, order.orderName)) # show a success message
      return redirect(self.success_url) #Redirect to the list of orders

#CLASS - ORDER RESTORE VIEW#
class OrderRestoreView(RedirectView):
  success_url = "/completed_orders_list/" # Redirect user to the list of completed orders

  def get(self, request, *args, **kwargs):
      order_id = self.kwargs['pk_order']  # pk_order is the name of the argument in the URL
      order = get_object_or_404(Order, pk=order_id) # Get the order object
      order.isDone = False # Set the order to not done
      order.save() # Save the order
      messages.warning(
        request,
        f'UWAGA - Zlecenie # {order.orderNumber} {order.orderName} zostało przywrócone do planu cięcia.'
        ) # show a warning message using f-string
      return redirect(self.success_url) #Redirect to the list of completed orders

#CLASS - ORDER DELETE VIEW
class OrderDeleteView(DeleteView):
  model=Order
  template_name = 'orders/orders_delete.html'
  success_url = '/orders_list/'

#CLASS - ITEM LIST VIEW
class ItemListView (ListView):
  model = Item # model to be used
  template_name = 'orders/orders_list.html'
  ordering = ['-orderDate']
  


#HOME VIEW#
@login_required
def home(request):
    context = {
        'title':'Strona startowa programu',
      }
    return render (request,'orders/home.html', context )

# #ORDERS VIEW#
# def orders_list(request):
#     context = {
#         'title':'Lista zleceń',
#       }
#     return render (request,'orders/orders_list.html', context )

#COMPLETED ORDERS VIEW#
class OrderCompletedListView (OrderListView):
  template_name = 'orders/completed_orders_list.html'