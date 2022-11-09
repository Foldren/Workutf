$(document).ready(function(){
    if(window.outerWidth >= 550) {
        $(".open-review").toggleAttr("data-bs-toggle", "data-bs-target", "aria-controls")
        $("#offcanvas-review").toggleClass("d-none")
        $("#filialRates .offcanvas-body").empty()
    } else {
        $(".open-review").removeClass("btn-sm")
        $("#openRate").remove()
    }

    $(".open-review").on("click", function(){
        reviewObject = $(this).parents(".review-object")
        platformSrcImg = reviewObject.find("img").attr("src")
        platform = $("#platform").val()
        namePlatform = ""
        reviewContent = reviewObject.find(".reviewText").html()
        srcPhotoProfile = reviewObject.attr("data-prof-photo")
        dateReview = reviewObject.attr("data-full-datetime")
        authorName = reviewObject.attr("data-auth-name")
        addressFilial = $("#addressFilialInpt").val()
        urlRate = reviewObject.attr("data-rate-url")

        $("#openRate>.rate-open").removeClass("d-none")
        $("#noChooseReviews")
            .removeClass("d-none")
            .addClass("d-none")
        $(".rate-platform-img").attr("src", platformSrcImg)

        if(platform == 0){
            namePlatform = "Yandex"
        } else if(platform == 1){
            namePlatform = "2GIS"
        } else if(platform == 2) {
            namePlatform = "Google"
        }

        $("#openRate #name-platform-card").html(namePlatform)
        $("#contentReview").html(reviewContent)


        $("#photo-profile-card").attr("src", srcPhotoProfile)

        $("#addressFilial").html(addressFilial)

        starsHtml = reviewObject.find(".filial-rate-star").clone()
        starsHtml.find("span").remove()

        $("#starRate").html(starsHtml)

        let date = new Date(dateReview);

        dateStr = date.getDate() + "." + (date.getMonth()+1) + "." + date.getFullYear()
        $("#dateReview").html(dateStr)

        timeStr = date.getHours() + ":" + date.getMinutes()
        $("#timeReview").html(timeStr)

        $("#authorName").html(authorName)

        $("#urlRate").attr("href", urlRate)
    })
})