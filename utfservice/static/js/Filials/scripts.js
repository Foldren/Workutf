$(document).ready(function() {
    filialsRequest = new AjaxRequests()

    filialsRequest.addAjaxEventRequest(
        selectorForm = ".changeStatusFilialForm",
        actionUrl = "/filials/change_status_filial",
        multipleForms = 1,
        operationSuccessConfig = NaN,
        operationErrorConfig = NaN,
        operationCompleteConfig = {
            toggle_disable: 1,
            selectorElems: ".status-class",
        },
    )
})