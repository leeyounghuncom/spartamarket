from django.shortcuts import redirect, render, get_object_or_404
from .models import Product, Comment
from .forms import ProductForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_POST
from django.contrib.auth import get_user_model

#목록
def product_list(request):
    # articles = Product.objects.all().order_by("-pk")
    # context = {
    #     "articles": articles,
    # }
    # return render(request, "articles/articles.html", context)
    products = Product.objects.all().order_by("-pk")
    return render(request, 'product_list.html', {'products': products})

#상품추기
@login_required
def create(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            return redirect("products:product_detail", article.pk)
    else:
        form = ProductForm()

    context = {"form": form}
    return render(request, "create.html", context)

#상세페이지
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

#삭제
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
            form.save()
            return redirect('products:product_detail', pk=product.pk)
    else:
        form = ProductForm(instance=product)

    context = {
        'form': form,
        'product': product,
    }
    return render(request, 'product_update.html', context)


#댓글 추가
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

#댓글 삭제
@require_POST
def comment_delete(request, pk, comment_pk):
    if request.user.is_authenticated:
        comment = get_object_or_404(Comment, pk=comment_pk)
        if comment.user == request.user:
            comment.delete()
    return redirect("products:product_detail", pk)


@require_POST
def like(request, pk):
    if request.user.is_authenticated:
        product = get_object_or_404(Product, pk=pk)
        if product.like_users.filter(pk=request.user.pk).exists():
            product.like_users.remove(request.user)  # 좋아요 취소
        else:
            product.like_users.add(request.user)  # 좋아요
        return redirect('products:product_detail', pk=pk)  # pk 인자를 함께 전달
    return redirect('accounts:login')
