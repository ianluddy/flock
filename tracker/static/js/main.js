var roles;

$(document).ready(function () {
    page_main = $("#main");
    loader = $("#loader");
    $.when(
        ajax_load('/templates', {}, add_templates)
    ).done(templates_loaded);
});

function add_templates(input){
    $("#tmpl_holder").html(input);
}

function compile_templates(){
    // Templates
    people_tmpl = Handlebars.compile($("#people_tmpl").html());
    dashboard_tmpl = Handlebars.compile($("#dashboard_tmpl").html());
    calendar_tmpl = Handlebars.compile($("#calendar_tmpl").html());
    events_tmpl = Handlebars.compile($("#events_tmpl").html());
    things_tmpl = Handlebars.compile($("#things_tmpl").html());
    places_tmpl = Handlebars.compile($("#places_tmpl").html());
    settings_tmpl = Handlebars.compile($("#settings_tmpl").html());
    notifications_tmpl = Handlebars.compile($("#notifications_tmpl").html());
    people_type_table_tmpl = Handlebars.compile($("#people_type_table_tmpl").html());
    no_data_tmpl = Handlebars.compile($("#no_data_tmpl").html());
    people_table_body_tmpl = Handlebars.compile($("#people_table_body_tmpl").html());
    people_table_filter_tmpl = Handlebars.compile($("#people_table_filter_tmpl").html());

    // Partial Templates
    Handlebars.registerPartial("person_type_part", $("#people_type_table_row_tmpl").html());
    Handlebars.registerPartial("checkbox_part", $("#checkbox_tmpl").html());
    Handlebars.registerPartial("radio_part", $("#radio_button_tmpl").html());
}

function add_handlers(){
    $('.tab').click(tab_handler);
}

function tab_handler(){
    clear();
    var target = $(this).attr('target').toString();
    window['load_' + target]();
    $(this).addClass('active').siblings('.tab').removeClass('active');
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
    $('.i-checks').iCheck({
        checkboxClass: 'icheckbox_square-green',
        radioClass: 'iradio_square-green',
    });
    $('.color-choice').on('click', radio_toggle);
    $('.color-choice').first().click();
}

function templates_loaded(){
    compile_templates();
    add_handlers();
    if ( window.location.hash != '' ){
        var target = $('.tab[target=' + window.location.hash.replace('#', '') + ']');
        if( $(target).length > 0 ){
            $(target).click();
        }else{
            $('.tab').first().click();
        }
    }else{
        $('.tab').first().click();
    }
    $(document).ajaxStart(function() { Pace.restart(); });
}

function clear(){
    page_main.empty();
}

function loadr(show){
    $(loader).toggle(show);
}

function load_dashboard(){
    $(page_main).html(dashboard_tmpl());
}

function load_calendar(){
    $(page_main).html(calendar_tmpl());
    $('#calendar_wrap').fullCalendar({
        header: {
            left: 'prev,next today',
            center: 'title',
            right: 'month,agendaWeek,agendaDay'
        },
    })
}

function load_people(){
    var sort_by, sort_dir, search, roles, people, count;
    var page = 0;
    var limit = 10;

    function draw_people(data){
        $('#people_table_body').html(people_table_body_tmpl({'people': data.data}));
        $('#people_table_body .delete-btn').on('click', delete_person);
        $('#people_table_body .invite-btn').on('click', invite_person);
        search = $('#people_table_search');
        count = data.count;
        $('#person_count').text(data.count);
        update_pagination();
    }

    function update_pagination(){
        $('#person_start').text((limit * page) + 1);
        var end = (limit * page) + limit;
        end = end > count ? count : end;
        $('#person_end').text(end);
    }

    function next_page(){
        if( (page + 1) * limit <= count ){
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
            'type': 'post',
            'notify': false,
            'data': filter,
            'success': draw_people
        });
        $('#add_people_modal').modal('hide');
    }

    function add_person(){
        new_person = {
            'type': $('#add_person_type_choice .color-choice.selected').attr('type_id'),
            'name': $('#add_person_name').val(),
        }

        var mail = $('#add_person_email').val();
        var invite = $('#add_person_invite').is(":checked");

        if( mail.length > 0 )
            new_person['mail'] = mail;

        if( invite == true )
            new_person['invite'] = true;

        if ( new_person['name'].length > 0 )
            ajax_call({
                'url': '/people',
                'type': 'put',
                'data': new_person,
                'success': function(){
                    reload_people();
                },
            });
    }

    function delete_person(){
        to_remove = {'id': parseInt($(this).attr("people_id")), 'name': $(this).attr('name')};
        ajax_call({
            'url': '/people',
            'type': 'delete',
            'data': to_remove,
            'success': function(){
                reload_people();
            }
        });
    }

    function invite_person(){
        to_invite = {'mail': $(this).attr("mail")};
        ajax_call({'url': '/people/invite', 'type': 'post', 'data': to_invite});
    }

    function add_handlers(){
        $('#modal_add_person').on('click', add_person);
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
    $(page_main).html(places_tmpl());
}

function load_settings(){
    $(page_main).html(settings_tmpl());
    load_people_type_table();
    load_components();
}

function load_notifications(){
    $(page_main).html(notifications_tmpl());
}

function load_events(){
    $(page_main).html(events_tmpl());
}

function add_update_people_type(){
    data = {
        'theme': $('#people_type_colour .color-choice.selected').attr('value'),
        'type': $('#people_type_type_check').find('input:checked').attr('value'),
        'name': $('#people_type_name').val(),
        'id': $('#add_people_type_form').attr('people_type_id')
    }
    ajax_call({
        'url': 'roles',
        'data': data,
        'type': 'put',
        'success': load_people_type_table
    });
}

function load_people_type_table(){

    function reset_form(){
        $("#add_people_type_btn").text("Add");
        $("#people_type_name").val("");
        $("#people_type_type_check .iradio_square-green").first().click();
        $("#people_type_colour span").first().click();
        $("#add_people_type_form").attr('people_type_id', '');
    }

    function delete_people_type(){
        ajax_call({
            'url': 'roles',
            'type': 'delete',
            'data': {
                'id': $(this).attr('type_id')
             },
            'success': load_people_type_table
        });
    }

    function edit_people_type(){
        $("#add_people_type_btn").text("Update");
        $('#add_people_type_form').attr('people_type_id', $(this).attr('type_id'));
        $("#people_type_name").val($(this).attr('name'));
        $("#people_type_colour span").first().click();
        $("#people_type_type_check .iradio_square-green input[value=" + $(this).attr('role_type')  + "]").click();
        $('#people_type_colour span.label-' + $(this).attr('theme')).click();
        scrll('#main', 200);
        anim('#add_people_type_form', 'pulse');
    }

    reset_form();
    ajax_call({
        'url': 'roles',
        'notify': false,
        'success': function(input){
            roles = input;
            if( input.length > 0){
                $('#people_type_table_holder').html(people_type_table_tmpl({'types': input}));
                $('#people_type_table_body i.delete-btn').on('click', delete_people_type);
                $('#people_type_table_body i.edit-btn').on('click', edit_people_type);
            }else{
                $('#people_type_table_holder').html(no_data_tmpl({
                    'caption': 'There are no People-Types configured. Add some now!'
                }));
            }
        }
    });
}