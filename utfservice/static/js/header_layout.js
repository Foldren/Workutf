$(document).ready(function(){

    function toggleSpinnerBtnReg() {
        $("#registrationSpinner").toggleClass("d-none")
        $("#registrationButton").toggleAttr("disabled")
    }

    function toggleSpinnerBtnLogIn(){
        $("#logInSpinner, #EnterButton>i").toggleClass("d-none")
        $("#EnterButton").toggleAttr("disabled")
    }

    function toggleSpinnerBtnLogOut(){
        $('#logOutSpinner, #LogOutButton>i').toggleClass("d-none")
        $("#LogOutButton").toggleAttr("disabled")
    }

    setTimeout(function(){
        $("#authorizationAfterRegSuccess").removeClass('show d-none')
    }, 5000)

    $("#regModalWindowForm").on("submit", function(event){
        event.preventDefault()
        toggleSpinnerBtnReg()

        $.ajax({
            url: window.location.origin+"/reg_new_user",
            method: 'POST',
          	headers: {'X-CSRFTOKEN': $.cookie("csrftoken")},
        	data: $(this).serialize(),
        	success: function(data){
        	    $("#registrationSuccess").toggleClass('d-none show')
        	    $(".navbar-collapse").toggleClass('show')
        	    setTimeout(function(){
                    $("#registrationSuccess").toggleClass('d-none show')
        	    }, 5000)

                let modalReg = $('#modalReg')
                let modal = bootstrap.Modal.getInstance(modalReg)
                modal.toggle()
        	},
        	error: function(xhr){
        	    let exceptText = $(xhr.responseText).find(".exception_value").html() //Возвращаем raise c сервера Django
        	    if(exceptText == 'Данное имя пользователя уже занято' || 'Логин содержит недопустимые символы'){
        	        $("#loginError").html(exceptText)
        	        if($("#loginError").hasClass("invisible"))
        	            $("#loginError").toggleClass("invisible")
        	    }
        	},
        	complete: function(){
                toggleSpinnerBtnReg()
        	},
        })
    })

    $("#authorizationUserForm").on("submit", function(event){
        event.preventDefault()
        toggleSpinnerBtnLogIn()

        $.ajax({
            url: window.location.origin+"/auth_user",
            method: 'POST',
          	headers: {'X-CSRFTOKEN': $.cookie("csrftoken")},
        	data: $(this).serialize(),
        	success: function(data){
        	    if(data == 'You are welcome') {
        	        location.reload()
        	    } else {
            	    $(".errorAuthMessage")
            	        .toggleClass("fade")
            	        .html(data)
        	    }
        	},
        	complete: function(){
        	    toggleSpinnerBtnLogIn()
        	}
        })
    })

    $("#LogOutButton").on("click", function(){
        toggleSpinnerBtnLogOut()

        $.ajax({
            url: window.location.origin+"/log_out_user",
            method: 'POST',
          	headers: {'X-CSRFTOKEN': $.cookie("csrftoken")},
        	data: $(this).serialize(),
        	success: function(data){
        	    if(data = 'You are log out')
        	        location.replace(window.location.origin)
        	},
        	complete: function(){
        	    toggleSpinnerBtnLogOut()
        	}
        })
    })

})