$(document).ready(function() {

    function toggleDisableAddDelBtn() {
        $(".del-question-btn, #addQuestionBtn, .del-platform-btn, #addPlatformBtn").toggleAttr("disabled")
    }



    function activateDeleteButton() {
        $(".del-question-btn, .del-platform-btn").off("click")

        $(".del-question-btn").on("click", function() {
            question = $(this).parent()

            $("#max3QuestionMes").hide(320)
            question.slideUp(320)

            toggleDisableAddDelBtn()
            setTimeout(function(){ question.remove(); toggleDisableAddDelBtn()  }, 320)
        })

        $(".del-platform-btn").on("click", function() {
            platform = $(this).parent()

            platform.slideUp(320)

            toggleDisableAddDelBtn()
            setTimeout(function(){ platform.remove(); toggleDisableAddDelBtn()  }, 320)
        })
    }

    $("#statusFilial").on("click", function(){
        inputStatus = $(this).parent().find('[name="statusFilial"]')

        if(inputStatus.val() == 2) {
            inputStatus.val(1)
        } else {
            inputStatus.val(2)
        }
    })

    $("#editMainInfoBtn").on("click", function(){
        $("#logotype")
            .toggleAttr("disabled")
            .toggleAttr("readonly")

        $("#statusFilial").toggleAttr("disabled")
        $("#statusFilialLabel").toggleClass("disable")
    })

    $("#statusFilial").on("change", function(){
        if(this.checked) {
            $("#statusFilialLabel")
                .html("Активирован")
                .toggleClass("text-primary text-muted")
        } else {
            $("#statusFilialLabel")
                .html("Невидимый")
                .toggleClass("text-primary text-muted")
        }
    })


    $("#max3QuestionMes").hide()

    activateDeleteButton()


    if(window.outerWidth <= 821)
        $(".btn-sm").toggleClass("btn-sm")



    $("#addQuestionBtn").on("click", function(){
        questions = $("#collapseQuestions>.accordion-body .input-group")

        if(questions.length < 3) {
            $("#collapseQuestions>.accordion-body #max3QuestionMes").before(
                '<div class="question-div input-group mt-3" style="display: none;">\
                    <input class="question-input form-control" type="text" form="saveWidgetForm" placeholder="Заполните поле" name="question" required>\
                    <button class="del-question-btn btn btn-danger" type="button"><i class="bi bi-x"></i></button>\
                 </div>')

            $("#collapseQuestions>.accordion-body .input-group").fadeIn(320)

            activateDeleteButton()
        } else {
            $("#max3QuestionMes").show(320)
        }
    })

    $("#editWidgetCashBackBtn").on("click", function(){
        $('[name="type_charge"]')
            .toggleAttr("disabled")
            .toggleAttr("readonly")

        $(".type-charge-label").toggleClass("btn-outline-secondary btn-outline-primary")

        $('[name="volume_cashback"]')
            .toggleAttr("disabled")
            .toggleAttr("readonly")
    })

    $("#collapseQuestions").on("hidden.bs.collapse", function(){
        $(".question-div").each(function(element) {
            let input = $(this).find("input")

            if(input.val() == "") {
                $("#max3QuestionMes").hide()
                input.parent().remove()
            }
        })
    })

    $("#saveChangesFilialEdit, #saveMainInfoFilialBtn").on("click", function(){
        $("input").removeAttr("readonly disabled")
    })
})