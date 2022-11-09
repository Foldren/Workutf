$(document).ready(function() {
    if(window.outerWidth <= 830){
        $(".btn-sm").toggleClass("btn-sm")
    }

    $('.status-class').on("click", function(){
        $("#"+$(this).attr("form")).submit()

        inputStatus = $(this).parent().find('[name="statusFilial"]')

        if(inputStatus.val() == 2) {
            inputStatus.val(1)
        } else {
            inputStatus.val(2)
        }
    })

    $(".status-filial").on("change", function(event){
        if(event.target.checked) {
            $(`[for='${event.target.id}']`)
                .html("Активирован")
                .toggleClass("text-primary text-muted")
        } else {
            $(`[for='${event.target.id}']`)
                .html("Невидимый")
                .toggleClass("text-primary text-muted")
        }
    })
})