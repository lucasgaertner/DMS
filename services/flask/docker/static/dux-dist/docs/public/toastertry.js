$(function() {

    function Toast(type, css, msg) {
        this.type = type;
        this.css = css;
        this.title = msg;
        this.msg = 'This is positioned in the ' + msg + '. You can also style the icon any way you like. Details at <a href="http://www.d-velop.de">d.velop.de</a>';
    }

    var toasts = [
        new Toast('error', 'toast-bottom-full-width', 'bottom full width'),
        new Toast('info', 'toast-top-full-width', 'top full width'),
        new Toast('warning', 'toast-top-left', 'top left'),
        new Toast('success', 'toast-top-right', 'top right'),
        new Toast('warning', 'toast-bottom-right', 'bottom right'),
        new Toast('error', 'toast-bottom-left', 'bottom left'),
        new Toast('info', 'toast-top-center', 'top center'),
        new Toast('warning', 'toast-bottom-center', 'bottom center'),
        new Toast('info', 'toast-middle-left', 'middle left'),
        new Toast('warning', 'toast-middle-center', 'middle center'),
        new Toast('success', 'toast-middle-full-width', 'middle full width'),
        new Toast('error', 'toast-middle-right', 'middle right')
    ];

    toastr.options.positionClass = 'toast-top-right';
    toastr.options.timeOut = 1000;
    toastr.options.extendedTimeOut = 0;
    toastr.options.showMethod = 'fadeIn';
    toastr.options.hideMethod = 'fadeOut';
    toastr.options.fadeOut = 250;
    toastr.options.fadeIn = 250;
    toastr.options.closeButton = true;
    toastr.options.progressBar = true;
    toastr.options.onclick = null;
    toastr.options.tapToDismiss = false;
    toastr.options.preventDuplicates = false;
    toastr.options.showEasing = 'linear';
    toastr.options.hideEasing = 'swing';
    toastr.options.showDuration = 300;
    toastr.options.hideDuration = 1000;
    toastr.options.newestOnTop = true;
    toastr.options.debug = false;

    var i = 0;
    var timeOut = (toastr.options.timeOut + toastr.options.extendedTimeOut + toastr.options.showDuration + toastr.options.hideDuration);

        $('#toastrTry').click(function () {
        $('#toastrTry').parent('li').addClass('disabled');
        delayToasts();
    });

    function delayToasts() {
        if (i === toasts.length) { return; }
        var delay = i === 0 ? 0 : timeOut + 1;
        window.setTimeout(function () { showToast(); }, delay);

        // re-enable the nav bar link
        if (i === toasts.length-1) {
            window.setTimeout(function () {
                $('#toastrTry').parent('li').removeClass('disabled');
                i = 0;
            }, delay * 2);
        }
    }

    function showToast() {
        var t = toasts[i];
        toastr.options.positionClass = t.css;
        toastr[t.type](t.msg,t.title.toUpperCase() + ' | ' + t.type.toUpperCase());
        i++;
        delayToasts();
    }
});
