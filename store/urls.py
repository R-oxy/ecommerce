from django.urls import path

from . import views

urlpatterns = [
	#Leave as empty string for base url
	path('', views.store, name="store"),
	path('login_page/', views.loginPage, name='login_page'),
	path('logout_page/', views.logoutPage, name='logout_page'),
	path('register/', views.registerUser, name='register'),
	path('view_item/', views.ViewItem, name='view_item'),
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),

	path('update-description/', views.UpdateDescription, name="update-description"),
	path('update_item/', views.updateItem, name="update_item"),
	path('process_order/', views.processOrder, name="process_order"),
]