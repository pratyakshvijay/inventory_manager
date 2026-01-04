from django.urls import path # type: ignore
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),

    path('vendors/', views.vendor_list, name='vendor_list'),
    path('vendors/add/', views.vendor_create, name='vendor_add'),
    path('vendors/edit/<int:pk>/', views.vendor_edit, name='vendor_edit'),
    path('vendor/<int:pk>/delete/', views.vendor_delete, name='vendor_delete'),

    path('lots/', views.fabric_lot_list, name='fabric_lot_list'),
    path('lots/add/', views.fabric_lot_create, name='fabric_lot_add'),
    path('lots/edit/<int:pk>/', views.fabric_lot_edit, name='fabric_lot_edit'),
    path('lots/export/', views.fabric_lot_export_excel, name='fabric_lot_export_excel'),
    path('fabric-lot/<int:pk>/delete/', views.fabric_lot_delete, name='fabric_lot_delete'),

    path('manufacturers/', views.manufacturer_list, name='manufacturer_list'),
    path('manufacturers/add/', views.manufacturer_create, name='manufacturer_add'),
    path('manufacturers/<int:pk>/edit/', views.manufacturer_edit, name='manufacturer_edit'),
    path('manufacturers/<int:pk>/delete/', views.manufacturer_delete, name='manufacturer_delete'),


    path('job-work/issue/add/', views.job_work_issue_create, name='job_work_issue_add'),
    path('job-work/issues/', views.job_work_issue_list, name='job_work_issue_list'),
    path('job-work/issue/<int:pk>/edit/', views.job_work_issue_create, name='job_work_issue_edit'),
    path('job-work/issue/<int:pk>/delete/', views.job_work_issue_delete, name='job_work_issue_delete'),
    path('ajax/get-colors/', views.get_colors_for_lot, name='get_colors_for_lot'),
    path('ajax/get-available-lots/', views.ajax_get_available_lots, name='ajax_get_available_lots'),

]
