$(document).ready(function(){
    if(window.outerWidth <= 830){
        $("#collapseLogData").remove()
        $(".reg-block").before('<li class="nav-item m-2">\
                                    <form id="authorizationUserForm" class="pb-0 mb-0">\
                                        <div class="row collapse collapse-log-data-sm pb-0 mb-4" id="collapseLogData">\
                                            <div class="input-group m-0 p-2">\
                                                <button id="EnterButton" type="submit" class="btn btn-primary input-group-text">\
                                                    <span id="logInSpinner" class="spinner-border spinner-border-sm d-none" role="status" aria-hidden="true"></span>\
                                                    <i class="bi bi-box-arrow-in-right"></i></button>\
                                                <input type="text" placeholder="Логин" name="username" aria-label="Логин" class="form-control">\
                                                <input type="password" placeholder="Пароль" name="password" aria-label="Пароль" class="form-control">\
                                            </div>\
                                            <div class="errorAuthMessage form-text text-danger w-100 fade">Sometext</div>\
                                            <div class="row mt-2">\
                                                <a href="social/login/vk-oauth2" class="btn btn-primary col-3 mx-2 my-1">\
                                                    <i class="fab fa-vk"></i>\
                                                </a>\
                                                <a href="social/login/google-oauth2" class="btn btn-danger col-3 m-1">\
                                                    <i class="bi bi-google"></i>\
                                                </a>\
                                                <a href="social/login/yandex-oauth2" class="btn btn-light col-3 mx-2 my-1">\
                                                    <i class="fab fa-yandex text-danger"></i>\
                                                </a>\
                                            </div>\
                                        </div>\
                                    </form>\
                                </li>')
    } else {
        $('#collapseLogData').on("show.bs.collapse", function(){
            $(".reg-block").css({"padding-left":0})
                $("#RegistrationButton").hide()
        })

        $('#collapseLogData').on("hidden.bs.collapse", function(){
            $("#RegistrationButton").show()
            $(".reg-block").css({"padding-left": 606})
        })
    }

    $("#navbarResponsive").on("show.bs.collapse", function(){
        $("#instrumentsPanelAuthUser").hide()
    })

    $("#navbarResponsive").on("hidden.bs.collapse", function(){
        $("#instrumentsPanelAuthUser").show()
    })
})