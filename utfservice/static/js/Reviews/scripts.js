$(document).ready(function(){
    if(window.outerWidth >= 550) {
        $(".open-review").toggleAttr("data-bs-toggle", "data-bs-target", "aria-controls")
        $("#offcanvas-review").toggleClass("d-none")

        $(".open-review").on("click", function(){
            // $('#openRate').
            //     .find(".name-platform-card")
            //         .html("")
        })
    }
})