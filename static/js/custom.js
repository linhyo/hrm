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

/*-------------------------------------------
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
                    '<input type="text" id="newevent_name" class="form-control" placeholder="Name of event">'+
                    '</div>'+

                    '<div class="form-group">'+
                    '<label>Location</label>'+
                    '<input type="text" id="newevent_location" class="form-control" placeholder="Location">'+
                    '</div>'+

                    '<div class="form-group">'+
                    '<label>Description</label>'+
                    '<textarea rows="3" id="newevent_desc" class="form-control" placeholder="Description"></textarea>'+
                    '</div>'+

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
							description: $('#newevent_desc').val(),
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
			if (event.description != "") {
				element.attr('title', event.description);
			}
		},
		eventClick: function(calEvent, jsEvent, view) {
			var form_2 = $('<div class="row">'+
				'<div class="col-lg-12">'+
                    '<div class="form-group">'+
                    '<label>Event title</label>'+
                    '<input type="text" id="newevent_name" value="'+ calEvent.title +'" class="form-control" placeholder="Name of event">'+
                    '</div>'+

                    '<div class="form-group">'+
                    '<label>Location</label>'+
                    '<input type="text" id="newevent_location" value="'+ calEvent.location +'"class="form-control" placeholder="Location">'+
                    '</div>'+

                    '<div class="form-group">'+
                    '<label>Description</label>'+
                    '<textarea rows="3" id="newevent_desc" class="form-control" placeholder="Description">'+ calEvent.description +'</textarea>'+
                    '</div>'+

				'</div></div>');

			var buttons = $('<button id="event_cancel" type="cancel" class="btn btn-default btn-label-left">'+
							'Cancel'+
							'</button>'+
							'<button id="event_delete" type="cancel" class="btn btn-danger btn-label-left">'+
							'Delete'+
							'</button>'+
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
				calEvent.description = $('#newevent_desc').val();
                calEvent.location = $('newevent_location').val();
				calendar.fullCalendar('updateEvent', calEvent);
				CloseModalBox()
			});
		}
		});
		$('#new-event-add').on('click', function(event){
			event.preventDefault();
			var event_name = $('#new-event-title').val();
			var event_description = $('#new-event-desc').val();
            var event_location = $('#new-event-location').val();
            var tag_name = 'tag' + random_int(1, 4);
			if (event_name != ''){
			var event_template = $('<div class="external-event '+tag_name+'" data-description="'+event_description+'"><span class="tag-name">'+event_name +
                '</span><span class="tag-loc">'+event_location+'</span></div>');
			$('#events-templates-header').after(event_template);
			var eventObject = {
				title: event_name,
				description: event_description,
                location: event_location
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
function OpenModalBox(header, inner, bottom){
	var modalbox = $('#modalbox');
	//modalbox.find('.modal-header-name span').html(header);
	//modalbox.find('.devoops-modal-inner').html(inner);
	//modalbox.find('.devoops-modal-bottom').html(bottom);
    modalbox.find('.modal-body').html(inner);
    modalbox.find('.modal-footer').html(bottom);
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
                        $("#myModal").modal('show');
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

// Open Modal
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
