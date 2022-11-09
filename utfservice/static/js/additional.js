class AjaxRequests {
    _domain = window.location.origin

    //
    // Метод проверки наличия подстроки в строке
    //
    // hasSubStr(str, substr) {
    //     if(str.indexOf(substr) == -1) {
    //         return 0
    //     } else {
    //         return 1
    //     }
    // }


    //
    // Метод изменения отображения спиннера загрузки
    //
    toggleSpinner(idSpinner, idButton) {
        $(idSpinner).toggle()
        $(idButton).toggleAttr("disabled")
    }


    //
    // Метод изменения доступа к элементам
    //
    toggleDisable(selectorElems) {
        $(selectorElems)
            .toggleAttr("disabled")
            .toggleAttr("readonly")
            .toggleClass("disabled")
    }


    //
    // Метод для добавления обработчика(ов) на кнопку(и) с ajax запросом (для подгрузки input из формы)
    //
    addAjaxEventRequest(selectorForm, actionUrl,  multipleForms = 0, operationSuccessConfig = Object(), operationErrorConfig = Object(), operationCompleteConfig = Object()) {
        $(selectorForm).on('submit', (event) => { // => убирает this в функции
            if(operationCompleteConfig.hasOwnProperty("update_spinner"))
                this.toggleSpinnerBtn(operationCompleteConfig.selectorSpinner, operationCompleteConfig.selectorButton)

            if(operationCompleteConfig.hasOwnProperty("toggle_disable"))
                this.toggleDisable(operationCompleteConfig.selectorElems)

            $.ajax({
                url: this._domain + actionUrl,
                method: 'POST',
              	headers: {'X-CSRFTOKEN': $.cookie("csrftoken")},
            	data: multipleForms == 0 ? $(selectorForm).serialize() : $(event.target).serialize(),

            	success: (data) => {
            	    if(operationSuccessConfig.hasOwnProperty("test"))
                        console.log(data)

                    if(operationSuccessConfig.hasOwnProperty("send_message"))
                        $(operationSuccessConfig.send_message).html(data) // Селектор dom объекта, куда записать сообщение

                    if(operationSuccessConfig.hasOwnProperty("reload"))
                        location.reload()

                    if(operationSuccessConfig.hasOwnProperty("run_function")) // передает в функцию выходные значения data
                        operationSuccessConfig.run_function(data)
            	},

            	error: (xhr) => {
        	        if(operationErrorConfig.hasOwnProperty("send_raise")){
        	            let exceptText = $(xhr.responseText).find(".exception_value").html()
        	            $(operationErrorConfig.send_raise).html(exceptText)
        	        }
            	},

            	complete: () => {
            	    if(operationCompleteConfig.hasOwnProperty("update_spinner"))
    	                this.toggleSpinnerBtn(operationCompleteConfig.selectorSpinner, operationCompleteConfig.selectorBtnSpinner)

    	            if(operationCompleteConfig.hasOwnProperty("toggle_disable"))
    	                this.toggleDisable(operationCompleteConfig.selectorElems)
            	},
            })
        })
    }
}


class Animation {
    //
    // Скрывает элемент selector, отображает selectorWillChanged (не забудьте добавить класс collapse обоим элементам!)
    //
    changeVisionSelectors(selector, selectorWillChanged) {
        $(selector).hide()
        $(selectorWillChanged).show()
    }

}