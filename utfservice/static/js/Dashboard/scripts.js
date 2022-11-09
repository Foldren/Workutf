$(document).ready(function() {
    $("#logotype").on("change", function(event){ // превью логотипа
        $("#logotype_preview").attr("src", URL.createObjectURL(event.target.files[0]))
    })


    // $("#updateQR").on("click", function(){ //генерация Qr кода с помощью плагина ClassyQR
    //     QRUrl = $("#qr_url").val()
    //     if(QRUrl) {
    //         $('#qr-preview-image').ClassyQR({
    //             type: 'url',
    // 			url: QRUrl,
    // 			size: 300,
    // 		});

    // 		$("#urlUncorrect").addClass("invisible")
    // 		$(this)
    // 		    .toggleAttr("disabled")
		  //      .addClass("disabled")
    // 		    .html("QR код обновлен")

    // 		qrCodeUrl = $("#qr-preview-image").attr("src")

    // 		$("#downloadQr")
    // 		    .attr("aria-disabled","true")
    // 		    .addClass("disabled")
    // 		$("#qr-image").val(qrCodeUrl)

    //     } else {
    //         $("#urlUncorrect").removeClass("invisible")
    // 	}
    // })

    dashboardRequest = new AjaxRequests()

    windowLocation = String(window.location)

    dashboardRequest.addAjaxEventRequest(
        selectorForm = "#saveWidgetForm",
        actionUrl = windowLocation.replace(window.location.origin, '') + "/save_widget_filial",
        multipleForms = 0,
        operationSuccessConfig = {
            reload: 1,
        }
    )

    $("#mainInfoFilialForm").on("submit", function(event){
        let form = new FormData($(this)[0]) //добавляем форму

        form.set('logotype', $("#logotype").prop('files')[0]) //с помощью методов FormData добавляем или изменяем поля

        $.ajax({
            url: window.location + "/change_main_info_filial",
            method: "post",
            headers: {'X-CSRFTOKEN': $.cookie("csrftoken")},
            data: form,
            processData: false,
            contentType: false,
            success: function(data) {
                location.reload()
            },
        })
    })
})