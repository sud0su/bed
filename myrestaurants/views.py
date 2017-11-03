from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView,ListView
from django.views.generic.edit import CreateView
from django.db.models import Count
from models import RestaurantReview, Restaurant, Dish
from forms import RestaurantForm, DishForm


class RestaurantDetail(DetailView):
  model = Restaurant
  template_name = 'myrestaurants/restaurant_detail.html'

  def get_context_data(self, **kwargs):
    context = super(RestaurantDetail, self).get_context_data(**kwargs)
    context['RATING_CHOICES'] = RestaurantReview.RATING_CHOICES
    return context

class RestaurantCreate(CreateView):
  model = Restaurant
  template_name = 'myrestaurants/form.html'
  form_class = RestaurantForm

  def form_valid(self, form):
    form.instance.user = self.request.user
    return super(RestaurantCreate, self).form_valid(form)

class DishCreate(CreateView):
  model = Dish
  template_name = 'myrestaurants/form.html'
  form_class = DishForm

  def form_valid(self, form):
    form.instance.user = self.request.user
    form.instance.restaurant = Restaurant.objects.get(id=self.kwargs['pk'])
    return super(DishCreate, self).form_valid(form)

def review(request, pk):
  restaurant = get_object_or_404(Restaurant, pk=pk)
  review = RestaurantReview(
      rating=request.POST['rating'],
      comment=request.POST['comment'],
      user=request.user,
      restaurant=restaurant)
  review.save()
  return HttpResponseRedirect(reverse('myrestaurants:restaurant_detail', args=(restaurant.id,)))

class TotalData(ListView):
    template_name = 'myrestaurants/dashboard.html'

    def get_queryset(self):
        return Restaurant.objects.all().count

    def get_context_data(self, **kwargs):
        context = super(TotalData, self).get_context_data(**kwargs)
        context['num_resto'] = Restaurant.objects.all().count
        context['num_dish'] = Dish.objects.all().count
        context['num_review'] = RestaurantReview.objects.all().count
        context['num_reviewer'] = RestaurantReview.objects.values('user_id').distinct().count()
        return context
