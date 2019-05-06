from vantagepoint import settings
from django.urls import path
from . import views
from api.views import ShiftHandoverView
from django.conf.urls.static import static

urlpatterns = [
    # HTML views
    path('', views.index, name='index'),
    path('home', views.home, name='home'),
    path('live-utility-check', views.live_utility, name='live_utility'),
    path('upload-docs', views.file_upload, name='file_upload'),
    # Logic
    path('shifthandover', ShiftHandoverView.as_view(), name='add_shifthandover'),
    path('add-views', views.add_views, name='add_views'),
    path('upload-file', views.upload_file, name='upload_file'),
    path('search-file', views.search_file, name='search_file'),
    path('parse', views.parse_excel, name='parse_excel'),
    path('ip-addresses', views.get_all_ip_address, name='get_ip_addresses'),
    path('get-ping-status', views.get_ping_status, name='get_ping_status'),
    path('get-memory-usage', views.get_memory_usage, name='get_memory_usage'),
    path('get-cpu-usage', views.get_cpu_usage, name='get_cpu_usage'),
    path('get-uptime-status', views.get_uptime_status, name='get_cpu_usage'),
    path('get-ospf-status', views.get_ospf_status, name='get_cpu_usage'),
    path('get-mpls-status', views.get_mpls_status, name='get_cpu_usage'),
    path('get-mpbgp-status', views.get_mpbgp_status, name='get_cpu_usage'),
    path('get-l2vpn-status', views.get_l2vpn_status, name='get_cpu_usage'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)