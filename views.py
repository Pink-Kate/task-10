from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Quote, Author, Tag
from .forms import QuoteForm, AuthorForm, TagForm

def home(request):
    quotes = Quote.objects.all()
    
    # Пошук
    query = request.GET.get('q')
    if query:
        quotes = quotes.filter(
            Q(text__icontains=query) |
            Q(author__name__icontains=query) |
            Q(tags__name__icontains=query)
        ).distinct()
    
    # Пагінація
    paginator = Paginator(quotes, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Статистика
    from .models import Author, Tag
    authors_count = Author.objects.count()
    tags_count = Tag.objects.count()
    
    context = {
        'page_obj': page_obj,
        'query': query,
        'authors_count': authors_count,
        'tags_count': tags_count,
    }
    return render(request, 'quotes/home.html', context)

def quote_detail(request, pk):
    quote = get_object_or_404(Quote, pk=pk)
    return render(request, 'quotes/quote_detail.html', {'quote': quote})

def author_list(request):
    authors = Author.objects.all()
    return render(request, 'quotes/author_list.html', {'authors': authors})

def author_detail(request, pk):
    author = get_object_or_404(Author, pk=pk)
    quotes = author.quotes.all()
    return render(request, 'quotes/author_detail.html', {
        'author': author,
        'quotes': quotes
    })

def tag_list(request):
    tags = Tag.objects.all()
    return render(request, 'quotes/tag_list.html', {'tags': tags})

def tag_detail(request, pk):
    tag = get_object_or_404(Tag, pk=pk)
    quotes = tag.quote_set.all()
    return render(request, 'quotes/tag_detail.html', {
        'tag': tag,
        'quotes': quotes
    })

@login_required
def add_author(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            author = form.save(commit=False)
            author.created_by = request.user
            author.save()
            messages.success(request, 'Автора додано успішно!')
            return redirect('quotes:author_detail', pk=author.pk)
    else:
        form = AuthorForm()
    
    return render(request, 'quotes/author_form.html', {'form': form, 'title': 'Додати автора'})

@login_required
def add_quote(request):
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            quote = form.save(commit=False)
            quote.created_by = request.user
            quote.save()
            form.save_m2m()  # Зберігаємо many-to-many зв'язки
            messages.success(request, 'Цитату додано успішно!')
            return redirect('quotes:quote_detail', pk=quote.pk)
    else:
        form = QuoteForm()
    
    return render(request, 'quotes/quote_form.html', {'form': form, 'title': 'Додати цитату'})

@login_required
def add_tag(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            tag = form.save()
            messages.success(request, 'Тег додано успішно!')
            return redirect('quotes:tag_detail', pk=tag.pk)
    else:
        form = TagForm()
    
    return render(request, 'quotes/tag_form.html', {'form': form, 'title': 'Додати тег'}) 