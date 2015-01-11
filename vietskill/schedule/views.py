from django.shortcuts import render, get_object_or_404, redirect
from vietskill import models


# Create your views here.
def meeting_index(request):
    """Display page with list of sorted meetings
    """
    meeting_all = models.Meeting.objects.all().order_by("date_time")

    # Prepare row & column / layout 3 columns
    meetings = list()
    row_cols = None
    for i in range(0, len(meeting_all)):
        print i % 3
        if i % 3 == 0:
            # Add old row
            row_cols = list()
            meetings.append(row_cols)

        # Push object to columns
        row_cols.append(meeting_all[i])

    context = {
        'meetings': meetings
    }
    print meetings
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