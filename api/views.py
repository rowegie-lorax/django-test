from django.shortcuts import render
from django.http import JsonResponse

# excel parser
import os
import subprocess
import xlrd
from IPy import IP
from subprocess import Popen, PIPE

path = os.path.dirname(os.path.abspath("/home/rowegiel/Documents/workspace/fernanz/Python Input File.xlsx"))
contents = xlrd.open_workbook(path + '/Python Input File.xlsx')
rows = contents.sheet_by_index(0)

# html views
def index(request):
    return render(request, 'api/report.html', {})

def live_utility(request):
    return render(request, 'api/live_utility.html', {})

# logic
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