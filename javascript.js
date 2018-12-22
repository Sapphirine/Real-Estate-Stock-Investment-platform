var msg = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
function predict(msg) {
    axios({
        url: "http://104.196.173.137:8000",
        method: 'post',
        data: {
            "Building_Qualit": [msg[0]],
            "Basement_Area": [msg[1]],
            "Year_Built": [msg[2]],
            "Room_Count": [msg[3]],
            "Total_BsmtS": [msg[4]],
            "Total_Area": [msg[5]],
            "Lot_Area": [msg[6]],
            "Garage_Area": [msg[7]],
            "Pool_Area": [msg[8]],
            "Full_Bath": [msg[9]],
            "Half_Bath": [msg[10]],
            "Garage_Cars": [msg[11]],
            "Fire_Places": [msg[12]],
            "1st_Floor_Square_Feet": [msg[13]]
        },
    }).then(response => {
        console.log(response);
        $('.out').remove()
        addoutput(response['data'])
    } ).catch(error => {
        console.log(error)
    })
}

function addoutput(message) {
    var m = message.split(',')
    var outp = $(".outp")
    var d1 = $("<div class = 'out'> Price:"+ m[0] + "</div>");
    var d2 = $("<div class = 'out'> Deviation:" + m[1] + "</div>");
    outp.append(d1);
    outp.append(d2);
}

function send() {
    msg[0] = $("#msg0").val();
    msg[1] = $("#msg1").val();
    msg[2] = $("#msg2").val();
    msg[3] = $("#msg3").val();
    msg[4] = $("#msg4").val();
    msg[5] = $("#msg5").val();
    msg[6] = $("#msg6").val();
    msg[7] = $("#msg7").val();
    msg[8] = $("#msg8").val();
    msg[9] = $("#msg9").val();
    msg[10] = $("#msg10").val();
    msg[11] = $("#msg11").val();
    msg[12] = $("#msg12").val();
    msg[13] = $("#msg13").val();
    msg[14] = $("#msg14").val();
    predict(msg);
    $(".input-field").val(null);
}

$(".msg").keydown(function () {
    if (event.keyCode == "13") {
        send();
        $(".msg").val(null);
    }
});
function clik() {
    document.getElementById("modal01").style.display = 'none';
}
