from vantagepoint.settings import BASE_DIR
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.views import View
from django.utils.decorators import method_decorator
from django.core import serializers
# excel parser
import os
import json
import subprocess
import xlrd
from IPy import IP
from subprocess import Popen, PIPE
from datetime import datetime
# models, forms
from api.models import (
    FileDirectory,
    FileViews,
    Shift,
    GeneralComment,
    Incident,
    Role,
    User,
    ShiftHandOver,
)
from api.forms import DocumentForm

path = os.path.dirname(os.path.abspath(BASE_DIR + '/Python Input File.xlsx'))
contents = xlrd.open_workbook(path + '/Python Input File.xlsx')
rows = contents.sheet_by_index(0)

BASE_URL = 'https://rowegiel.pythonanywhere.com'


# class based views
class ShiftView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(ShiftView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        if request.method == 'GET':
            data = []
            shifts = Shift.objects.all()
            if shifts:
                for shift in shifts:
                    data.append({
                        'id': shift.id,
                        'name': shift.name,
                        'time_in': shift.time_in,
                        'time_out': shift.time_out
                    })

                return JsonResponse({'data': data}, status=200)

            return JsonResponse({'error': 'No shift(s) found on your database.'})


class RoleView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(RoleView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        if request.method == 'GET':
            data = []
            roles = Role.objects.all()
            if roles:
                for role in roles:
                    data.append({
                        'id': role.id,
                        'name': role.name,
                        'abbreviation': role.abbreviation
                    })

                return JsonResponse({'data': data}, status=200)

            return JsonResponse({'error': 'No role(s) found on your database.'})


class UserView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(UserView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        if request.method == 'GET':
            data = {};
            pk = request.GET.get('pk', None)
            if pk:
                try:
                    user = User.objects.get(pk=pk)
                    if user:
                        role = Role.objects.get(pk=user.role.id)
                        data = {
                            'id': user.id,
                            'first_name': user.first_name,
                            'last_name': user.last_name,
                            'email': user.email,
                            'role': {
                                'id': role.id,
                                'name': role.name,
                                'abbreviation': role.abbreviation
                            }
                        }
                except User.DoesNotExist:
                    return JsonResponse({'error': 'User not found.'}, status=404)
            else:
                data = []
                users = User.objects.all()
                if users:
                    for user in users:
                        role = Role.objects.get(pk=user.role.id)
                        data.append({
                            'id': user.id,
                            'first_name': user.first_name,
                            'last_name': user.last_name,
                            'email': user.email,
                            'role': {
                                'id': role.id,
                                'name': role.name,
                                'abbreviation': role.abbreviation
                            }
                        })

                    return JsonResponse({'data': data}, status=200)

            return JsonResponse({'error': 'No user(s) found on your database.'}, status=404)


class ShiftHandoverView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(ShiftHandoverView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        incidents = []
        comments = []
        shift_members = []
        if request.method == 'GET':
            pk = request.GET.get('pk', None)
            if pk:
                data = {}
                try:
                    handover = ShiftHandOver.objects.get(pk=int(pk))
                    if handover:
                        shift = Shift.objects.get(pk=handover.shift.id)
                        sender = User.objects.get(pk=handover.sender.id)
                        sender_role = Role.objects.get(pk=sender.role.id)
                        receiver = User.objects.get(pk=handover.receiver.id)
                        receiver_role = Role.objects.get(pk=receiver.role.id)
                        # incidents 
                        for incident in handover.incidents.all():
                            incidents.append({
                                'id': incident.id,
                                'priority': incident.priority,
                                'incident': incident.incident,
                                'description': incident.description,
                                'comment': incident.comment
                            })

                        for comment in handover.comments.all():
                            comments.append({
                                'id': comment.id,
                                'comment': comment.comment
                            })

                        for member in handover.shift_members.all():
                            member_role = Role.objects.get(pk=member.role.id)
                            shift_members.append({
                                'id': member.id,
                                'first_name': member.first_name,
                                'last_name': member.last_name ,
                                'email': member.email,
                                'role': {
                                    'id': member_role.id,
                                    'name': member_role.name,
                                    'abbreviation': member_role.abbreviation
                                }
                            })

                        data = {
                            'id': handover.id,
                            'date': handover.date,
                            'shift': {
                                'id': shift.id,
                                'name': shift.name,
                                'time_in': shift.time_in,
                                'time_out': shift.time_out
                            },
                            'sender': {
                                'id': sender.id,
                                'first_name': sender.first_name,
                                'last_name': sender.last_name ,
                                'email': sender.email,
                                'role': {
                                    'id': sender_role.id,
                                    'name': sender_role.name,
                                    'abbreviation': sender_role.abbreviation
                                }
                            },
                            'receiver': {
                                'id': receiver.id,
                                'first_name': receiver.first_name,
                                'last_name': receiver.last_name,
                                'email': receiver.email,
                                'role': {
                                    'id': receiver_role.id,
                                    'name': receiver_role.name,
                                    'abbreviation': receiver_role.abbreviation
                                }
                            },
                            'incidents': incidents,
                            'comments': comments,
                            'shift_members': shift_members
                        }
                        return JsonResponse({'data': data}, status=200)
                except ShiftHandOver.DoesNotExist:
                    return JsonResponse({'error': 'Shift Handover not found!'}, status=404)
            else:
                data = []
                handovers = ShiftHandOver.objects.all().order_by('-date').order_by('-id')
                if handovers:
                    for handover in handovers:
                        shift = Shift.objects.get(pk=handover.shift.id)
                        sender = User.objects.get(pk=handover.sender.id)
                        sender_role = Role.objects.get(pk=sender.role.id)
                        receiver = User.objects.get(pk=handover.receiver.id)
                        receiver_role = Role.objects.get(pk=receiver.role.id)
                        # incidents 
                        for incident in handover.incidents.all():
                            incidents.append({
                                'id': incident.id,
                                'priority': incident.priority,
                                'incident': incident.incident,
                                'description': incident.description,
                                'comment': incident.comment
                            })

                        for comment in handover.comments.all():
                            comments.append({
                                'id': comment.id,
                                'comment': comment.comment
                            })

                        for member in handover.shift_members.all():
                            member_role = Role.objects.get(pk=member.role.id)
                            shift_members.append({
                                'id': member.id,
                                'first_name': member.first_name,
                                'last_name': member.last_name ,
                                'email': member.email,
                                'role': {
                                    'id': member_role.id,
                                    'name': member_role.name,
                                    'abbreviation': member_role.abbreviation
                                }
                            })

                        data.append({
                            'id': handover.id,
                            'date': handover.date,
                            'shift': {
                                'id': shift.id,
                                'name': shift.name,
                                'time_in': shift.time_in,
                                'time_out': shift.time_out
                            },
                            'sender': {
                                'id': sender.id,
                                'first_name': sender.first_name,
                                'last_name': sender.last_name ,
                                'email': sender.email,
                                'role': {
                                    'id': sender_role.id,
                                    'name': sender_role.name,
                                    'abbreviation': sender_role.abbreviation
                                }
                            },
                            'receiver': {
                                'id': receiver.id,
                                'first_name': receiver.first_name,
                                'last_name': receiver.last_name,
                                'email': receiver.email,
                                'role': {
                                    'id': receiver_role.id,
                                    'name': receiver_role.name,
                                    'abbreviation': receiver_role.abbreviation
                                }
                            },
                            'incidents': incidents,
                            'comments': comments,
                            'shift_members': shift_members
                        })
                    return JsonResponse({'data': data}, status=200)
                return JsonResponse({'error': 'No data found for shift handovers!'}, status=404)

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            data = json.loads(request.body.decode('utf-8'))
            date = data.get('date', None)
            shift_id = data.get('shift_id', None)
            sender_id = data.get('sender_id', None)
            receiver_id = data.get('receiver_id', None)
            shift_members = data.get('shift_members', None)
            incidents = data.get('incidents', None)
            comments = data.get('comments', None)
            # get shift
            shift = Shift.objects.get(pk=int(shift_id))
            # get sender and receiver
            sender = User.objects.get(pk=int(sender_id))
            receiver = User.objects.get(pk=int(receiver_id))
            # save shift handover
            shift_handover = ShiftHandOver()
            shift_handover.date = datetime.strptime(date, "%Y-%m-%d")
            shift_handover.shift = shift
            shift_handover.sender = sender
            shift_handover.receiver = receiver
            shift_handover.save()

            for incident in incidents:
                _incident = Incident.objects.create(
                    priority=incident['priority'],
                    incident=incident['incident'],
                    description=incident['description'],
                    comment=incident['comment']
                )
                shift_handover.incidents.add(_incident)

            for comment in comments:
                g_comment = GeneralComment.objects.create(
                    comment=comment['comment']
                )
                shift_handover.comments.add(g_comment)

            s_members = User.objects.filter(pk__in=shift_members)

            for shift_member in s_members:
                shift_handover.shift_members.add(shift_member)

            shift_handover.save()
            return JsonResponse({
                'message': 'Shift saved'
            })


# html views
def home(request):
    documents = FileDirectory.objects.all()
    return render(request, 'api/home.html', { 'documents': documents })

def index(request):
    return render(request, 'api/report.html', {})

def live_utility(request):
    return render(request, 'api/live_utility.html', {})

def file_upload(request):
    return render(request, 'api/file_upload.html', {})

# logic
@csrf_exempt
def search_file(request):
    retVal = []
    if request.method == 'POST':
        try:
            data_ = json.loads(request.body.decode('utf-8'))
            file_name = data_.get('keyword')
            file_extension = data_.get('extension')
            if file_extension == 'all':
                filter_ = Q(document__icontains=file_name)
            else:
                filter_ = Q(document__icontains=file_extension) &  Q(document__icontains=file_name)
            # check filenames
            result = FileDirectory.objects.filter(filter_)
            for data in result:
                if file_extension == 'all':
                    views = FileViews.objects.get(file=data)
                    name_ = (data.document.name).split('/')
                if data.extension() == file_extension:
                    views = FileViews.objects.get(file=data)
                    name_ = (data.document.name).split('/')

                retVal.append({
                    'file_name': name_[1],
                    'file_url': BASE_URL + '/add-views?file_id=' + str(data.id),
                    'desc': data.description,
                    'number_of_views': views.number_of_views
                })
            return JsonResponse(retVal, status=200, safe=False)
        except FileDirectory.DoesNotExist:
            return JsonResponse({'error': 'File not found!'}, status=404)
    return JsonResponse({'error': 'Something went wrong'}, status=400)

def add_views(request):
    if request.method == 'GET':
        file_id = (request.GET['file_id'])
        try:
            fd = FileDirectory.objects.get(pk=int(file_id))
            fv, created = FileViews.objects.get_or_create(file=fd)
            if created:
                fv.number_of_views = 1
            else:
                fv.number_of_views = fv.number_of_views + 1

            fv.save()
            return redirect(fd.document.url)
        except FileDirectory.DoesNotExist:
            return JsonResponse({'error': 'File not found!'}, status=400)

@csrf_exempt
def upload_file(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        # check if file is valid
        file = request.FILES['document'].name
        size = request.FILES['document'].size
        file = file.replace(' ', '_')
        #check file size
        if size > 2097152:
            return JsonResponse({'message': 'File is too big.'}, status=400)
        # check if file exists
        check_file = FileDirectory.objects.filter(document__icontains=file).exists()
        if check_file:
            return JsonResponse({'message': 'File already exists.'}, status=400)
        #check if form is valid
        if form.is_valid():
            new_file = form.save()
            fd = FileDirectory.objects.get(pk=new_file.pk)
            FileViews.objects.create(**{'file': fd, 'number_of_views': 0})
            return JsonResponse({'message': 'File uploaded successfully!'})
    else:
        form = DocumentForm()

def get_l2vpn_status(request):
    ip = request.GET['ip']
    counter = 0
    retVal = []
    headers = []
    ping_value = None
    for rx in range(rows.nrows):
        content = rows.row(rx)
        content = [ str(element).replace(' ', '') for element in content ]
        if ("text:'DeviceList'" in content):
            ip_col = content.index("text:'DeviceList'")
        if ("text:'L2VPNStatus'" in content):
            l2vpn_col = content.index("text:'L2VPNStatus'")
        try:
            ip_value = str(rows.cell_value(rowx=counter, colx=ip_col))
            if ip_value.strip() == ip.strip():
                l2vpn_status = str(rows.cell_value(rowx=counter, colx=l2vpn_col))
        except Exception as e:
            pass
        counter += 1
    return JsonResponse({'l2vpn_status': l2vpn_status.strip() })

def get_mpbgp_status(request):
    ip = request.GET['ip']
    counter = 0
    retVal = []
    headers = []
    ping_value = None
    for rx in range(rows.nrows):
        content = rows.row(rx)
        content = [ str(element).replace(' ', '') for element in content ]
        if ("text:'DeviceList'" in content):
            ip_col = content.index("text:'DeviceList'")
        if ("text:'MPBGPStatus'" in content):
            mpbgp_col = content.index("text:'MPBGPStatus'")
        try:
            ip_value = str(rows.cell_value(rowx=counter, colx=ip_col))
            if ip_value.strip() == ip.strip():
                mpbgp_status = str(rows.cell_value(rowx=counter, colx=mpbgp_col))
        except Exception as e:
            pass
        counter += 1
    return JsonResponse({'mpbgp_status': mpbgp_status.strip() })

def get_mpls_status(request):
    ip = request.GET['ip']
    counter = 0
    retVal = []
    headers = []
    ping_value = None
    for rx in range(rows.nrows):
        content = rows.row(rx)
        content = [ str(element).replace(' ', '') for element in content ]
        if ("text:'DeviceList'" in content):
            ip_col = content.index("text:'DeviceList'")
        if ("text:'MPLSStatus'" in content):
            mplss_col = content.index("text:'MPLSStatus'")
        try:
            ip_value = str(rows.cell_value(rowx=counter, colx=ip_col))
            if ip_value.strip() == ip.strip():
                mplss_status = str(rows.cell_value(rowx=counter, colx=mplss_col))
        except Exception as e:
            pass
        counter += 1
    return JsonResponse({'mpls_status': mplss_status.strip() })

def get_ospf_status(request):
    ip = request.GET['ip']
    counter = 0
    retVal = []
    headers = []
    ping_value = None
    for rx in range(rows.nrows):
        content = rows.row(rx)
        content = [ str(element).replace(' ', '') for element in content ]
        if ("text:'DeviceList'" in content):
            ip_col = content.index("text:'DeviceList'")
        if ("text:'OSPFstatus'" in content):
            ospf_col = content.index("text:'OSPFstatus'")
        try:
            ip_value = str(rows.cell_value(rowx=counter, colx=ip_col))
            if ip_value.strip() == ip.strip():
                ospf_status = str(rows.cell_value(rowx=counter, colx=ospf_col))
        except Exception as e:
            pass
        counter += 1
    return JsonResponse({'ospf_status': ospf_status.strip() })

def get_uptime_status(request):
    ip = request.GET['ip']
    counter = 0
    retVal = []
    headers = []
    ping_value = None
    for rx in range(rows.nrows):
        content = rows.row(rx)
        content = [ str(element).replace(' ', '') for element in content ]
        if ("text:'DeviceList'" in content):
            ip_col = content.index("text:'DeviceList'")
        if ("text:'Uptime(HH:MM:SS)'" in content):
            uptime_col = content.index("text:'Uptime(HH:MM:SS)'")
        try:
            ip_value = str(rows.cell_value(rowx=counter, colx=ip_col))
            if ip_value.strip() == ip.strip():
                uptime = (rows.cell_value(rowx=counter, colx=uptime_col))
                uptime = xlrd.xldate.xldate_as_datetime(uptime, contents.datemode)
        except Exception as e:
            pass
        counter += 1
    return JsonResponse({'uptime': uptime.strftime("%H:%M:%S") })

def get_cpu_usage(request):
    ip = request.GET['ip']
    counter = 0
    retVal = []
    headers = []
    ping_value = None
    for rx in range(rows.nrows):
        content = rows.row(rx)
        content = [ str(element).replace(' ', '') for element in content ]
        if ("text:'DeviceList'" in content):
            ip_col = content.index("text:'DeviceList'")
        if ("text:'CPUUtilisation(Unitsin%)'" in content):
            cpu_col = content.index("text:'CPUUtilisation(Unitsin%)'")
        try:
            ip_value = str(rows.cell_value(rowx=counter, colx=ip_col))
            if ip_value.strip() == ip.strip():
                cpu_usage = str(rows.cell_value(rowx=counter, colx=cpu_col))
        except Exception as e:
            pass
        counter += 1
    return JsonResponse({'cpu_usage': cpu_usage.strip() })

def get_memory_usage(request):
    ip = request.GET['ip']
    counter = 0
    retVal = []
    headers = []
    ping_value = None
    for rx in range(rows.nrows):
        content = rows.row(rx)
        content = [ str(element).replace(' ', '') for element in content ]
        if ("text:'DeviceList'" in content):
            ip_col = content.index("text:'DeviceList'")
        if ("text:'MemoryUtilisation(Unitsin%)'" in content):
            memory_col = content.index("text:'MemoryUtilisation(Unitsin%)'")
        try:
            ip_value = str(rows.cell_value(rowx=counter, colx=ip_col))
            if ip_value.strip() == ip.strip():
                memory_usage = str(rows.cell_value(rowx=counter, colx=memory_col))
        except Exception as e:
            pass
        counter += 1
    return JsonResponse({'memory_usage': memory_usage.strip() })

def get_ping_status(request):
    ip = request.GET['ip']
    counter = 0
    retVal = []
    headers = []
    ping_value = None
    for rx in range(rows.nrows):
        content = rows.row(rx)
        content = [ str(element).replace(' ', '') for element in content ]
        if ("text:'DeviceList'" in content):
            ip_col = content.index("text:'DeviceList'")
        if ("text:'Ping/Reachability'" in content):
            ping_col = content.index("text:'Ping/Reachability'")

        try:
            ip_value = str(rows.cell_value(rowx=counter, colx=ip_col))
            if ip_value.strip() == ip.strip():
                ping_value = str(rows.cell_value(rowx=counter, colx=ping_col))
        except Exception as e:
            pass
        counter += 1
    return JsonResponse({'ping_status': ping_value.strip() })

def get_all_ip_address(request):
    counter = 0
    retVal = []
    headers = []
    for rx in range(rows.nrows):
        content = rows.row(rx)
        content = [ str(element).replace(' ', '') for element in content ]
        # if ("text:'S.No:'" in content):
        #     serial_col = content.index("text:'S.No:'")
        #     headers.append(str(rows.cell_value(rowx=counter, colx=serial_col)))
        if ("text:'DeviceList'" in content):
            ip_col = content.index("text:'DeviceList'")
            headers.append(str(rows.cell_value(rowx=counter, colx=ip_col)))
        if ("text:'HostName'" in content):
            hostname_col = content.index("text:'HostName'")
            headers.append(str(rows.cell_value(rowx=counter, colx=hostname_col)))
        if ("text:'Ping/Reachability'" in content):
            ping_col = content.index("text:'Ping/Reachability'")
            headers.append(str(rows.cell_value(rowx=counter, colx=ping_col)))
        if ("text:'CPUUtilisation(Unitsin%)'" in content):
            cpu_col = content.index("text:'CPUUtilisation(Unitsin%)'")
            headers.append(str(rows.cell_value(rowx=counter, colx=cpu_col)))
        if ("text:'MemoryUtilisation(Unitsin%)'" in content):
            memory_col = content.index("text:'MemoryUtilisation(Unitsin%)'")
            headers.append(str(rows.cell_value(rowx=counter, colx=memory_col)))
        if ("text:'Uptime(HH:MM:SS)'" in content):
            uptime_col = content.index("text:'Uptime(HH:MM:SS)'")
            headers.append(str(rows.cell_value(rowx=counter, colx=uptime_col)))
        if("text:'OSPFStatus'" in content):
            ospf_col = content.index("text:'OSPFStatus'")
            headers.append(str(rows.cell_value(rowx=counter, colx=ospf_col)))
        if ("text:'MPLSStatus'" in content):
            mplss_col = content.index("text:'MPLSStatus'")
            headers.append(str(rows.cell_value(rowx=counter, colx=mplss_col)))
        if ("text:'MPBGPStatus'" in content):
            mpgbps_col = content.index("text:'MPBGPStatus'")
            headers.append(str(rows.cell_value(rowx=counter, colx=mpgbps_col)))
        if ("text:'L2VPNStatus'" in content):
            l2vpn_col = content.index("text:'L2VPNStatus'")
            headers.append(str(rows.cell_value(rowx=counter, colx=l2vpn_col)))

        try:
            ip_value = str(rows.cell_value(rowx=counter, colx=ip_col))
            ip_address = IP(ip_value)
            hostname_value = str(rows.cell_value(rowx=counter, colx=hostname_col))
            retVal.append({
                'ip_address': str(ip_address),
                'hostname': hostname_value
            })
        except Exception as e:
            pass
        counter += 1
    return JsonResponse({"headers": headers, "values": retVal})

def parse_excel(request):
    counter = 0
    retVal = []
    headers = []
    headers_2 = []
    retVal_2 = []
    mplslinktype_col = None
    mplslinktype_row = None
    mplslinktypestatus_row = None
    for rx in range(rows.nrows):
        table_2 = {}
        content = rows.row(rx)
        content = [ str(element).replace(' ', '') for element in content ]
        if ("text:'S.No:'" in content):
            serial_col = content.index("text:'S.No:'")
            headers.append(str(rows.cell_value(rowx=counter, colx=serial_col)))
        if ("text:'DeviceList'" in content):
            ip_col = content.index("text:'DeviceList'")
            headers.append(str(rows.cell_value(rowx=counter, colx=ip_col)))
        if ("text:'HostName'" in content):
            hostname_col = content.index("text:'HostName'")
            headers.append(str(rows.cell_value(rowx=counter, colx=hostname_col)))
        if ("text:'Ping/Reachability'" in content):
            ping_col = content.index("text:'Ping/Reachability'")
            headers.append(str(rows.cell_value(rowx=counter, colx=ping_col)))
        if ("text:'CPUUtilisation(Unitsin%)'" in content):
            cpu_col = content.index("text:'CPUUtilisation(Unitsin%)'")
            headers.append(str(rows.cell_value(rowx=counter, colx=cpu_col)))
        if ("text:'MemoryUtilisation(Unitsin%)'" in content):
            memory_col = content.index("text:'MemoryUtilisation(Unitsin%)'")
            headers.append(str(rows.cell_value(rowx=counter, colx=memory_col)))
        if ("text:'Uptime(HH:MM:SS)'" in content):
            uptime_col = content.index("text:'Uptime(HH:MM:SS)'")
            headers.append(str(rows.cell_value(rowx=counter, colx=uptime_col)))
        if("text:'OSPFStatus'" in content):
            ospf_col = content.index("text:'OSPFStatus'")
            headers.append(str(rows.cell_value(rowx=counter, colx=ospf_col)))
        if ("text:'MPLSStatus'" in content):
            mplss_col = content.index("text:'MPLSStatus'")
            headers.append(str(rows.cell_value(rowx=counter, colx=mplss_col)))
        if ("text:'MPBGPStatus'" in content):
            mpgbps_col = content.index("text:'MPBGPStatus'")
            headers.append(str(rows.cell_value(rowx=counter, colx=mpgbps_col)))
        if ("text:'L2VPNStatus'" in content):
            l2vpn_col = content.index("text:'L2VPNStatus'")
            headers.append(str(rows.cell_value(rowx=counter, colx=l2vpn_col)))

        # headers_2
        if ("text:'MPLSLinkType'" in content):
            mplslinktype_col = content.index("text:'MPLSLinkType'")
            mplslinktype_row = counter
            headers_2.append(str(rows.cell_value(rowx=counter, colx=mplslinktype_col)).strip())

        if ("text:'Status'" in content):
            mpls_link_type_status_col = content.index("text:'Status'")
            mplslinktypestatus_row = counter
            headers_2.append(str(rows.cell_value(rowx=counter, colx=mpls_link_type_status_col)).strip())

        if mplslinktype_row and counter > mplslinktype_row:
            mplslinktype = str(rows.cell_value(rowx=counter, colx = mplslinktype_col))
            table_2.update({'mplslinktype': mplslinktype.strip()})

        if mplslinktypestatus_row and counter > mplslinktypestatus_row:
            mplslinktype_status = str(rows.cell_value(rowx=counter, colx=mpls_link_type_status_col))
            table_2.update({'status': mplslinktype_status.strip()})

        if table_2:
            retVal_2.append(table_2)

        try:
            serial_value = str(rows.cell_value(rowx=counter, colx=serial_col))
            ip_value = str(rows.cell_value(rowx=counter, colx=ip_col))
            ip_address = IP(ip_value)
            hostname_value = str(rows.cell_value(rowx=counter, colx=hostname_col))
            ping_value = str(rows.cell_value(rowx=counter, colx=ping_col))
            cpu_utilisation = str(rows.cell_value(rowx=counter, colx=cpu_col))
            memory_utilisation = str(rows.cell_value(rowx=counter, colx=memory_col))
            uptime = (rows.cell_value(rowx=counter, colx=uptime_col))
            uptime = xlrd.xldate.xldate_as_datetime(uptime, contents.datemode)
            ospf_status = str(rows.cell_value(rowx=counter, colx=ospf_col))
            mplss_status = str(rows.cell_value(rowx=counter, colx=mplss_col))
            mpgbps_status = str(rows.cell_value(rowx=counter, colx=mpgbps_col))
            l2vpn_status = str(rows.cell_value(rowx=counter, colx=l2vpn_col))

            retVal.append({
                "serial_number": serial_value.strip(),
                "ip_address": str(ip_address),
                "hostname": hostname_value.strip(),
                "ping_status": ping_value.strip(),
                "cpu_utilisation": cpu_utilisation.strip(),
                "memory_utilisation": memory_utilisation.strip(),
                "uptime": uptime.strftime("%H:%M:%S").strip(),
                "ospf_status": ospf_status.strip(),
                "mplss_status": mplss_status.strip(),
                "mpgbps_status": mpgbps_status.strip(),
                "l2vpn_status": l2vpn_status.strip()
            })
        except Exception as e:
            pass
        counter += 1
    return JsonResponse({
        "headers": headers,
        "headers_2": headers_2,
        "values": retVal,
        "values_2": retVal_2
    })
