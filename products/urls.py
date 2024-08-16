from django.urls import path
from products import views

app_name = 'products'

urlpatterns = [
    path('', views.product_list, name='product_list'),  # 기본 URL에 대한 뷰 연결
    path("create/", views.create, name="product_create"), #생성
    path("<int:pk>/", views.product_detail, name="product_detail"), #상세페이지
    path("<int:pk>/delete/", views.product_delete, name="product_delete"),
    path("<int:pk>/update/", views.product_update, name="product_update"),


    path("<int:pk>/comments/", views.comment_create, name="comment_create"),
    path(
        "<int:pk>/comments/<int:comment_pk>/delete/",
        views.comment_delete,
        name="comment_delete",
    ),
    path("<int:pk>/like/", views.like_product, name="like_product"),  # 찜 기능 URL

    path('liked/', views.liked_products, name='liked_products'),
]
