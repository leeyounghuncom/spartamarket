from itertools import product

from django.db import IntegrityError
from django.shortcuts import redirect, render, get_object_or_404
from .models import Product, Comment, Hashtag
from .forms import ProductForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_POST
from django.db.models import Count, Q

import logging
import logging
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from .models import Product, Hashtag
from .forms import ProductForm
from django.shortcuts import render
from django.db.models import Q

from .forms import SearchForm

# 목록
def product_list(request):
    query = request.GET.get('query', '')  # 'query' 파라미터를 받아옴
    sort = request.GET.get('sort', '')  # 'sort' 파라미터를 받아옴

    # 초기 쿼리셋: 모든 제품
    products = Product.objects.all()


    if query:
        products = products.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(author__username__icontains=query) |  # 'user' 대신 'author' 사용
            Q(hashtags__content__icontains=query)
        ).distinct()

    # 정렬 옵션 처리
    if sort == 'likes':
        products = products.annotate(counts=Count('like_users')).order_by('-counts', '-pk')
    else:
        products = products.order_by('-pk')

    return render(request, 'product_list.html', {'products': products})


# 상품추기
@login_required
def create(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.author = request.user
            product.save()
            hashtags = form.cleaned_data['hashtags']
            for tag in hashtags:
                hashtag, created = Hashtag.objects.get_or_create(content=tag)
                product.hashtags.add(hashtag)

            return redirect("products:product_detail", product.pk)
    else:
        form = ProductForm()
    context = {"form": form}
    return render(request, "create.html", context)


# 상세페이지
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    comment_form = CommentForm()
    comments = product.comments.all().order_by("-pk")
    context = {
        "product": product,
        "comment_form": comment_form,
        "comments": comments,
    }
    return render(request, "product_detail.html", context)


# 삭제
@require_POST
def product_delete(request, pk):
    article = get_object_or_404(Product, pk=pk)
    if request.user.is_authenticated:
        if article.author == request.user:
            article = get_object_or_404(Product, pk=pk)
            article.delete()
    return redirect("products:product_list")


@login_required
@require_http_methods(["GET", "POST"])
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            product = form.save(commit=False)
            # 기존 해시태그 제거
            product.hashtags.clear()  # 해시태그 연결 제거

            hashtags = form.cleaned_data['hashtags']
            for tag in hashtags:
                hashtag, created = Hashtag.objects.get_or_create(content=tag)
                product.hashtags.add(hashtag)

            return redirect('products:product_detail', pk=product.pk)
    else:
        form = ProductForm(instance=product)
        

    context = {
        'form': form,
        'product': product,

    }
    return render(request, 'product_update.html', context)


# 댓글 추가
@require_POST
def comment_create(request, pk):
    article = get_object_or_404(Product, pk=pk)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.article = article
        comment.user = request.user
        comment.save()
        return redirect("products:product_detail", article.pk)


# 댓글 삭제
@require_POST
def comment_delete(request, pk, comment_pk):
    if request.user.is_authenticated:
        comment = get_object_or_404(Comment, pk=comment_pk)
        if comment.user == request.user:
            comment.delete()
    return redirect("products:product_detail", pk)


@require_POST
def like_product(request, pk):
    if request.user.is_authenticated:
        product = get_object_or_404(Product, pk=pk)
        if product.like_users.filter(pk=request.user.pk).exists():
            product.like_users.remove(request.user)  # 찜 취소
        else:
            product.like_users.add(request.user)  # 찜 추가
        return redirect('products:product_detail', pk=pk)
    return redirect('accounts:login')


@login_required
def liked_products(request):
    products = request.user.liked_products.all()  # 사용자가 찜한 물건들
    return render(request, 'liked_products.html', {'products': products})
