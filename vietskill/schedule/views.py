from django.shortcuts import render, get_object_or_404, redirect
from vietskill import models
from vietskill.schedule import forms


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


def plan_index(request):
    """Display page with list of plans
    """
    return render(request, 'schedule/plan.html')


def event_index(request):
    """Display page with list of events
    """
    return render(request, 'schedule/event.html')


def schedule_index(request):
    """Display teaching data table
    """
    return render(request, 'schedule/teaching_sched.html')