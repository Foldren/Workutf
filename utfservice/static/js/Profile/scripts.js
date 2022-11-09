$(document).ready(function(){
    platformAccountsRequest = new AjaxRequests()


    platformAccountsRequest.addAjaxEventRequest(
        selectorForm = "#platformAccountsForm",
        actionUrl = "/profile/add_platform_account",
        multipleForms = 0,

        operationSuccessConfig = {
            reload: 1,
        },

        operationErrorConfig = {
            send_raise: "#messageAuthAccount",
        },
    )


    platformAccountsRequest.addAjaxEventRequest(
        selectorForm = "#profileForm",
        actionUrl = "/profile/save_profile",
        multipleForms = 0,

        operationSuccessConfig = {
            reload: 1
        },
    )


    platformAccountsRequest.addAjaxEventRequest(
        selectorForm = ".platformAccountGetIdForm",
        actionUrl = "/profile/load_platform_filials",
        multipleForms = 1,

        operationSuccessConfig = {
            run_function: renderAccountFilials,
        },

        operationCompleteConfig = {
            update_spinner: 1,
            idSpinner: "#spinnerLoadFilials",
        },
    )


    platformAccountsRequest.addAjaxEventRequest(
        selectorForm = "#includeFilialsForm",
        actionUrl = "/profile/include_filials",
        multipleForms = 0,

        operationSuccessConfig = {
            reload: 1,
        },
    )
})