from this import d
from django.shortcuts import render
from django.views.generic import CreateView, ListView, DeleteView
from .models import Order, Item
from django.shortcuts import  get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
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
  model = Order
  template_name = 'orders/orders_list.html'
  ordering = ['-orderDate']


#CLASS - ORDER DELETE VIEW
class OrderDeleteView(DeleteView):
  model=Order
  template_name = 'orders/orders_delete.html'
  success_url = '/orders_list/'

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