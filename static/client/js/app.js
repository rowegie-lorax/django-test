$(document).ready(function(){
    $("#downloadAsPdf").on('click', function(e){
        var doc = new jsPDF('l', 'mm');
        doc.autoTable({
            html: '#reportTable',
            useCss: true,
            styles: {
                cellWidth: 20,
            },
        });
        var finalY = doc.previousAutoTable.finalY;

        let pageNumber = doc.internal.getNumberOfPages();

        doc.autoTable({
            startY: finalY + 45,
            html: '#reportTable_2',
            useCss: true,
            showHead: 'firstPage',
            styles: {overflow: 'hidden'},
            margin: {right: 150}
        });
    
        doc.setPage(pageNumber);

        doc.autoTable({
            head: [['User comments']],
            body: [[$("#userComments").val()]],
            startY: finalY + 95,
            showHead: 'firstPage',
            styles: {overflow: 'hidden'},
            margin: {left: 150}
        });
        // var lastTableY = doc.previousAutoTable.finalY;
        doc.addPage();
        let y = doc.autoTable.previous.finalY; // The y position on the page
        doc.text(20, y, "Charts")
        var promise = new Promise(function(resolve){
            html2canvas($('#charts'), {
                background: "#ffffff",
                onrendered: function(canvas) {
                    var myImage = canvas.toDataURL("image/jpeg,1.0");
                    resolve(myImage);
                }   
            });
        });
        Promise.all([promise]).then(function(values){
            // var x = 15; 
            var y = 40;
            for (var i=0; i<values.length;i++){
                if (i > 0 && i % 2 == 0){
                    doc.addPage();
                    doc.text(20, 20, "Charts")
                    y = 40;
                }
                doc.addImage(values[i], 'JPEG', 55, y, 220, 120)
                y += 80;
            }
            doc.save('Daily Network Healthreport.pdf');
        })
    })  

    $("#generateReport").on('click', function(e){
        e.preventDefault();
        $.ajax({
            url: 'http://127.0.0.1:8000/parse',
            type: 'GET',
            success: function (data) {
                $("#reportTable").removeAttr("style");
                $("#reportTable_2").removeAttr("style");
                var chart_data = [];
                var headers = data.headers;
                var values = data.values;
                var headers_2 = data.headers_2;
                var values_2 =  data.values_2;
                /* Table 1*/
                for (var i=0; i<headers.length; i++){
                    $("#header").append("<th scope='col' style='text-align: center'>" + headers[i]);
                }
                ping_status = "";
                
                memory_labels = []
                var chart_values = {
                    'cpu': [],
                    'memory': []
                };
                for (var i=0; i<values.length; i++){
                    ping_status = "<td scope='row' style='text-align: center'>" +values[i].ping_status+ "</th>"
                    cpu = "<td scope='row' style='text-align: center'>" +values[i].cpu_utilisation+ "%</th>"
                    memory = "<td scope='row' style='text-align: center'>" +values[i].memory_utilisation+ "%</th>"
                    ospf = "<td scope='row' style='text-align: center'>" +values[i].ospf_status+ "</th>"
                    mplss = "<td scope='row' style='text-align: center'>" +values[i].mplss_status+ "</th>"
                    mpgbps = "<td scope='row' style='text-align: center'>" +values[i].mpgbps_status+ "</th>"
                    l2vpn = "<td scope='row' style='text-align: center'>" +values[i].l2vpn_status+ "</th>"

                    if (values[i].ospf_status == "DOWN")
                        ospf = "<td scope='row' style='text-align: center; color:red;'>" +values[i].ospf_status+ "</th>"
                    if (values[i].mplss_status == 'DOWN')
                        mplss = "<td scope='row' style='text-align: center; color:red;'>" +values[i].mplss_status+ "</th>"
                    if (values[i].mpgbps_status == "DOWN")
                        mpgbps = "<td scope='row' style='text-align: center; color:red;'>" +values[i].mpgbps_status+ "</th>"
                    if (values[i].l2vpn_status == "DOWN")
                        l2vpn = "<td scope='row' style='text-align: center; color:red;'>" +values[i].l2vpn_status+ "</th>"

                    if (parseInt(values[i].cpu_utilisation) > 59){
                        chart_values.cpu.push({
                            'ip_address': values[i].ip_address,
                            'cpu': parseFloat(values[i].cpu_utilisation)
                        })

                        cpu = "<td scope='row' style='text-align: center; color:red;'>" +values[i].cpu_utilisation+ "%</th>"
                    }

                    if (parseInt(values[i].memory_utilisation) > 59){
                        chart_values.memory.push({
                            'ip_address': values[i].ip_address,
                            'memory': parseFloat(values[i].memory_utilisation)
                        })
                        memory = "<td scope='row' style='text-align: center;color:red;'>" +values[i].memory_utilisation+ "%</th>"
                    }

                    if (values[i].ping_status == 'Not Reachable'){
                        ping_status = "<td scope='row' style='text-align: center;color:red;'>" 
                            +values[i].ping_status+ "</th>"
                    }

                    $("#values").append(
                        "<tr>"
                        + "<th scope='row' style='text-align: center'>" +values[i].serial_number+ "</th>"
                        + "<td scope='row' style='text-align: center'>" +values[i].ip_address+ "</th>"
                        + "<td scope='row' style='text-align: center'>" +values[i].hostname+ "</th>"
                        + ping_status
                        + cpu
                        + memory
                        + "<td scope='row' style='text-align: center'>" +values[i].uptime+ "</th>"
                        + ospf
                        + mplss
                        + mpgbps
                        + l2vpn
                        +"<tr>"
                    )
                }
                /* Table 2 */
                for (var i=0; i<headers_2.length; i++){
                    $("#header_2").append("<th scope='col' style='text-align: center'>" + headers_2[i]);
                }
                status = "<td scope='row' style='text-align: center'>" +values_2[i].status+ "</th>";

                if (values_2[i].status == "DOWN"){
                    status = "<td scope='row' style='text-align: center; color:red;'>" +values_2[i].status+ "</th>";
                }
                for (var i=0; i<values_2.length; i++){
                    $("#values_2").append(
                        "<tr>"
                        + "<th scope='row' style='text-align: center'>" +values_2[i].mplslinktype+ "</th>"
                        + status
                        +"<tr>"
                    )
                }
                if ('cpu' in chart_values){
                    var cpu_labels = []
                    var cpu_data = []
                    var chart_el = document.createElement('canvas')
                    var cpu_val = chart_values.cpu
                    chart_el.setAttribute('id', 'cpuChart');
                    chart_el.setAttribute("width", 400);
                    chart_el.setAttribute("height", 400);
                    bgColor = []
                    bdColor = []
                    for (var i=0; i<cpu_val.length; i++){
                        cpu_labels.push(cpu_val[i].ip_address)
                        cpu_data.push(cpu_val[i].cpu)
                        bgColor.push('rgba(207, 0, 15, 1)')
                        bdColor.push('rgba(207, 0, 15, 1)')
                    }   
                    $("#charts").append(
                        "<div class='col' style='text-align: : center;' id='cpu_utilisation'>"
                        + "CPU Utilization</div>"
                    )
                    $("#cpu_utilisation").append(chart_el);
                    var ctx = document.getElementById('cpuChart');
                    var myChart = new Chart(ctx, {
                        type: 'bar',
                        data: {
                            labels: cpu_labels,
                            datasets: [{
                                label: 'Utilization',
                                data: cpu_data,
                                backgroundColor: bgColor,
                                borderColor: bdColor,
                                borderWidth: 1
                            }]
                        },
                        options: {
                            responsive: false,
                            scales: {
                                xAxes: [{   
                                    ticks: {
                                        maxRotation: 90,
                                        minRotation: 80
                                    }
                                }],
                                yAxes: [{
                                    ticks: {
                                        beginAtZero: true
                                    }
                                }]
                            }
                        }
                    });
                }
                if ('memory' in chart_values){
                    var memory_labels = [];
                    var memory_data = [];
                    var chart_el = document.createElement('canvas')
                    var memory_val = chart_values.memory
                    chart_el.setAttribute('id', 'memoryChart');
                    chart_el.setAttribute("width", 400);
                    chart_el.setAttribute("height", 400);
                    bgColor = []
                    bdColor = []
                    for (var i=0; i<memory_val.length; i++){
                        memory_labels.push(memory_val[i].ip_address)
                        memory_data.push(memory_val[i].memory)
                        bgColor.push('rgba(207, 0, 15, 1)')
                        bdColor.push('rgba(207, 0, 15, 1)')
                    }
                    $("#charts").append(
                        "<div class='col' style='text-align: : center;' id='memory_utilisation'>"
                        + "Memory Utilization</div>"
                    )
                    $("#memory_utilisation").append(chart_el);
                    var ctx = document.getElementById('memoryChart');
                    var myChart = new Chart(ctx, {
                        type: 'bar',
                        data: {
                            labels: memory_labels,
                            datasets: [{
                                label: 'Utilization',
                                data: memory_data,
                                backgroundColor: bgColor,
                                borderColor: bdColor,
                                borderWidth: 1
                            }]
                        },
                        options: {
                            responsive: false,
                            scales: {
                                xAxes: [{   
                                    ticks: {
                                        maxRotation: 90,
                                        minRotation: 80
                                    }
                                }],
                                yAxes: [{
                                    ticks: {
                                        beginAtZero: true
                                    }
                                }]
                            }
                        }
                    });
                }
            },
            error: function (err) {}
        });
    })

    $("#liveUtilityReport").on('click', function(e){
        e.preventDefault();
        $.ajax({
            url: 'http://127.0.0.1:8000/ip-addresses',
            type: 'GET',
            success: function (data) {
                $("#utilityTable").removeAttr("style");
                var headers = data.headers;
                var values = data.values;
                for (var i=0; i<headers.length; i++){
                    $("#utilityHeader").append("<th scope='col' style='text-align: center'>" + headers[i]);
                }
                for (var i=0; i<values.length; i++){
                    $("#utilityValues").append(
                        "<tr>"
                        + "<th scope='row' style='text-align: center'>" + values[i].ip_address + "</th>"
                        + "<th scope='row' style='text-align: center'>" + values[i].hostname + "</th>"
                        + "<td scope='row' style='text-align: center'>"
                        + "<button type='button' class='btn btn-secondary' onClick='getPingStatus(this, \"" + values[i].ip_address + "\")'>Ping Status</button></td>"
                        + "<td scope='row' style='text-align: center'>"
                        + "<button type='button' class='btn btn-secondary' onClick='getCpuUsage(this, \"" + values[i].ip_address + "\")'>CPU <br> Usage</button></td>"
                        + "<td scope='row' style='text-align: center'>"
                        + "<button type='button' class='btn btn-secondary' onClick='getMemoryUsage(this, \"" + values[i].ip_address + "\")'>Memory <br> Usage</button></td>"
                        + "<td scope='row' style='text-align: center'>"
                        + "<button type='button' class='btn btn-secondary' onClick='getUptimeStatus(this, \"" + values[i].ip_address + "\")'>Uptime Status</button></td>"
                        + "<td scope='row' style='text-align: center'>"
                        + "<button type='button' class='btn btn-secondary' onClick='getOspfStatus(this, \"" + values[i].ip_address + "\")'>OSPF Status</button></td>"
                        + "<td scope='row' style='text-align: center'>"
                        + "<button type='button' class='btn btn-secondary' onClick='getMplsStatus(this, \"" + values[i].ip_address + "\")'>MPLS Status</button></td>"
                        + "<td scope='row' style='text-align: center'>"
                        + "<button type='button' class='btn btn-secondary' onClick='getMpbgpStatus(this, \"" + values[i].ip_address + "\")'>MPBGP Status</button></td>"
                        + "<td scope='row' style='text-align: center'>"
                        + "<button type='button' class='btn btn-secondary' onClick='getL2vpnStatus(this, \"" + values[i].ip_address + "\")'>L2VPN Status</button></td>"
                        +"<tr>"
                    )
                }
            },
            error: function (err) {}
        })
    })
});
function getPingStatus(elm, ip){
    $.ajax({
        url: 'http://127.0.0.1:8000/get-ping-status',
        type: 'GET',
        data: {'ip': ip},
        success: function(data){
            if ($(elm).text() == 'Ping Status'){
                if (data.ping_status == 'Reachable'){
                    $(elm).text(data.ping_status).toggleClass('btn-success');
                }else if(data.ping_status == 'Not Reachable'){
                    $(elm).text(data.ping_status).toggleClass('btn-warning');
                }
            }
        },
        error: function(data){

        }   
    })
}
function getMemoryUsage(elm, ip){
    $.ajax({
        url: 'http://127.0.0.1:8000/get-memory-usage',
        type: 'GET',
        data: {'ip': ip},
        success: function(data){
            if ($(elm).text() == 'Memory  Usage'){
                if (data.memory_usage)
                    $(elm).text(data.memory_usage).toggleClass('btn-success');
            }
        },
        error: function(data){

        }
    })
}
function getCpuUsage(elm, ip){
    $.ajax({
        url: 'http://127.0.0.1:8000/get-cpu-usage',
        type: 'GET',
        data: {'ip': ip},
        success: function(data){
            if ($(elm).text() == 'CPU  Usage'){
                if (data.cpu_usage){
                    $(elm).text(data.cpu_usage).toggleClass('btn-success');
                }
            }
        },
        error: function(data){

        }
    })
}
function getUptimeStatus(elm, ip){
    $.ajax({
        url: 'http://127.0.0.1:8000/get-uptime-status',
        type: 'GET',
        data: {'ip': ip},
        success: function(data){
            if ($(elm).text() == 'Uptime Status'){
                if (data.uptime){
                    $(elm).text(data.uptime).toggleClass('btn-success');
                }
            }
        },
        error: function(data){

        }
    })
}
function getOspfStatus(elm, ip){
    $.ajax({
        url: 'http://127.0.0.1:8000/get-ospf-status',
        type: 'GET',
        data: {'ip': ip},
        success: function(data){
            if ($(elm).text() == 'OSPF Status'){
                if (data.ospf_status == 'UP'){
                    $(elm).text(data.ospf_status).toggleClass('btn-success');
                }else if (data.ospf_status == 'DOWN'){
                    $(elm).text(data.ospf_status).toggleClass('btn-danger');
                }
            }
        },
        error: function(data){}
    })
}
function getMplsStatus(elm, ip){
    $.ajax({
        url: 'http://127.0.0.1:8000/get-mpls-status',
        type: 'GET',
        data: {'ip': ip},
        success: function(data){
            if ($(elm).text() == 'MPLS Status'){
                if (data.mpls_status == 'UP'){
                    $(elm).text(data.mpls_status).toggleClass('btn-success');
                }else if (data.mpls_status == 'DOWN'){
                    $(elm).text(data.mpls_status).toggleClass('btn-danger');
                }
            }
        },
        error: function(data){

        }
    })
}
function getMpbgpStatus(elm, ip){
    $.ajax({
        url: 'http://127.0.0.1:8000/get-mpbgp-status',
        type: 'GET',
        data: {'ip': ip},
        success: function(data){
            if ($(elm).text() == 'MPBGP Status'){
                if (data.mpbgp_status == 'UP'){
                    $(elm).text(data.mpbgp_status).toggleClass('btn-success');
                }else if (data.mpbgp_status == 'DOWN'){
                    $(elm).text(data.mpbgp_status).toggleClass('btn-danger');
                } 
            }
        },
        error: function(data){

        }
    })
}
function getL2vpnStatus(elm, ip){
    $.ajax({
        url: 'http://127.0.0.1:8000/get-l2vpn-status',
        type: 'GET',
        data: {'ip': ip},
        success: function(data){
            if ($(elm).text() == 'L2VPN Status'){
                if (data.l2vpn_status == 'UP'){
                    $(elm).text(data.l2vpn_status).toggleClass('btn-success');
                }else if (data.l2vpn_status == 'DOWN'){
                    $(elm).text(data.l2vpn_status).toggleClass('btn-danger');
                }
            }
        },
        error: function(data){

        }
    })
}

