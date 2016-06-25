
function elapsed_time(milliseconds) {
    // TIP: to find current time in milliseconds, use:
    // var  current_time_milliseconds = new Date().getTime();

    milliseconds = new Date().getTime() - milliseconds;

    function numberEnding (number) {
        return (number > 1) ? 's' : '';
    }

    var temp = Math.floor(milliseconds / 1000);
    var years = Math.floor(temp / 31536000);
    if (years) {
        return years + ' year' + numberEnding(years);
    }
    //TODO: Months! Maybe weeks?
    var days = Math.floor((temp %= 31536000) / 86400);
    if (days) {
        return days + ' day' + numberEnding(days);
    }
    var hours = Math.floor((temp %= 86400) / 3600);
    if (hours) {
        return hours + ' hr' + numberEnding(hours);
    }
    var minutes = Math.floor((temp %= 3600) / 60);
    if (minutes) {
        return minutes + ' min' + numberEnding(minutes);
    }
//    var seconds = temp % 60;
//    if (seconds) {
//        return seconds + ' s' + numberEnding(seconds);
//    }
    return 'just now'; //'just now' //or other string you like;
}

function ajax_load(func, args, callback, timeout){
    return $.ajax({
        url: func,
        data: args,
        type: 'get',
        timeout: timeout == undefined ? 10000 : timeout
    }).done(function(input){
        if (callback)
            callback(input);
    }).error(function(request, error){
        console.log(error);
    });
}

function notify_success(text){
    toastr.success(text, 'Success!', {'timeOut':2000, 'progressBar':true});
}

function notify_error(text){
    toastr.error(text, 'Oh No!', {'timeOut': 3000, 'progressBar': true});
}

function ajax_call(options){
    var url = options.url;
    var data = options.data;
    if( (options.type == 'get' || options.type == undefined) && options.data != undefined){
        url = url + '?' + $.param(options.data);
        data = '';
    }
    return $.ajax({
        url: url,
        type: options.type || "get",
        datatype: "json",
        data: data,
        complete: function(data) {
            if (options.complete != undefined)
                options.complete(data);
        },
        success: function(data) {
            if (options.success != undefined)
                options.success(data);
            if (options.notify != false)
                notify_success(data);
        },
        error: function(data) {
            if (options.error != undefined)
                options.error(data);
            if (options.notify != false) {
                if (data.responseText.indexOf('500 Internal Server Error') != -1) {
                    notify_error('Something went wrong, the error has been logged');
                } else {
                    notify_error(strip_response_msg(data.responseText));
                }
            }
        }
    });
}

function anim(dom, type){
    $(dom).addClass('animated ' + type);
    setTimeout(function(){$(dom).removeClass('animated ' + type);}, 800);
}

function strip_response_msg(msg){
    return msg.replace('</p>', '').split('<p>').slice(-1)[0];
}

function scrll(dom, delay){
    $('html, body').animate({
        scrollTop: $(dom).offset().top
    }, delay);
}

function confirmation(){
    swal({
        title: "Are you sure?",
        text: "You will not be able to recover this imaginary file!",
        type: "warning",
        showCancelButton: true,
        confirmButtonColor: "#DD6B55",
        confirmButtonText: "Yes, delete it!",
        closeOnConfirm: false
    }, function () {
        swal("Deleted!", "Your imaginary file has been deleted.", "success");
    });
}

var delay = (function(){
    var timer = 0;
    return function(callback, ms){
        clearTimeout (timer);
        timer = setTimeout(callback, ms);
    };
})();

function date_string(unix_timestamp){
    // Create a new JavaScript Date object based on the timestamp
    // multiplied by 1000 so that the argument is in milliseconds, not seconds.
    var date = new Date(unix_timestamp);
    // Hours part from the timestamp
    var hours = date.getHours();
    // Minutes part from the timestamp
    var minutes = "0" + date.getMinutes();
    // Seconds part from the timestamp
    var seconds = "0" + date.getSeconds();

    // Will display time in 10:30:23 format
    var formattedTime = hours + ':' + minutes.substr(-2);
    return formattedTime;
}

function default_evaluator(element){
    if ( $(element).val().replace(' ','').length > 0 ){
        return true;
    }
    return 'Required';
}

function email_evaluator(element){
    var valid_or_warning = default_evaluator(element);
    if ( valid_or_warning != true ){
        return valid_or_warning;
    }else{
        var re = /\S+@\S+\.\S+/;
        if( re.test($(element).val()) ){
            return true;
        }
        return 'Valid Email Required';
    }
}

function valid8(validator){
    for( var i in validator ){
        var target = validator[i];
        $(target.elem).off('change.validate').off('keyup.validate');
        var evaluator = target.eval === undefined ? default_evaluator : target.eval;
        var valid_or_warning = evaluator(target.elem);
        if( valid_or_warning != true ){
            if( $(target.elem).siblings('.val_error').length == 0 ) {
                $(target.elem).parent().append(value_error_tmpl({'warning': valid_or_warning}));
                $(target.elem).parent().find('.val_error').fadeIn();
                setTimeout(function(target){
                    $(target.elem).parent().find('.val_error').fadeOut(function(){ $(this).remove(); });
                }, 2000, target);
            }
            return false;
        }
    }
    return true;
}