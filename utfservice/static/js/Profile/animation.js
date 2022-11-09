function renderAccountFilials(data) {
    let i = 0
    jsonData = JSON.parse(data)

    $("#filials").html("").show()

    // Номер платформы
    $("#filials").append(`<input type="hidden" class="form-check-input" name="filial-platform" value="${$("[name='platformRadio']:checked").val()}" form="includeFilialsForm">`)

    profileAnimation = new Animation()
    profileAnimation.changeVisionSelectors("#chooseProfileMsg", "#chooseProfile")

    $.each(jsonData, function(key, item) {
        if(i == 0)
            $("#nameOrganization").html($("#hiddenNameOrg").val())

        if(item['status'] == 0) {
            $("#filials").append(
                `<label for="filial-${i}" class="checkbox-filials list-group-item list-group-item-action border-0 border-bottom user-select-none">\
                    <div class="row">\
                        <div class="col-1">\
                            <input type="checkbox" class="form-check-input" id="filial-${i}" name="filials" value="${item['id_platform_filial']}" form="includeFilialsForm">\
                        </div>\
                        <label class="form-check-label col-11 ps-lg-0 ps-2" for="filial-${i}">${item['address']}</label>\
                    </div>\
                </label>`
            )
        } else {
            $("#filials").prepend(
                `<div class="list-group-item list-group-item-action disabled border-0 border-bottom" tabindex="-1" aria-disabled="true">\
                    <div class="row">\
                        <span class="col-lg-10 col-9">${item['address']}</span>\
                        <div class="badge rounded-pill bg-light text-muted col-lg-2 col-3 align-self-start">Подключен</div>\
                    </div>\
                </div>`
            )
        }

        i += 1
    });

    $("#addFilials").show()
}


$(document).ready(function(){
    $("#navPlatforms label").on("click", function(){
        $("#navPlatforms label").removeClass("active shadow-sm")
        $(this).toggleClass("active shadow-sm")
    })


    profileAnimation = new Animation()

    $(".platform-radio-label").on("click", function(){
        profileAnimation.changeVisionSelectors(".platform-accounts, #filials, #chooseProfile, #addFilials", "#chooseProfileMsg, .platform-" + $(this).find("input").val())
    })

    $("#chooseProfileMsg, .platform-0").show()


    $("#editAuthDataBtn").on("click", function(){
        $(".auth-data").toggleAttr("readonly")
    })


    $("#editContactDataBtn").on("click", function(){
        $(".contact-data").toggleAttr("readonly")
    })
})