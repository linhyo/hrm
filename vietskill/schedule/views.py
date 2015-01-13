import json

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.core.urlresolvers import reverse

from vietskill import models
from vietskill.schedule import forms

from django.contrib import messages


def meeting_delete(request, pk):
    meeting = get_object_or_404(models.Meeting, pk=pk)
    meeting.delete()
    return redirect(meeting_index)


def meeting_update(request, pk):
    if request.method == 'POST':
        # process form
        form = forms.MeetingForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # Create meeting
            meeting = get_object_or_404(models.Meeting, pk=pk)
            meeting.datetime = form.cleaned_data.get('datetime') or meeting.datetime
            meeting.purpose = form.cleaned_data.get('purpose') or meeting.purpose
            meeting.location = form.cleaned_data.get('location') or meeting.location
            meeting.save()
            # Associate attendants
            staff_ids = form.cleaned_data.get('attendants').split(',')
            map(lambda x: x.delete(), meeting.meetingpaticipant_set.all())
            for id in staff_ids:
                staff = models.StaffProfile.objects.get(id=int(id))
                attendant = models.MeetingPaticipant(name=staff.name, email=staff.email,
                                                     phone=staff.phone_number, staff_id=staff.id,
                                                     )
                meeting.meetingpaticipant_set.add(attendant)

    return redirect(meeting_index)


def meeting_new(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = forms.MeetingForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # Create meeting
            m = models.Meeting(date_time=form.cleaned_data.get('datetime'),
                               purpose=form.cleaned_data.get('purpose'),
                               location=form.cleaned_data.get('location'))
            m.save()
            # Associate attendants
            staff_ids = form.cleaned_data.get('attendants').split(',')
            for id in staff_ids:
                staff = models.StaffProfile.objects.get(id=int(id))
                attendant = models.MeetingPaticipant(name=staff.name, email=staff.email,
                                                     phone=staff.phone_number, staff_id=staff.id,
                                                     )
                m.meetingpaticipant_set.add(attendant)

    return redirect(meeting_index)


# Create your views here.
def meeting_index(request):
    """Display page with list of sorted meetings
    """
    meeting_all = models.Meeting.objects.all().order_by("-date_time")
    staffs = models.StaffProfile.objects.all()
    # Prepare row & column / layout 3 columns
    meetings = list()
    row_cols = None
    for i in range(0, len(meeting_all)):
        if i % 3 == 0:
            # Add old row
            row_cols = list()
            meetings.append(row_cols)

        # Push object to columns
        record = meeting_all[i]
        setattr(record, 'attendants', ",".join([str(p.staff_id) for p in record.meetingpaticipant_set.all()]))
        row_cols.append(record)

    context = {
        'meetings': meetings,
        'staffs': staffs,
    }
    return render(request, 'schedule/meeting.html', context)


def plan_new(request):
    """Create new Plan.
    """
    if request.method == 'POST':
        # process form
        form = forms.PlanForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # Create plan
            dt_start = form.cleaned_data.get('start_date')
            dt_end = form.cleaned_data.get('due_date')
            content = form.cleaned_data.get('content')
            duration = (dt_end - dt_start).days
            status = form.cleaned_data.get('status')
            plan = models.Plan(start_date=dt_start, due_date=dt_end,
                               status=status, content=content, duration=duration)
            plan.save()
            # Associate staffs
            staff_ids = form.cleaned_data.get('staffs').split(',')
            for id in staff_ids:
                staff = models.StaffProfile.objects.get(id=int(id))
                plan.staffs.add(staff)

    return redirect(plan_index)


def plan_update(request, pk):
    """Update a Plan.
    """
    if request.method == 'POST':
        # process form
        form = forms.PlanForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # Update plan
            plan = get_object_or_404(models.Plan, pk=pk)
            dt_start = form.cleaned_data.get('start_date') or plan.start_date
            dt_end = form.cleaned_data.get('due_date') or plan.due_date
            plan.start_date = dt_start
            plan.due_date = dt_end
            plan.content = form.cleaned_data.get('content') or plan.content
            plan.duration = (dt_end - dt_start).days
            plan.status = form.cleaned_data.get('status') or plan.status
            plan.save()
            # Associate staffs
            staff_ids = form.cleaned_data.get('staffs').split(',')
            plan.staffs.clear()
            for id in staff_ids:
                staff = models.StaffProfile.objects.get(id=int(id))
                plan.staffs.add(staff)

    return redirect(plan_index)


def plan_delete(request, pk):
    """Delete Plan.
    """
    plan = get_object_or_404(models.Plan, pk=pk)
    plan.delete()
    return redirect(plan_index())


def plan_index(request):
    """Display page with list of plans
    """
    plan_all = models.Plan.objects.all().order_by("-due_date")
    staffs = models.StaffProfile.objects.all()
    # Prepare row & column / layout 3 columns
    plans = list()
    row_cols = None
    for i in range(0, len(plan_all)):
        if i % 3 == 0:
            # Add old row
            row_cols = list()
            plans.append(row_cols)

        # Push object to columns
        record = plan_all[i]
        setattr(record, 'staffs_ref', ",".join([str(p.id) for p in record.staffs.all()]))
        row_cols.append(record)

    context = {
        'plans': plans,
        'staffs': staffs,
    }
    return render(request, 'schedule/plan.html', context)


def event_update_or_create(request):
    """Update exist event or create new event.
    """
    if request.method == 'POST':
        # process form
        form = forms.EventForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # Update or get event
            data = form.cleaned_data
            event_id = data.get('id')
            date = data.get('date')
            title = data.get('title')
            content = data.get('content')
            location = data.get('location')
            if event_id:
                # Request to update existing event
                event = get_object_or_404(models.Event, pk=event_id)
                event.date = date or event.date
                event.title = title or event.title
                event.content = content or event.content
                event.location = location or event.location
                event.save()
            else:
                # New event
                event = models.Event(date=date, title=title,
                                     content=content, location=location)
                event.save()
    return redirect(event_index)


def event_delete(request, pk):
    """Delete event
    """
    event = get_object_or_404(models.Event, pk=pk)
    event.delete()
    return redirect(event_index)


def event_json(request):
    """Return Events in JSON format.
    """
    if request.method == 'POST':
        # Extra parameters & return data
        events = models.Event.objects.all()
        response_data = []
        colors = ["#2b5797", "#9f00a7", "#5444CB", "#b91d47", "color5"]
        for e in events:
            print e.date.isoformat()
            response_data.append({'title': e.title,
                                  'start': e.date.isoformat(),
                                  'content': e.content,
                                  'location': e.location,
                                  'event_id': e.id,
                                  'delete_url': reverse('delete_event', kwargs={'pk': e.id}),
                                  'color': colors[e.id % 5]})
    else:
        response_data = []
    return HttpResponse(json.dumps(response_data), content_type="application/json")


def event_index(request):
    """Display page models.
    """
    return render(request, 'schedule/event.html')


def schedule_index(request, **kwargs):
    """Display teaching data table
    """
    # Dict of staff & list of schedule items
    staffs_schedule = dict()
    schedule_items = models.TeachingSchedule.objects.all()
    # Sort by day & session
    schedule_items = sorted(schedule_items, key=lambda x: (x.day, x.session))
    for item in schedule_items:
        staffs_schedule.setdefault(item.staff_id, [])
        staffs_schedule[item.staff_id].append(item)

    # Construct columns % row on data table
    data_tables = []
    for staff_id, items in staffs_schedule.iteritems():
        row = [[] for i in range(0, 8)]
        # First column - staff name
        row[0] = models.StaffProfile.objects.get(id=staff_id)
        # Remaining columns - days in week
        for i in range(1, len(row)):
            # Put day's items in session order
            cols = []
            for j in range(1, 5):
                # Check next item
                if items:
                    next_item = items[0]
                    if int(next_item.session) == j and int(next_item.day) == i:
                        cols.append(next_item)
                        items.pop(0)
                        continue
                cols.append(models.TeachingSchedule())
            row[i] = cols
        data_tables.append(row)

    day_choices = [{'id': i[0], 'value': i[1]}
                   for i in models.TeachingSchedule.DAY_CHOICES]
    subject_choices = [{'id': i[0], 'value': i[1]}
                        for i in models.TeachingSchedule.SUBJECT_CHOICES]
    session_choices = [{'id': i[0], 'value': i[1]}
                        for i in models.TeachingSchedule.SESSION_CHOICES]
    context = {
        "teacher_schedule": data_tables,
        "day_choices": day_choices,
        "session_choices": session_choices,
        "subject_choices": subject_choices,
        "teacher_list": models.StaffProfile.objects.all()
    }
    return render(request, 'schedule/teaching_sched.html', context)


def schedule_delete(request, pk):
    """Delete schedule
    """
    item = get_object_or_404(models.TeachingSchedule, pk=pk)
    item.delete()
    return redirect(schedule_index)


def schedule_update_or_create(request):
    """Update current schedule or create new
    """
    if request.method == 'POST':
        # process form
        form = forms.ScheduleForm(request.POST)
        message = dict()
        # check whether it's valid:
        if not form.is_valid():
            messages.add_message(request, messages.ERROR, form.errors)
        else:
            # Update or get event
            data = form.cleaned_data
            item_id = data.get('id')
            day = data.get('day')
            session = data.get('session')
            subject = data.get('subject')
            cls = data.get('classes')
            staff = models.StaffProfile.objects.get(id=data.get('staff'))
            room = data.get('room')
            # Check if staff available
            results = models.TeachingSchedule.objects.filter(**{'staff': data.get('staff'),
                                                             'session': session,
                                                             'day': day})
            if (results and results[0].id != item_id) or (results and not item_id):
                # messages.add_message(request, level, message, extra_tags='', fail_silently=False)
                messages.add_message(request, messages.ERROR, "Teacher already busy on that session!")
            else:
                if item_id:
                    # Request to update existing item
                    item = get_object_or_404(models.TeachingSchedule, pk=item_id)
                    item.day = day
                    item.session = session
                    item.subject = subject
                    item.classes = cls
                    item.staff = staff
                    item.room = room
                    item.save()
                else:
                    # New Item
                    item = models.TeachingSchedule(staff=staff, day=day,
                                                   session=session, subject=subject,
                                                   classes=cls, room=room)
                    item.save()
    return redirect(schedule_index)
