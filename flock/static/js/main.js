var user_id, page_main, loader, permissions, account;
var people, places, things;

// Templates
var people_tmpl, dashboard_tmpl, account_tmpl, planner_tmpl, events_tmpl, things_tmpl, places_tmpl, settings_tmpl;
var notifications_tmpl, no_data_tmpl, no_data_table_tmpl, places_table_body_tmpl, people_type_table_tmpl;
var people_table_body_tmpl, event_tmpl, upcoming_events_tmpl, single_select_tmpl, multi_select_tmpl, value_error_tmpl;
var notification_rule_table_tmpl;

$(document).ready(function () {
    page_main = $("#main");
    loader = $("#loader");
    account = $("#account");
    user_id = parseInt($(account).attr("user_id"));
    permissions = $(account).attr("permissions");
    $.when(
        ajax_load('/templates', {}, add_templates)
    ).done(templates_loaded);
});

function heartbeat(){
    $.ajax({
        url: '/heartbeat',
        type: "get"
    });
}

$( document ).ajaxError(function( event, jqxhr ) {
    // Logout if session expires
    if( jqxhr.status == 403 )
        $(location).attr('href', 'logout');
});

function add_templates(input){
    $("#tmpl_holder").html(input);
}

function compile_templates(){
    // Templates
    people_tmpl = Handlebars.compile($("#people_tmpl").html());
    dashboard_tmpl = Handlebars.compile($("#dashboard_tmpl").html());
    account_tmpl = Handlebars.compile($("#account_tmpl").html());
    planner_tmpl = Handlebars.compile($("#planner_tmpl").html());
    events_tmpl = Handlebars.compile($("#events_tmpl").html());
    things_tmpl = Handlebars.compile($("#things_tmpl").html());
    places_tmpl = Handlebars.compile($("#places_tmpl").html());
    settings_tmpl = Handlebars.compile($("#settings_tmpl").html());
    no_data_tmpl = Handlebars.compile($("#no_data_tmpl").html());
    no_data_table_tmpl = Handlebars.compile($("#no_data_table_tmpl").html());
    places_table_body_tmpl = Handlebars.compile($("#places_table_body_tmpl").html());
    people_type_table_tmpl = Handlebars.compile($("#people_type_table_tmpl").html());
    people_table_body_tmpl = Handlebars.compile($("#people_table_body_tmpl").html());
    notification_rule_table_tmpl = Handlebars.compile($("#notification_rule_table_tmpl").html());
    event_tmpl = Handlebars.compile($("#event_tmpl").html());
    notifications_tmpl = Handlebars.compile($("#notifications_tmpl").html());
    upcoming_events_tmpl = Handlebars.compile($("#upcoming_events_tmpl").html());
    single_select_tmpl = Handlebars.compile($("#single_select_tmpl").html());
    multi_select_tmpl = Handlebars.compile($("#multi_select_tmpl").html());
    value_error_tmpl = Handlebars.compile($("#value_error_tmpl").html());

    // Partial Templates
    Handlebars.registerPartial("person_type_part", $("#people_type_table_row_tmpl").html());
    Handlebars.registerPartial("checkbox_part", $("#checkbox_tmpl").html());
    Handlebars.registerPartial("radio_part", $("#radio_button_tmpl").html());
}

function add_handlers(){
    $('.tab').click(tab_handler);
    $('#account_link').click(account_link_handler);
}

function account_link_handler(){
    $(".tab").removeClass('active');
    $(account).addClass('active')
    load_account();
}

function tab_handler(){
    clear();
    var target = $(this).attr('target').toString();
    window['load_' + target]();
    $(this).addClass('active').siblings('.tab').removeClass('active');
    $(account).removeClass('active');
}

function dashboard(){
    $('#dashboard_tab').click();
}

function radio_toggle(){
    $(this).addClass('selected').siblings().removeClass('selected');
}

function toggle(){
    $(this).toggleClass('selected');
}

function sort_toggle(dom){
    $(dom).parent().siblings().children('.table-sorter').removeClass('fa-sort-up').removeClass('fa-sort-down').addClass('fa-sort');
    $(dom).removeClass('fa-sort');
    if( $(dom).hasClass('fa-sort-down') ){
        $(dom).removeClass('fa-sort-down').addClass('fa-sort-up');
    }else if( $(dom).hasClass('fa-sort-up') ){
        $(dom).removeClass('fa-sort-up').addClass('fa-sort-down');
    }else{
        $(dom).addClass('fa-sort-down');
    }
}

function load_components(){
    $('.btn-choice-mult .btn').off('click');
    $('.color-choice').off('click');
    $('.label-color-choice').off('click');
    $('.btn-choice-req .btn').off('click');

    $('.i-checks').iCheck({
        checkboxClass: 'icheckbox_square-green',
        radioClass: 'iradio_square-green',
    });
    $('.color-choice').on('click', radio_toggle);
    $('.color-choice').first().click();
    $('.label-color-choice').on('click', radio_toggle);
    $('.label-color-choice').first().click();
    $('.btn-choice .btn').on('click', function(){
        $(this).siblings().removeClass('btn-primary').addClass('btn-white').removeClass('selected');
        if( $(this).hasClass('selected') ){
            $(this).removeClass('btn-primary').addClass('btn-white').removeClass('selected');
        }else{
            $(this).addClass('btn-primary').removeClass('btn-white').addClass('selected');
        }
    });
    $('.btn-choice-req .btn').on('click', function(){
        $(this).siblings().removeClass('btn-primary').addClass('btn-white').removeClass('selected');
        $(this).addClass('btn-primary').removeClass('btn-white').addClass('selected');
    });
    $('.btn-choice-mult .btn').on('click', function(){
        if( $(this).hasClass('selected') ){
            $(this).removeClass('btn-primary').addClass('btn-white').removeClass('selected');
        }else{
            $(this).addClass('btn-primary').removeClass('btn-white').addClass('selected');
        }
    });
}

function reset_components(){
    $('.btn-choice .btn').off('click').removeClass('btn-primary').addClass('btn-white').removeClass('selected');
}

function templates_loaded(){
    compile_templates();
    add_handlers();
    if ( window.location.hash != '' ){
        if( window.location.hash == '#account' ){
            account_link_handler();
        }else{
            var target = $('.tab[target=' + window.location.hash.replace('#', '') + ']');
            if( $(target).length > 0 ){
                $(target).click();
            }else{
                $('.tab').first().click();
            }
        }
    }else{
        $('.tab').first().click();
    }
    $(document).ajaxSend(function(evt, request, settings) {
        if( settings.url.indexOf('heartbeat') == -1 ) {
            Pace.restart();
        }
    });
    setInterval(heartbeat, 120000);
}

function clear(){
    page_main.empty();
}

function loadr(show){
    $(loader).toggle(show);
}

function load_account(){
    var user;
    $(page_main).html(account_tmpl());
    load_user();

    function load_user(){
        ajax_call({
            'url': '/user',
            'type': 'get',
            'notify': false,
            'success': function(input){
                user = input;
                $('#account_image img').attr('src', input['image']);
                $('#account_name').val(input['name']);
                $('#account_phone').val(input['phone']);
                $('#account_email').val(input['email']);
            }
        });
    };

    var update_account_validation = [{'elem': '#account_name'}];
    $('#update_account_btn').on('click', function(e){
        e.preventDefault();
        if( valid8(update_account_validation) ){
            ajax_call({
                'url': '/user',
                'type': 'post',
                'data': {
                    'name': $('#account_name').val(),
                    'phone': $('#account_phone').val(),
                    'image': user['image']
                },
                "success": function(){
                    $("#account a span").text($('#account_name').val());
                }
            });
        };
    });

    var change_password_validation = [{'elem': '#password_current'}, {'elem': '#password_new'}];
    $('#change_password_btn').on('click', function(e){
        e.preventDefault();
        if( valid8(change_password_validation) ){
            ajax_call({
                'url': '/password',
                'type': 'post',
                'data': {
                    'current': $('#password_current').val(),
                    'new': $('#password_new').val()
                }
            });
        };
    });

    function refresh_image(){
        load_user();
        $('#account_image_progress .progress-bar').fadeOut(function(){
            $('#account_image_progress .progress-bar').css('width', '0%');
            $('#account_image_progress .progress-bar').animate({'width': '0%'}, function(){
                $('#account_image_progress .progress-bar').css('display', 'block');
            });
        });
    }

    $('#profile_fileupload').fileupload({
        url: '/image',
        autoUpload: true,
        done: function (e, data) {
            notify_success(data.result);
            setTimeout(function(){ refresh_image() }, 1000);
        },
        progressall: function (e, data) {
            var progress = parseInt(data.loaded / data.total * 100, 10);
            $('#account_image_progress .progress-bar').css('width', progress + '%');
        },
        error: function (e, data){
            var message = e.responseText;
            if( message == undefined) {
                message = "That file is too large. Try a smaller one";
            }else{
                message = strip_response_msg(message);
            }
            notify_error(message);
        }
    });
}
function load_dashboard(){
    $(page_main).html(dashboard_tmpl());
    ajax_call({
        'url': '/events',
        'type': 'get',
        'data': {
            'limit': 10,
            'sort_by': 'start',
            'hide_expired': true,
            'user_id': user_id
        },
        'notify': false,
        'success': function(input){
            $('#upcoming-timeline-wrapper').append(upcoming_events_tmpl({'events': input}));
        }
    });
    ajax_call({
        'url': '/notifications',
        'type': 'get',
        'data': {
            'limit': 20,
            'offset': 0,
            'sort_by': 'stamp',
            'sort_dir': 'asc'
        },
        'notify': false,
        'success': function(input){
            $('#notifications-wrapper').append(notifications_tmpl({'notifications': input}));
        }
    });
}

function load_planner(){
    var can_edit = permissions.indexOf('edit_events') != -1;
    var people = [];
    var place_data, people_data, place_id, calendar;

    function load_data(){
        ajax_call({
            'url': '/places',
            'type': 'get',
            'notify': false,
            'success': function(input){
                place_data = input.data;
                add_handlers();
            }
        });
        ajax_call({
            'url': '/people',
            'type': 'get',
            'notify': false,
            'success': function(input){
                people_data = input.data;
            }
        });
    }

    function load_planner() {
        var event_height = null;
        calendar = $('#calendar_holder').fullCalendar({
            header: {
                left: 'prev,next today',
                center: 'title',
                right: 'agendaDay,agendaWeek',
                // right: 'agendaDay,agendaWeek,month',
            },
            defaultView: "agendaDay",
            height: $('#page-wrapper').height(),
            selectable: true,
            timeFormat: 'H:mm',
            events: '/events',
            eventRender: function (event, element) {
                event.start_string = date_string(event.start);
                event.end_string = date_string(event.end);
                $(event_tmpl(event)).insertAfter($(element).find('.fc-content'));
            },
            eventMouseout: function (event, element) {
                $(element.currentTarget).removeClass('active');
                $(element.currentTarget).css('height', event_height.toString() + 'px');
                $('.fc-event').removeClass('faded');
            },
            eventMouseover: function (event, element) {
                $(element.currentTarget).addClass('active');
                event_height = $(element.currentTarget).height();
                var event_body_height = $(element.currentTarget).find('.event_tip_wrapper').height() + 50;
                $(element.currentTarget).css('height', event_body_height.toString() + 'px');
                $('.fc-event').addClass('faded');
            },
            eventClick: function (event, element) {
                if( can_edit ){
                    var details = $(element.currentTarget).find('.event_details');
                    people = [];
                    var start_stamp = moment.utc(parseInt($(details).attr('event_start')));
                    var end_stamp = moment.utc(parseInt($(details).attr('event_end')));
                    $(details).find('.event_details_people span').each(function(){
                        people.push($(this).attr('person_id'))
                    });
                    place_id = event.place.id.toString();
                    load_modal_components(function(){
                        $('#add_event_modal .modal-title').text('Update Event');
                        $('#modal_add_event').text('Update');
                        $('#modal_delete_event').show();
                        $('#add_event_form').attr('event_id', event['id']);
                        $('#add_event_name').val($(details).attr('event_title'));
                        $('#add_event_description').val($(details).find('.event_details_description span').text());
                        $('#add_event_datepicker_start input').attr('value', start_stamp.format("DD/MM/YY"));
                        $('#add_event_datepicker_end input').attr('value', end_stamp.format("DD/MM/YY"));
                        $('#add_event_clockpicker_start input').attr('value', start_stamp.format("HH:mm"));
                        $('#add_event_clockpicker_end input').attr('value', end_stamp.format("HH:mm"));
                        $('#add_event_placepicker_wrapper select').val(event.place.id).trigger('chosen:updated');
                        $('#add_event_peoplepicker_wrapper select').val(people).trigger('chosen:updated');
                        $('#add_event_modal').modal('show');
                    });
                };
            }
        });
    }

    function reset_modal(){
        var soon = moment().add(1, 'hour').set('minute', 0);
        place_id = null;
        people = [];
        $('#add_event_form').attr('event_id', '');
        $('#add_event_name').val('');
        $('#add_event_description').val('');
        $('#add_event_datepicker_start input').attr('value', soon.format('DD/MM/YY'));
        $('#add_event_datepicker_end input').attr('value', soon.format('DD/MM/YY'));
        $('#add_event_clockpicker_start input').attr('value', soon.format("HH:mm"));
        $('#add_event_clockpicker_end input').attr('value', soon.add('hour', 1).format("HH:mm"));
    }

    function reload_planner(){
        $('#add_event_modal').modal('hide');
        calendar.fullCalendar('refetchEvents');
    }

    function load_modal_components(callback){
        $('#add_event_modal .modal-title').text('Add Event');
        $('#modal_add_event').text('Add');
        $('#modal_delete_event').hide();

        $('#add_event_placepicker_wrapper').html(single_select_tmpl({
            'options': place_data,
            'id': 'add_event_placepicker',
            'placeholder': 'Choose a Place...',
            'tabindex': '2'
        }));
        $("#add_event_placepicker").chosen();
        $("#add_event_placepicker").on('change', function(evt, params) { place_id = params.selected; });

        $('#add_event_peoplepicker_wrapper').html(multi_select_tmpl({
            'options': people_data,
            'id': 'add_event_peoplepicker',
            'placeholder': 'Choose Attendees...',
            'tabindex': '3'
        }));
        $("#add_event_peoplepicker").chosen();
        $("#add_event_peoplepicker").on('change', function(evt, params) {
            if( params.selected != undefined )
                people.push(params.selected);
            if( params.deselected != undefined )
                people.splice(people.indexOf(params.deselcted), 1);
        });

        $('#add_event_name').focus();

        if( callback !== undefined && typeof(callback) == "function" )
            callback();
    }

    var save_event_validation = [
        {'elem': '#add_event_name'},
        {'elem': '#add_event_placepicker_chosen', 'eval': function(element){
            if( place_id != null && place_id.length > 0 ){
                return true;
            }
            return 'Required';
        }},
        {'elem': '#add_event_datepicker_start input'},
        {'elem': '#add_event_datepicker_end input'},
        {'elem': '#add_event_clockpicker_start input'},
        {'elem': '#add_event_clockpicker_end input'}
    ];
    function save_event(e){
        e.preventDefault();
        if( valid8(save_event_validation) ){
            var event = {};
            var event_id = $('#add_event_form').attr('event_id');
            event['title'] = $('#add_event_name').val();
            event['description'] = $('#add_event_description').val();
            event['place'] = place_id;
            event['people'] = JSON.stringify(people);
            event['start'] = datepicker_start.datepicker('getDate').toString().substring(0, 16) + $('#add_event_clockpicker_start input').val();
            event['end'] = datepicker_end.datepicker('getDate').toString().substring(0, 16) + $('#add_event_clockpicker_end input').val();
            if( event_id.length > 0 ){
                event['id'] = event_id;
                ajax_call({
                    'url': '/events',
                    'type': 'put',
                    'data': event,
                    'success': reload_planner
                });
            }else{
                ajax_call({
                    'url': '/events',
                    'type': 'post',
                    'data': event,
                    'success': reload_planner
                });
            }
            reset_modal();
        }
    }

    function delete_event(e){
        e.preventDefault();
        var event = {};
        event['title'] = $('#add_event_name').val();
        event['id'] = $('#add_event_form').attr('event_id');
        if( event['id'].length > 0 ){
            ajax_call({
                'url': '/events',
                'type': 'delete',
                'data': event,
                'success': reload_planner
            });
            reset_modal();
        }
    }

    function add_handlers(){
        if( place_data.length == 0 ){
            $("#add_event_btn").on("click", function(e){
                e.preventDefault();
                e.stopPropagation();
                toastr.error('You need to add some Places first. Go to the Places tab.', 'Oh No!', {
                    'timeOut': 3000,
                    'progressBar': true
                });
            });
        }else{
            $("#add_event_btn").on("click", load_modal_components);
            $("#modal_add_event").on("click", save_event);
            $("#modal_delete_event").on("click", delete_event);
            $("#add_event_btn").on("click", reset_modal);
        }
    }

    $(page_main).html(planner_tmpl());
    var datepicker_start = $('#add_event_datepicker_start .input-group.date').datepicker({format: "dd/mm/yy", todayBtn: "linked", keyboardNavigation: false, forceParse: false, calendarWeeks: true, autoclose: true});
    var clockpicker_start = $('#add_event_clockpicker_start').clockpicker();
    var datepicker_end = $('#add_event_datepicker_end .input-group.date').datepicker({format: "dd/mm/yy", todayBtn: "linked", keyboardNavigation: false, forceParse: false, calendarWeeks: true, autoclose: true});
    var clockpicker_end = $('#add_event_clockpicker_end').clockpicker({placement: 'top'});

    if( can_edit ) {
        load_data();
        reset_modal();
    }

    load_planner();
}

function load_people(){
    var sort_by, sort_dir, search, roles, people, count, role_id;
    var page = 0;
    var limit = 10;

    function draw_people(data){
        if( data.data.length == 0){
            $('#people_table_body').html(no_data_table_tmpl({
                'caption': 'No People to display. Broaden your search or add some People!', 'span': '6'
            }));
        }else{
            $('#people_table_body').html(people_table_body_tmpl({'people': data.data}));
            $('#people_table_body .delete-btn').on('click', delete_person);
            $('#people_table_body .edit-btn').on('click', edit_person);
            $('#people_table_body .invite-btn').on('click', invite_person);
        }
        count = data.count;
        $('#person_count').text(data.count);
        update_pagination();
    }

    function update_pagination(){
        var start = (limit * page) + 1;
        start = start < count ? start : count;
        $('#person_start').text(start);
        var end = (limit * page) + limit;
        end = end > count ? count : end;
        $('#person_end').text(end);
    }

    function next_page(){
        if( (page + 1) * limit < count ){
            page = page + 1;
            reload_people();
        }
    }

    function last_page(){
        if( page > 0){
            page = page - 1;
            reload_people();
        }
    }

    function reset_people_form(){
        role_id = null;
        $("#add_person_form").attr("person_id", "");
        $("#add_person_invite_box").show();
        $('#add_person_email').removeAttr('disabled');
        $('#add_person_name').val('');
        $('#add_person_email').val('');
        $('#add_person_phone').val('');
        $("#modal_add_person").text('Add');
        $("#add_people_modal .modal-title").text("Add a Person");
        $('#add_person_rolepicker_wrapper').html(single_select_tmpl({
            'options': roles,
            'id': 'add_person_rolepicker',
            'placeholder': 'Choose Role',
            'tabindex': '4'
        }));
        $("#add_person_rolepicker").chosen();
        $("#add_person_rolepicker").on('change', function(evt, params) { role_id = params.selected; });
    }

    function reload_people(){
        $('#add_person_error').hide();
        var filter = {
            'search': search.val(),
            'sort_by': sort_by,
            'sort_dir': sort_dir,
            'offset': page,
            'limit': limit
        }
        ajax_call({
            'url': '/people',
            'type': 'get',
            'notify': false,
            'data': filter,
            'success': draw_people
        });
        $('#add_people_modal').modal('hide');
    }

    function edit_person(){
        reset_people_form();
        $("#add_person_invite_box").hide();
        var person_id = $(this).attr("person_id");
        var person_dom = $(this).parent().parent();
        $("#modal_add_person").text('Update');
        $("#add_people_modal .modal-title").text("Update a Person");
        $("#add_person_form").attr("person_id", person_id);
        $('#add_person_name').val($.trim($(person_dom).find('.person_name').text()));
        $('#add_person_email').val($.trim($(person_dom).find('.person_email').text()));
        $('#add_person_email').attr('disabled','');
        var person_phone = $(person_dom).find('.person_phone').text();
        if( person_phone.indexOf('Unknown') == -1 )
            $('#add_person_phone').val($.trim(person_phone));
    }

    var add_person_validation = [
        {'elem': '#add_person_name'},
        {'elem': '#add_person_email', 'eval': email_evaluator},
        {'elem': '#add_person_rolepicker_chosen', 'eval': function(element){
            if( role_id != null && role_id.length > 0 ){
                return true;
            }
            return 'Required';
        }}
    ];
    function add_person(e){
        e.preventDefault();
        if( valid8(add_person_validation) ){
            var person = {
                'role': role_id,
                'name': $('#add_person_name').val(),
                'email': $('#add_person_email').val()
            };
            var person_id = $('#add_person_form').attr('person_id');
            var phone = $('#add_person_phone').val();
            var invite = $('#add_person_invite').is(":checked");

            if( invite == true )
                person['invite'] = true;

            if( phone.length > 0)
                person['phone'] = phone;

            if ( person['name'].length > 0 && person['email'].length > 0 )

                if( person_id.length > 0 ){
                    person['id'] = person_id;
                    ajax_call({
                        'url': '/people',
                        'type': 'put',
                        'data': person,
                        'success': reload_people
                    });
                }else{
                    ajax_call({
                        'url': '/people',
                        'type': 'post',
                        'data': person,
                        'success': reload_people
                    });
                }
        }
    }

    function delete_person(){
        var to_remove = {'id': parseInt($(this).attr("person_id")), 'name': $(this).attr('name')};
        ajax_call({
            'url': '/people',
            'type': 'delete',
            'data': to_remove,
            'success': reload_people
        });
    }

    function invite_person(){
        var to_invite = {'email': $(this).attr("email")};
        ajax_call({'url': '/people/invite', 'type': 'post', 'data': to_invite, 'success': reload_people});
    }

    function add_handlers(){
        $('#modal_add_person').on('click', add_person);
        $('#add_person_btn').on('click', reset_people_form);
        $('#people_table_search').on('keyup', function(){
            delay(function(){
                page = 0;
                reload_people();
            }, 800 );
        });
        $('.table-sorter').on('click', function(){
            sort_toggle($(this));
            sort_by = $(this).attr('sorter');
            sort_dir = $(this).hasClass('fa-sort-down') == true ? 'desc' : 'asc';
            reload_people();
        });
        $('#person_next').on('click', next_page);
        $('#person_prev').on('click', last_page);
        search = $('#people_table_search');
    }
    $.when(
        ajax_load('/roles', {}, function(data){roles=data}),
        ajax_load('/people', {}, function(data){people=data})
    ).done(function(){
        $(page_main).html(people_tmpl({"roles": roles}));
        draw_people(people);
        add_handlers();
        load_components();
    });
}

function load_things(){
    $(page_main).html(things_tmpl());
}

function load_places(){
    var sort_by, sort_dir, search, places, count;
    var page = 0;
    var limit = 10;

    function draw_places(data){
        if( data.data.length == 0){
            $('#places_table_body').html(no_data_table_tmpl({
                'caption': 'No Places to display. Broaden your search or add some Places!', 'span': '5'
            }));
        }else{
            $('#places_table_body').html(places_table_body_tmpl({'places': data.data}));
            $('#places_table_body .delete-btn').on('click', delete_place);
            $('#places_table_body .edit-btn').on('click', edit_place);
        }
        count = data.count;
        $('#places_count').text(data.count);
        update_pagination();
    }

    function update_pagination(){
        var start = (limit * page) + 1;
        start = start < count ? start : count;
        $('#places_start').text(start);
        var end = (limit * page) + limit;
        end = end > count ? count : end;
        $('#places_end').text(end);
    }

    function next_page(){
        if( (page + 1) * limit < count ){
            page = page + 1;
            reload_places();
        }
    }

    function last_page(){
        if( page > 0){
            page = page - 1;
            reload_places();
        }
    }

    function reset_places_form(){
        $("#add_place_form").attr("place_id", "");
        $('#add_place_name').val('');
        $('#add_place_email').val('');
        $('#add_place_phone').val('');
        $('#add_place_address').val('');
        $("#modal_add_place").text('Add');
        $("#add_places_modal .modal-title").text("Add a Place");
    }

    function reload_places(){
        $('#add_place_error').hide();
        var filter = {
            'search': search.val(),
            'sort_by': sort_by,
            'sort_dir': sort_dir,
            'offset': page,
            'limit': limit
        }
        ajax_call({
            'url': '/places',
            'type': 'get',
            'notify': false,
            'data': filter,
            'success': draw_places
        });
        $('#add_places_modal').modal('hide');
    }

    var add_place_validation = [
        {'elem': '#add_place_name'},
        {'elem': '#add_place_address'}
    ];
    function add_place(e){
        e.preventDefault();

        if( valid8(add_place_validation) ){
            var place = {
                'name': $('#add_place_name').val(),
                'email': $('#add_place_email').val(),
                'phone': $('#add_place_phone').val(),
                'address': $('#add_place_address').val(),
            };
            if ( place['name'].length > 0 && place['address'].length > 0 ) {
                var place_id = $("#add_place_form").attr("place_id").toString();
                if( place_id.length > 0){
                    place['id'] = place_id;
                    ajax_call({
                        'url': '/places',
                        'type': 'put',
                        'data': place,
                        'success': reload_places
                    });
                }else{
                    ajax_call({
                        'url': '/places',
                        'type': 'post',
                        'data': place,
                        'success': reload_places
                    });
                }
            }
        }
    }

    function delete_place(){
        var to_remove = {'id': parseInt($(this).attr("place_id")), 'name': $(this).attr('name')};
        ajax_call({
            'url': '/places',
            'type': 'delete',
            'data': to_remove,
            'success': function(){
                reload_places();
            }
        });
    }

    function edit_place(){
        reset_places_form();
        var place_id = $(this).attr("place_id");
        var place_dom = $(this).parent().parent();
        $("#modal_add_place").text('Update');
        $("#add_places_modal .modal-title").text("Update a Place");
        $("#add_place_form").attr("place_id", place_id);

        $('#add_place_name').val($.trim($(place_dom).find('.place_name').text()));
        $('#add_place_address').val($.trim($(place_dom).find('.place_address').text()));

        var place_email = $(place_dom).find('.place_mail').text();
        if( place_email.indexOf('Unknown') == -1 )
            $('#add_place_email').val($.trim(place_email));

        var place_phone = $(place_dom).find('.place_phone').text();
        if( place_phone.indexOf('Unknown') == -1 )
            $('#add_place_phone').val($.trim(place_phone));
    }

    function add_handlers(){
        $('#modal_add_place').on('click', add_place);
        $('#add_places_btn').on('click', reset_places_form);
        $('#places_table_search').on('keyup', function(){
            delay(function(){
                page = 0;
                reload_places();
            }, 800 );
        });
        $('.table-sorter').on('click', function(){
            sort_toggle($(this));
            sort_by = $(this).attr('sorter');
            sort_dir = $(this).hasClass('fa-sort-down') == true ? 'desc' : 'asc';
            reload_places();
        });
        $('#place_next').on('click', next_page);
        $('#place_prev').on('click', last_page);
        search = $('#places_table_search');
    }
    $.when(
        ajax_load('/places', {}, function(data){places=data})
    ).done(function(){
        $(page_main).html(places_tmpl());
        draw_places(places);
        add_handlers();
        load_components();
    });
}

function load_settings(){
    $(page_main).html(settings_tmpl());
    load_settings_people();
    $("#settings_roles_tab").on("click", load_settings_people);
    $("#settings_rules_tab").on("click", load_settings_notifications);
}

function load_settings_notifications(){
    var role_data;
    var rule_id = "";
    var roles = [];
    var object = null;
    var actions = [];

    function draw_rules(input){
        $('#notification_rule_table_holder').empty();
        if( input.length == 0 ){
            $('#notification_rule_table_holder').html(no_data_tmpl({
                'caption': 'There are no Notification Rules configured. Add some now!'
            }));
        }
        $('#notification_rule_table_holder').append(notification_rule_table_tmpl({'rules': input}));
        $('#rule_table_body i.delete-btn').on('click', delete_rule);
        $('#rule_table_body i.edit-btn').on('click', edit_rule);
        add_handlers();
    }

    var save_rule_validation = [
        {'elem': '#rule-action-picker', 'eval': function(element){
            if( $('#rule-action-picker button.selected').length > 0 ){
                return true;
            }
            return 'Required';
        }},
    ];
    function save_rule(e){
        e.preventDefault();

        if( valid8(save_rule_validation)){
            var args = get_args();
            if ( rule_id.length > 0 ){
                args.id = rule_id;
                ajax_call({
                    'url': 'email_rules',
                    'data': args,
                    'type': 'PUT',
                    'success': load_rules
                });
            }else{
                ajax_call({
                    'url': 'email_rules',
                    'data': args,
                    'type': 'POST',
                    'success': load_rules
                });
            }
        }
    }

    function add_handlers(){
        $('#modal_add_rule_btn').off('click');
        $('#add_rule_btn').off('click');

        $('#modal_add_rule_btn').on('click', save_rule);
        $('#add_rule_btn').on('click', open_modal);

    }

    function open_modal(){
        reset_form();
        $('#add_rule_modal').modal('show');
    }

    function get_args(){
        object = $('#rule-object-picker button.selected:first').attr('value');

        actions = [];
        $('#rule-action-picker button.selected').each(function(){
            actions.push($(this).attr('value'));
        });

        return {
            'roles': JSON.stringify(roles),
            'actions': JSON.stringify(actions),
            'object': object
        };
    }

    function reset_form(){
        $('#add_rule_rolepicker_wrapper').html(multi_select_tmpl({
            'options': role_data,
            'id': 'add_rule_peoplepicker',
            'class': 'req-input',
            'placeholder': 'All Users',
            'tabindex': '1'
        }));
        $("#add_rule_peoplepicker").chosen();
        $("#add_rule_peoplepicker").on('change', function(evt, params) {
            if( params.selected != undefined )
                roles.push(params.selected);
            if( params.deselected != undefined )
                roles.splice(roles.indexOf(params.deselected), 1);
        });
        $("#rule-action-picker button").removeClass("selected").removeClass("btn-primary").addClass("btn-white");
        roles = [];
        rule_id = "";
        load_components();
        $("#modal_add_rule_btn").text("Add");
        $("#add_rule_modal .modal-title").text("Add Rule");
    }

    function delete_rule(){
        ajax_call({
            'url': 'email_rules',
            'type': 'delete',
            'data': {
                'id': $(this).attr('rule_id')
             },
            'success': load_rules
        });
    }

    function edit_rule(){
        reset_form();
        rule_id = $(this).attr("rule_id");
        $('#add_rule_modal').modal('show');
        $("#modal_add_rule_btn").text("Update");
        $("#add_rule_modal .modal-title").text("Update Rule");

        var rule_dom = $("#rule_" + $(this).attr('rule_id'));

        $("#rule-object-picker button[pretty_value='" + $(rule_dom).attr('rule_object') + "']").click();

        roles = [];
        $(rule_dom).find(".person_role").each(function(){
            roles.push($(this).attr("role_id"));
        });

        $('#add_rule_rolepicker_wrapper select').val(roles).trigger('chosen:updated');

        if( $(rule_dom).find('.rule-added').length )
            $("#rule-action-picker button[value=added]").click();

        if( $(rule_dom).find('.rule-edited').length )
            $("#rule-action-picker button[value=edited]").click();

        if( $(rule_dom).find('.rule-deleted').length )
            $("#rule-action-picker button[value=deleted]").click();

    }

    function load_rules(){
        $('#add_rule_modal').modal('hide');
        reset_form();
        ajax_call({
            'url': 'email_rules',
            'notify': false,
            'success': draw_rules
        });
    }

    function load_data(){
        ajax_call({
            'url': '/roles',
            'type': 'get',
            'notify': false,
            'success': function(input){
                role_data = input;
            }
        });
    }
    load_data();
    load_rules();
}

function load_settings_people(){

    function reset_form(){
        reset_components();
        $("#modal_add_role_btn").text("Add");
        $('#add_role_modal .modal-title').text("Add Role");
        $("#add_role_name").val("");
        $('#role_colour span').first().click();
        $("#add_role_form").attr('role_id', '');
        $('#modal_add_role_btn').off('click');
        $('#add_role_modal').modal('hide');
    }

    function edit_role(){
        reset_form();
        add_handlers();
        $('#add_role_modal').modal('show');
        $('#add_role_modal .modal-title').text("Update Role");
        $("#modal_add_role_btn").text("Update");
        $("#add_role_form").attr('role_id', $(this).attr('role_id'));
        $("#add_role_name").val($(this).attr('name'));
        $('#role_colour span.label-' + $(this).attr('theme')).click();
        var permissions = $(this).attr('permissions').split(',');
        for( var i in permissions ){
            $('#add_role_form .btn[value="' + permissions[i] + '"]').click();
        }
    }
    var save_role_validation = [
        {'elem': '#add_role_name'}
    ];
    function save_role(e){
        e.preventDefault();

        if( valid8(save_role_validation)){
            var role_id = $('#add_role_form').attr('role_id');

            var data = {
                'theme': $('#role_colour .color-choice.selected').attr('value'),
                'name': $('#add_role_name').val(),
                'permissions': []
            };

            if( data.name.length > 0 ) {

                $('#add_role_form .btn-choice .btn.selected').each(function () {
                    var dom_permissions = $(this).attr('value');
                    if (dom_permissions != undefined) {
                        var split_permissions = dom_permissions.split(' ');
                        for (var i in split_permissions) {
                            data.permissions.push(split_permissions[i]);
                        }
                    }
                });

                data.permissions = JSON.stringify(data.permissions);

                if ( role_id.length > 0 ){
                    data.id = role_id;
                    ajax_call({
                        'url': 'roles',
                        'data': data,
                        'type': 'PUT',
                        'success': load_roles
                    });
                }else{
                    ajax_call({
                        'url': 'roles',
                        'data': data,
                        'type': 'POST',
                        'success': load_roles
                    });
                }
            }
        }
    }

    function delete_role(){
        ajax_call({
            'url': 'roles',
            'type': 'delete',
            'data': {
                'id': $(this).attr('role_id')
             },
            'success': load_roles
        });
    }

    function draw_roles(input){
        if( input.length > 0 ){
            $('#role_table_holder').html(people_type_table_tmpl({'types': input}));
        }else{
            $('#role_table_holder').html(no_data_tmpl({
                'caption': 'There are no People-Types configured. Add some now!'
            }));
        }
        $('#role_table_body i.delete-btn').on('click', delete_role);
        $('#role_table_body i.edit-btn').on('click', edit_role);
        $('#add_role_btn').on('click', open_modal);
    }

    function open_modal(){
        reset_form();
        add_handlers();
    }

    function add_handlers(){
        load_components();
        $('#modal_add_role_btn').on('click', save_role);
    }

    function load_roles(){
        reset_form();
        ajax_call({
            'url': 'roles',
            'notify': false,
            'success': draw_roles
        });
    }

    load_roles();
}