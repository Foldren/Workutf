$(document).ready(function(){
    function getActiveLabel(){
        return $("#mainCard7 .btn-group input:checked").attr("id")
    }

    function changeBgTxtColorTariffBlock(tarifBlockSel){
        $(tarifBlockSel)
            .toggleClass("bg-primary text-white")
            .find(".getTariff")
                .toggleClass("btn-outline-primary btn-dark")
            .end()
            .find('.for-range')
                .toggleClass("text-dark text-white")
            .end()
            .find(".range-btn")
                .toggleClass("btn-primary btn-light")
            .end()
            .find(".unner-tarif-block")
                .toggleClass("bg-primary bg-white text-dark text-white")
            .end()
            .find(".details-tariff span, p:eq(0), p:eq(1), select")
                .toggleClass("text-dark text-white");

        return tarifBlockSel
    }

    function getEndLabelFilial(valLastNumber){
        if((valLastNumber >= 5 && valLastNumber <= 9) || valLastNumber == 0) {
            return " филиалов"
        } else if(valLastNumber == 1) {
            return " филиал"
        } else if(valLastNumber >= 2 && valLastNumber <= 4) {
            return " филиала"
        }
    }

    $("#mainCard7 .btn-group label").on("click", function(){
        activeTariffBlock = $(this).attr("data-tariff-class")

        changeBgTxtColorTariffBlock($(".tarif-block.bg-primary"))
        changeBgTxtColorTariffBlock(activeTariffBlock)

        $(this).addClass("text-white")
            .removeClass("text-dark")
            .addClass("bg-primary")

        $(".btn-group label").not($(this))
            .addClass("text-dark")
            .removeClass("text-white bg-primary")
    })

    $("#mainCard7 .btn-group label").hover(function(){
        $(this).toggleClass("text-dark")
    })

    $("[type='range']").on("mousemove touchmove", function() {
        labelRangeLine = $("[for="+$(this).attr("id")+"]")
        rangeValue= $(this).val()

        valLastNumber = parseInt(rangeValue.substr(-1))
        labelRangeLine.html(rangeValue + getEndLabelFilial(valLastNumber))

        $(this).change()
    })

    $("[type='range']").on("change", function() {
        thisBlockPrice = $(this).parents(".tarif-block").find(".price")
        thisBlockPriceVal = $("#" + $(this).attr("data-price-id")).html()
        thisBlockAfterPrice = $('.after-price-info[data-price-id="' + $(this).attr("data-price-id") + '"]')
        rangeVal10 = $(this).val() / 10

        if((rangeVal10 >= 1)) {
            if(!thisBlockPrice.hasClass("text-decoration-line-through")) {
                thisBlockPrice.toggleClass("text-decoration-line-through")
                thisBlockAfterPrice.toggleClass("d-none d-block")
            }

            newPriceWithoutDisc = thisBlockPriceVal * $(this).val()
            newPrice = parseInt(newPriceWithoutDisc) - ((newPriceWithoutDisc/100) * (Math.round(rangeVal10) * 5))

            thisBlockAfterPrice.html("ОТ " + newPrice + " РУБ./МЕС. Скидка: " + Math.round(rangeVal10) * 5 + "%")
        } else if(rangeVal10 < 1 && thisBlockPrice.hasClass("text-decoration-line-through")) {
            thisBlockPrice.toggleClass("text-decoration-line-through")
            thisBlockAfterPrice.toggleClass("d-none d-block")
        }
    })

    $(".range-btn").on("click", function() {
        idRange = $(this).attr("data-range-id")
        rangeObj = $("#"+idRange)
        labelRangeLine = $("[for="+idRange+"]")

        if($(this).hasClass("range-minus-btn")) {
            rangeObj.val(parseInt(rangeObj.val()) - 1)
        } else if($(this).hasClass("range-plus-btn")) {
            rangeObj.val(parseInt(rangeObj.val()) + 1)
        }

        rangeVal = rangeObj.val()
        rangeLastNumb = parseInt(rangeVal.substr(-1))
        labelRangeLine.html(rangeVal + getEndLabelFilial(rangeLastNumb))

        rangeObj.change()
    })

    $(".button-question").on("click", function(){
        $(this).find(".bi").toggleClass("bi-plus bi-dash")
    })

    if(window.outerWidth <= 821) {
        $("#mainCard7 .btn-group label").on("click", function(){
            var myCarouselEl = $('#carouselTariff')
            var carousel = bootstrap.Carousel.getInstance(myCarouselEl)

            carousel.to($(this).attr("data-slide"))
        })

        if(window.outerWidth < 760) {
            $("#mainCard1Img").attr("src", "/static/images/main/mainCard1ImgMobile.png")
            $("#afterCard4Img").attr("src", "/static/images/main/afterMainCard4ImgMobile.png")
            $(".cardImg61").attr("src", "/static/images/main/mainCard61ImgMobile.png")
            $(".cardImg62").attr("src", "/static/images/main/mainCard62ImgMobile.png")
            $("#afterCard8Img").attr("src", "/static/images/main/afterMainCard8ImgMobile.png")
        }
    } else if(window.outerWidth >= 760) {
        $("#mainCard4 .carousel-indicators button").remove()
        $("#mainCard4 .carousel-item:eq(0) .row").append($("#mainCard4 .carousel-item .card"))
        $("#mainCard7 .carousel-item:eq(0)>.row").append($("#mainCard7 .carousel-item .tarif-block"))
    }

    $(".fst-btn-tarif").click();

    idActiveLabel = getActiveLabel()
    $("[for="+idActiveLabel+"]").toggleClass("text-dark text-white")
})