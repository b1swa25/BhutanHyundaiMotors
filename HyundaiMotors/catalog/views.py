from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.db import models
from .models import Part, Category

def part_list(request):
    query = request.GET.get('q')
    category = request.GET.get('category')
    
    parts = Part.objects.all()
    
    if query:
        parts = parts.filter(
            models.Q(name__icontains=query) | 
            models.Q(description__icontains=query) |
            models.Q(category__name__icontains=query)
        )
        
    if category:
        parts = parts.filter(category__name=category)
        
    categories = Category.objects.values_list('name', flat=True).distinct()
    
    return render(request, 'catalog/part_list.html', {
        'parts': parts,
        'categories': categories,
        'selected_category': category,
        'search_query': query
    })

class PartDetailView(DetailView):
    model = Part
    template_name = 'catalog/part_detail.html'

class PartCreateView(LoginRequiredMixin, CreateView):
    model = Part
    fields = ['name', 'category', 'description', 'price', 'stock', 'image']
    template_name = 'catalog/part_form.html'
    success_url = reverse_lazy('part_list')

    def form_valid(self, form):
        form.instance.added_by = self.request.user
        return super().form_valid(form)

class PartUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Part
    fields = ['name', 'category', 'description', 'price', 'stock', 'image']
    template_name = 'catalog/part_form.html'
    success_url = reverse_lazy('part_list')

    def test_func(self):
        part = self.get_object()
        return self.request.user == part.added_by or self.request.user.role == 'ADMIN'

class PartDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Part
    template_name = 'catalog/part_confirm_delete.html'
    success_url = reverse_lazy('part_list')

    def test_func(self):
        part = self.get_object()
        return self.request.user == part.added_by or self.request.user.role == 'ADMIN'
