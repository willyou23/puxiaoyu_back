from django.urls import path
from . import views
# from .views import AliBack
# from .views import AlipayRedirect

urlpatterns = [
    path('page/', views.AlipayPageTrade.as_view(), name='purchase'),
    path('page2/', views.AlipayRedirect.as_view()),
    # path('page1/', views.getBalance.as_view()),
    # path('ali_back/', AliBack.as_view())
    # path('page2/', AlipayRedirect.as_view())
]