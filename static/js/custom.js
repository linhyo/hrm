/**
 * Created by hails on 1/10/15.
 */

//
// Function to generate a random number
//
var pre = 1
function random_int(start, end) {
    var x = Math.floor((Math.random() * end) + start);
    if (x == pre) {
        x = Math.floor((Math.random() * end) + start);
    }
    pre = x;
    return x;
}
/*---------------------------------------------*/
//
// Dynamically load Fullcalendar Plugin Script
// homepage: http://arshaw.com/fullcalendar
// require moment.js
//
function LoadCalendarScript(callback){
        function LoadFullCalendarScript(){
                if(!$.fn.fullCalendar){
                        $.getScript(STATIC + 'plugins/fullcalendar/fullcalendar.js', callback);
                }
                else {
                        if (callback && typeof(callback) === "function") {
                                callback();
                        }
                }
        }
        if (!$.fn.moment){
                $.getScript(STATIC + 'plugins/moment/moment.min.js', LoadFullCalendarScript);
        }
        else {
                LoadFullCalendarScript();
        }
}

/*-------------------------------------------class Event
	Function for Calendar page (calendar.html)
---------------------------------------------*/
//
// Example form validator function
//
function DrawCalendar(){
	/* initialize the external events
	-----------------------------------------------------------------*/
	$('#external-events div.external-event').each(function() {
		// create an Event Object (http://arshaw.com/fullcalendar/docs/event_data/Event_Object/)
		var eventObject = {
			title: $.trim($(this).text()) // use the element's text as the event title
		};
		// store the Event Object in the DOM element so we can get to it later
		$(this).data('eventObject', eventObject);
		// make the event draggable using jQuery UI
		$(this).draggable({
			zIndex: 999,
			revert: true,      // will cause the event to go back to its
			revertDuration: 0  //  original position after the drag
		});
	});
	/* initialize the calendar
	-----------------------------------------------------------------*/
	var calendar = $('#calendar').fullCalendar({
            eventSources: [

            // your event source
            {
                url: EVENTS_JSON,
                type: 'POST',
                data: {
                    custom_param1: 'something',
                    custom_param2: 'somethingelse'
                },
                error: function() {
                    alert('there was an error while fetching events!');
                }
            }
        ],
		header: {
			left: 'prev,next today',
			center: 'title',
			right: 'month,agendaWeek,agendaDay'
		},
		selectable: true,
		selectHelper: true,
		select: function(start, end, allDay) {

            var form = $('<div class="row">'+
				'<div class="col-lg-12">'+
                    '<div class="form-group">'+
                    '<label>Event title</label>'+
                    '<input type="text" id="newevent_name" name="title" class="form-control" placeholder="Name of event">'+
                    '</div>'+

                    '<div class="form-group">'+
                    '<label>Location</label>'+
                    '<input type="text" id="newevent_location" name="location" class="form-control" placeholder="Location">'+
                    '</div>'+

                    '<div class="form-group">'+
                    '<label>Description</label>'+
                    '<textarea rows="3" id="newevent_content" name="content" class="form-control" placeholder="Description"></textarea>'+
                    '</div>'+

                    '<input type="hidden" name="date" value="'+ start +'">'+
                    '<input type="hidden" name="id" value="undefined">'+

				'</div></div>');

			var buttons = $('<button id="event_cancel" type="cancel" class="btn btn-default btn-label-left">'+
							'Cancel'+
							'</button>'+
							'<button type="submit" id="event_submit" class="btn btn-primary btn-label-left pull-right">'+
							'Add'+
							'</button>');
			OpenModalBox('Add event', form, buttons);
			$('#event_cancel').on('click', function(){
				CloseModalBox();
			});
			$('#event_submit').on('click', function(){
				var new_event_name = $('#newevent_name').val();
				if (new_event_name != ''){
					calendar.fullCalendar('renderEvent',
						{
							title: new_event_name,
							content: $('#newevent_content').val(),
							start: start,
							end: end,
							allDay: allDay
						},
						true // make the event "stick"
					);
				}
				CloseModalBox();
			});
			calendar.fullCalendar('unselect');
		},
		editable: true,
		droppable: true, // this allows things to be dropped onto the calendar !!!
		drop: function(date, allDay) { // this function is called when something is dropped
			// retrieve the dropped element's stored Event Object
			var originalEventObject = $(this).data('eventObject');
			// we need to copy it, so that multiple events don't have a reference to the same object
			var copiedEventObject = $.extend({}, originalEventObject);
			// assign it the date that was reported
			copiedEventObject.start = date;
			copiedEventObject.allDay = allDay;
			// render the event on the calendar
			// the last `true` argument determines if the event "sticks" (http://arshaw.com/fullcalendar/docs/event_rendering/renderEvent/)
			$('#calendar').fullCalendar('renderEvent', copiedEventObject, true);
			// is the "remove after drop" checkbox checked?
			if ($('#drop-remove').is(':checked')) {
				// if so, remove the element from the "Draggable Events" list
				$(this).remove();
			}
		},
		eventRender: function (event, element, icon) {
			if (event.content != "") {
				element.attr('title', event.content);
			}
		},
		eventClick: function(calEvent, jsEvent, view) {
            console.log(calEvent);
            console.log(view);
            var form_content = '<div class="row">'+
				'<div class="col-lg-12">'+
                    '<div class="form-group">'+
                    '<label>Event title</label>'+
                    '<input type="text" name="title" id="newevent_name" value="'+ calEvent.title +'" class="form-control" placeholder="Name of event">'+
                    '</div>'+

                    '<div class="form-group">'+
                    '<label>Location</label>'+
                    '<input type="text" name="location" id="newevent_location" value="'+ calEvent.location +'"class="form-control" placeholder="Location">'+
                    '</div>'+

                    '<div class="form-group">'+
                    '<label>Description</label>'+
                    '<textarea rows="3" name="content" id="newevent_content" class="form-control" placeholder="Description">'+ calEvent.content +'</textarea>'+
                    '</div>'+

                    '<input type="hidden" name="date" value="'+ calEvent.start +'">';

            if (calEvent.event_id != null) {
                form_content += '<input type="hidden" name="id" value="'+ calEvent.event_id +'">';

            }
            form_content += '</div></div>';
            console.log(form_content)
			var form_2 = $(form_content);

            console.log(calEvent.event_id);
			var buttons = $('<button id="event_cancel" type="cancel" class="btn btn-default btn-label-left">'+
							'Cancel'+
							'</button>'+
							'<a id="event_delete" href="'+ calEvent.delete_url +'" type="cancel" class="btn btn-danger btn-label-left">'+
							'Delete'+
							'</a>'+
							'<button type="submit" id="event_change" class="btn btn-primary btn-label-left pull-right">'+
							'Save changes'+
							'</button>');
			OpenModalBox('Edit event', form_2, buttons);
			$('#event_cancel').on('click', function(){
				CloseModalBox();
			});
			$('#event_delete').on('click', function(){
				calendar.fullCalendar('removeEvents' , function(ev){
					return (ev._id == calEvent._id);
				});
				CloseModalBox();
			});
			$('#event_change').on('click', function(){
				calEvent.title = $('#newevent_name').val();
				calEvent.content = $('#newevent_content').val();
                calEvent.location = $('newevent_location').val();
				calendar.fullCalendar('updateEvent', calEvent);
				CloseModalBox()
			});
		}
		});
		$('#new-event-add').on('click', function(event){
			event.preventDefault();
			var event_name = $('#new-event-title').val();
			var event_description = $('#new-event-content').val();
            var event_location = $('#new-event-location').val();
            var tag_name = 'tag' + random_int(1, 4);
			if (event_name != ''){
			var event_template = $('<div class="external-event '+tag_name+'" data-description="'+event_description+'"><span class="tag-name">'+event_name +
                '</span><span class="tag-loc">'+event_location+'</span></div>');
			$('#events-templates-header').after(event_template);
			var eventObject = {
				title: event_name,
				content: event_description,
                location: event_location,
			};
			// store the Event Object in the DOM element so we can get to it later
			event_template.data('eventObject', eventObject);
			event_template.draggable({
				zIndex: 999,
				revert: true,
				revertDuration: 0
			});
			}
		});
}

//
// Load scripts and draw Calendar
//
function DrawFullCalendar(){
        $.getScript(STATIC + 'plugins/jquery-ui/jquery-ui.min.js');
        LoadCalendarScript(DrawCalendar);
}
//
//  Function set min-height of window
//
function SetMinBlockHeight(elem){
        elem.css('min-height', window.innerHeight - 49)
}

//
//  Helper for open ModalBox with requested header, content and bottom
//
//
function OpenModalBox(header, inner, bottom, url){
    // Default value for url is None
    url = typeof url !== 'undefined' ? url : EVENT_UPDATE;
	var modalbox = $('#modalbox');
    modalbox.find('.modal-body').html(inner);
    modalbox.find('.modal-footer').html(bottom);
    if (url != null) {
        var form = modalbox.find('form');
        form.attr('action', url);
        form.attr('method', 'POST');
    }
    modalbox.modal('show');
	modalbox.fadeIn('fast');
	$('body').addClass("body-expanded");
}
//
//  Close modalbox
//
//
function CloseModalBox(){
	var modalbox = $('#modalbox');
	modalbox.fadeOut('fast', function(){
		modalbox.find('.modal-header-name span').children().remove();
		modalbox.find('.devoops-modal-inner').children().remove();
		modalbox.find('.devoops-modal-bottom').children().remove();
		$('body').removeClass("body-expanded");
	});
}

//
// Function for table, located in element with id = datatable-3
//
function TestTable3(){
	$('#datatable-3').dataTable( {
		"aaSorting": [[ 0, "asc" ]],
		"sDom": "T<'box-content'<'col-sm-6'f><'col-sm-6 text-right'l><'clearfix'>>rt<'box-content'<'col-sm-6'i><'col-sm-6 text-right'p><'clearfix'>>",
		"sPaginationType": "bootstrap",
		"oLanguage": {
			"sSearch": "",
			"sLengthMenu": '_MENU_'
		},
		"oTableTools": {
			"sSwfPath": "plugins/datatables/copy_csv_xls_pdf.swf",
			"aButtons": [
                {
                    "fnClick": function ( nButton, oConfig, oFlash ) {
                        var modal = $("#myModal")
                        modal.find('button[type="submit"]').text("Add");
                        modal.find('a.delete_item').hide();
                        modal.modal('show');
                    },
                    "sButtonClass": "schedule-button",
                    "sExtends": "text",
                    "sButtonText": "New Item"
                },
				"copy",
				"print",
				{
					"sExtends":    "collection",
					"sButtonText": 'Save <span class="caret" />',
					"aButtons":    [ "csv", "xls", "pdf" ]
				}
			]
		}
	});
}

//
//  Dynamically load jQuery Select2 plugin
//  homepage: https://github.com/ivaynberg/select2  v3.4.5
//
function LoadSelect2Script(callback){
	if (!$.fn.select2){
		$.getScript(STATIC + 'plugins/select2/select2.min.js', callback);
	}
	else {
		if (callback && typeof(callback) === "function") {
			callback();
		}
	}
}
//
//  Dynamically load DataTables plugin
//  homepage: http://datatables.net
//
function LoadDataTablesScripts(callback){
	function LoadDatatables(){
		$.getScript(STATIC + 'plugins/datatables/jquery.dataTables.js', function(){
			$.getScript(STATIC + 'plugins/datatables/ZeroClipboard.js', function(){
				$.getScript(STATIC + 'plugins/datatables/TableTools.js', function(){
					$.getScript(STATIC + 'plugins/datatables/dataTables.bootstrap.js', callback);
				});
			});
		});
	}
	if (!$.fn.dataTables){
		LoadDatatables();
	}
	else {
		if (callback && typeof(callback) === "function") {
			callback();
		}
	}
}

//
//  Function maked all .box selector is draggable, to disable for concrete element add class .no-drop
//
function WinMove(){
	$( "div.box").not('.no-drop')
		.draggable({
			revert: true,
			zIndex: 2000,
			cursor: "crosshair",
			handle: '.box-name',
			opacity: 0.8
		})
		.droppable({
			tolerance: 'pointer',
			drop: function( event, ui ) {
				var draggable = ui.draggable;
				var droppable = $(this);
				var dragPos = draggable.position();
				var dropPos = droppable.position();
				draggable.swap(droppable);
				setTimeout(function() {
					var dropmap = droppable.find('[id^=map-]');
					var dragmap = draggable.find('[id^=map-]');
					if (dragmap.length > 0 || dropmap.length > 0){
						dragmap.resize();
						dropmap.resize();
					}
					else {
						draggable.resize();
						droppable.resize();
					}
				}, 50);
				setTimeout(function() {
					draggable.find('[id^=map-]').resize();
					droppable.find('[id^=map-]').resize();
				}, 250);
			}
		});
}
//
// Swap 2 elements on page. Used by WinMove function
//
jQuery.fn.swap = function(b){
	b = jQuery(b)[0];
	var a = this[0];
	var t = a.parentNode.insertBefore(document.createTextNode(''), a);
	b.parentNode.insertBefore(a, b);
	t.parentNode.insertBefore(b, t);
	t.parentNode.removeChild(t);
	return this;
};

//
//  Dynamically load  jQuery Timepicker plugin
//  homepage: http://trentrichardson.com/examples/timepicker/
//
function LoadTimePickerScript(callback){
	if (!$.fn.timepicker){
		$.getScript(STATIC + 'plugins/jquery-ui-timepicker-addon/jquery-ui-timepicker-addon.min.js', callback);
	}
	else {
		if (callback && typeof(callback) === "function") {
			callback();
		}
	}
}

// Open Schedule Modal
function OpenMeetingModal() {
    $('.event-block').on('click', function(evt) {
        // Retrieve meeting data
        var meeting_json =  $(evt.currentTarget).data('json');
        console.log(meeting_json);
        // Update modal data
        var modal = $('#myModal');
        var location_input = modal.find('input#inputLocation');
        var purpose_input = modal.find('textarea#inputPurpose');
        var date_input = modal.find('input[name="date"]');
        var time_input = modal.find('input[name="time"]');
        var delete_button = modal.find('a.delete_item');
        var update_form = modal.find('form');

        location_input.val(meeting_json.location);
        purpose_input.val(meeting_json.purpose);
        date_input.val(meeting_json.date);
        time_input.val(meeting_json.time);
        var delete_link = delete_button.attr('href');
        delete_button.attr('href', delete_link.replace(0, meeting_json.id));
        var action = update_form.attr('action');
        update_form.attr('action', action.replace(0, meeting_json.id));
        // Attendants
        var attendants_input = modal.find('input#inputAttandants');
        attendants_input.tagsinput('removeAll');
        var attendants_data = meeting_json.attendants.split(",");
        for (i = 0; i < attendants_data.length; i++) {
            attendants_input.tagsinput('add', staff_objects[attendants_data[i]]);
        }

        // Display modal
        modal.modal('show');
    });
}

// New Plan Modal
function OpenNewPlan(action_url) {
    $('.new-plan').on('click', function(evt) {
        // Display modal;
        var modal = $('#myModal');
        var create_form = modal.find('form');
        var delete_button = modal.find('a.delete_item');
        var submit_button = modal.find('button[type="submit"]');
        submit_button.text("Create")
        var action = create_form.attr('action');
        delete_button.hide()
        create_form.attr('action', action_url);

        modal.modal('show');
    });
}

// Open Plan Modal
function OpenPlanModal() {
    $('.plan-block').on('click', function(evt) {
        // Retrieve plan data
        var plan_json =  $(evt.currentTarget).data('json');
        // Update modal data
        var modal = $('#myModal');
        var content_input = modal.find('textarea#inputContent');
        var start_input = modal.find('input#inputStartDate');
        var due_input = modal.find('input#inputDueDate');
        var status_input = modal.find('input[type="radio"]');
        var delete_button = modal.find('a.delete_item');
        var update_form = modal.find('form');

        content_input.val(plan_json.content);
        start_input.val(plan_json.start_date);
        due_input.val(plan_json.due_date);
        for (var i = 0; i < status_input.length; i++) {
            var obj = $(status_input[i]);
            if (obj.val() == plan_json.status) {
                obj.prop('checked', true);
            }
            else{
                obj.prop('checked', false);
            }
        }

        var delete_link = delete_button.attr('href');
        delete_button.attr('href', delete_link.replace(0, plan_json.id));
        delete_button.show();
        var action = update_form.attr('action');
        update_form.attr('action', action.replace(0, plan_json.id));
        var submit_button = modal.find('button[type="submit"]');
        submit_button.text("Save Changes");

        // Staffs
        var staffs_input = modal.find('input#inputStaffs');
        staffs_input.tagsinput('removeAll');
        var staffs_data = plan_json.staffs_ref.split(",");
        for (i = 0; i < staffs_data.length; i++) {
            staffs_input.tagsinput('add', staff_objects[staffs_data[i]]);
        }

        // Display modal
        modal.modal('show');
    });
}

// Function to dynamically load modal data
function LoadScheduleModal() {
    $('span[class^="session"]').on("click", function(evt){
        // Retrieve item data
        var item_json =  $(evt.currentTarget).data('json');
        // Find modal element
        var modal = $('#myModal');
        var subject_choice = modal.find('select[name="subject"]');
        var day_choice = modal.find('select[name="day"]');
        var session_choice = modal.find('select[name="session"]');
        var teacher_choice = modal.find('select[name="staff"]');
        var room_input = modal.find('input[name="room"]');
        var class_input = modal.find('input[name="classes"]');
        var id_input = modal.find('input[name="id"]');


        // Set element value
        subject_choice.select2("val", item_json.subject);
        day_choice.select2("val", item_json.day);
        session_choice.select2("val", item_json.session);
        teacher_choice.select2("val", item_json.staff);
        room_input.val(item_json.room);
        class_input.val(item_json.class);
        id_input.val(item_json.id);
        var form = modal.find('form');
        form.attr('method', 'POST');
        var delete_button = modal.find('a.delete_item');
        var delete_link = delete_button.attr('href');
        delete_button.attr('href', delete_link.replace(0, item_json.id));
        delete_button.show();
        modal.find('button[type="submit"]').text("Save Changes");


        modal.modal("show");

    });
}