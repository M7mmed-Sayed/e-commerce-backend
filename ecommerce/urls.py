"""
URL configuration for ecommerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny


schema_view = get_schema_view(
    openapi.Info(
        title="E Commerce API",
        default_version='v4',
        description="API collection for  E-commerce System",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="mohamedsayed1167@gmail.com",name="Mohamed Sayed",url='https://www.linkedin.com/in/m7mmed-sayed/' ),
        license=openapi.License(name="BSD License",url="https://github.com/M7mmed-Sayed/e-commerce-backend"),

    ),
    public=True,
    permission_classes=(AllowAny,),

)
urlpatterns = [
    # swagger docummentation
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),


    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path("products/", include("products.urls")),
    path("cart/", include("cart.urls")),
    path("payments/", include("payments.urls")),
    path("about/", include("company.urls")),

]
