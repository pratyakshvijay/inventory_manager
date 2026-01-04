from django.urls import path # type: ignore
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),

    # SKU Management
    path('master-skus/', views.master_skus, name='master_skus'),
    path('add-sku/', views.add_sku, name='add_sku'),
    path('upload-sku-excel/', views.upload_sku_excel, name='upload_sku_excel'),
    path("master-skus/reset-stock/", views.reset_master_stock, name="reset_master_stock"),

    # Inventory
    path('upload-excel/', views.upload_excel, name='upload_excel'),
    path('upload-orders/', views.upload_order_file, name='upload_orders'),
    path('adjust/', views.manual_adjust, name='manual_adjust'),
    path('inventory-history/', views.inventory_history, name='inventory_history'),
    path('low-stock/', views.low_stock_alert, name='low_stock_alert'),
    path('sync-all-flipkart/', views.sync_all_inventory, name='sync_all_inventory'),

    #Bags
    path("bags/add/", views.add_bag, name="add_bag"),
    path("bags/", views.view_bags, name="view_bags"),
    path("bags/delete/<int:pk>/", views.delete_bag, name="delete_bag"),
    path("bags/edit/<int:pk>/", views.edit_bag, name="edit_bag"),

    #Rack
    path("rack/", views.rack_view, name="rack_view"),
    path("rack/upload-excel/", views.upload_rack_excel, name="upload_rack_excel"),
    path("rack/export-excel/", views.export_rack_excel, name="export_rack_excel"),
    path("ajax/rack-stock/", views.ajax_rack_stock, name="ajax_rack_stock"),

    #Progress Bar and Syncing
    path("sync/start/", views.start_inventory_sync, name="start_inventory_sync"),
    path("sync/progress/", views.get_sync_progress, name="get_sync_progress"),
    path("sync-logs/", views.sync_logs_view, name="sync_logs"),
    path("export-sync-logs/", views.export_sync_logs, name="export_sync_logs"),

    # AJAX
    path('ajax/update-stock/', views.update_stock, name='update_stock'),
    path("ajax/sku-search/", views.ajax_sku_search, name="ajax_sku_search"),

    # Flipkart Channel Listings
    path('channel/upload/', views.upload_channel_listing, name='upload_channel_listing'),
    path('channel/mapping/', views.view_channel_listings, name='view_channel_listings'),
    path('channel/bulk-map/', views.bulk_map_channel_skus, name='bulk_map_channel_skus'),
    path('channel/template/', views.download_channel_mapping_template, name='download_channel_mapping_template'),
    path('channel/download-failed/', views.download_failed_channel_mappings, name='download_failed_channel_mappings'),
    path("channel/delete/<int:pk>/", views.delete_channel_listing, name="delete_channel_listing"),
]
