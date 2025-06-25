from django.shortcuts import render, redirect, get_object_or_404
from .decorators import role_required
from .models import Courses, ClassSlotSetup, Teacher, Lesson, CourseLessonLink, ClassSlotGroup,StudentSchedule,CourseProgressionMap
from .forms import LessonForm
from datetime import datetime
from collections import defaultdict, Counter
from django.db.models import Case, When, Value, IntegerField
import openpyxl
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

@role_required('administrator')
def general_setup(request):
    setup_items = [
        {'name': 'Courses', 'url': 'course_list', 'description': 'Manage available courses'},
        # {'name': 'Class Slots', 'url': '#', 'description': 'Manage class schedules and slots (coming soon)'},
        # {'name': 'Syllabus Setup', 'url': '#', 'description': 'Upload and organize syllabus (coming soon)'},
    ]
    return render(request, 'adminhub/setup/general_setup.html', {'setup_items': setup_items})

@role_required('administrator')
def course_list(request):
    courses = Courses.objects.filter(deleted=False).order_by('code')
    return render(request, 'adminhub/setup/course_list.html', {'courses': courses})

@role_required('administrator')
def course_form_view(request):
    course_id = request.GET.get('id')
    course = None

    if course_id:
        course = get_object_or_404(Courses, id=course_id, deleted=False)

    if request.method == 'POST':
        code = request.POST.get('code', '').strip()
        description = request.POST.get('description', '').strip()

        if course:
            course.code = code
            course.description = description
        else:
            course = Courses(code=code, description=description, deleted=False, archived=False)

        course.save()
        return redirect('course_list')

    return render(request, 'adminhub/setup/course_form.html', {'course': course})

@role_required('administrator')
def course_delete(request, pk):
    # Check if the user is authenticated
    if 'user_id' not in request.session:
        return redirect('login')  # Redirect to login if not authenticated

    course = get_object_or_404(Courses, pk=pk)
    course.deleted = True
    course.save()
    return redirect('course_list')

@role_required('administrator')
def class_slot_setup_view(request):
    feedback_message = None
    error_message = None

    if request.method == 'POST':
        day = request.POST.get('day')
        time = request.POST.get('time')
        teacher_id = request.POST.get('teacher')
        course_id = request.POST.get('course')

        try:
            teacher = Teacher.objects.get(id=teacher_id)
            course = Courses.objects.get(id=course_id)
            time_obj = datetime.strptime(time, '%H:%M').time()

            ClassSlotSetup.objects.create(
                day=day,
                time=time_obj,
                teacher=teacher,
                course=course
            )
            feedback_message = "Class slot setup saved successfully!"
        except Exception as e:
            error_message = f"Error saving setup: {str(e)}"

    slots = ClassSlotSetup.objects.select_related('teacher', 'course').all()
    teachers = Teacher.objects.all().order_by('full_name')
    courses = Courses.objects.filter(deleted=False)

    context = {
        'slots': slots,
        'teachers': teachers,
        'courses': courses,
        'days': [day for day, _ in ClassSlotSetup.DAYS_OF_WEEK],
        'feedback_message': feedback_message,
        'error_message': error_message
    }

    return render(request, 'adminhub/setup/class_slot_setup.html', context)

@role_required('administrator')
def lesson_list(request):
    lessons = Lesson.objects.all()
    return render(request, 'adminhub/lessons/lesson_list.html', {'lessons': lessons})


@role_required('administrator')
def lesson_form(request):
    lesson_id = request.GET.get('id')
    instance = get_object_or_404(Lesson, id=lesson_id) if lesson_id else None

    if request.method == 'POST':
        form = LessonForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect('lesson_list')
    else:
        form = LessonForm(instance=instance)

    return render(request, 'adminhub/lessons/lesson_form.html', {'form': form, 'lesson': instance})


@role_required('administrator')
def lesson_delete(request, id):
    lesson = get_object_or_404(Lesson, id=id)
    lesson.delete()
    return redirect('lesson_list')

@role_required('administrator')
def course_lesson_link_list(request):
    if request.method == 'POST':
        course_id = request.POST.get('course_id')
        lesson_id = request.POST.get('lesson_id')
        sequence = request.POST.get('sequence')
        if course_id and lesson_id:
            CourseLessonLink.objects.create(
                course_id=course_id,
                lesson_id=lesson_id,
                sequence=sequence
            )
            return redirect('course_lesson_link_list')

    courses = Courses.objects.filter(deleted=False)
    lessons = Lesson.objects.all()
    links = CourseLessonLink.objects.select_related('course', 'lesson').order_by('course__code', 'sequence')

    # Group links by course
    grouped = {}
    for link in links:
        grouped.setdefault(link.course.id, {
            'course': link.course,
            'links': []
        })['links'].append(link)

    return render(request, 'adminhub/lessons/course_lesson_link_list.html', {
        'courses': courses,
        'lessons': lessons,
        'linked_data': grouped.values()
    })


@role_required('administrator')
def unlink_lesson(request, id):
    link = get_object_or_404(CourseLessonLink, id=id)
    link.delete()
    return redirect('course_lesson_link_list')


@role_required('administrator')
def class_slot_group_list(request):
    from django.db.models import Q  # ensure Q is imported

    query = request.GET.get('q', '').strip()
    selected_day = request.GET.get('day', '').strip()
    selected_program = request.GET.get('program', '').strip()

    # ✅ Step 1: Initialize queryset first
    groups = ClassSlotGroup.objects.select_related('teacher')

    # ✅ Step 2: Apply dropdown filters
    if selected_day:
        groups = groups.filter(day__iexact=selected_day)
    if selected_program:
        groups = groups.filter(program__iexact=selected_program)

    # ✅ Step 3: Apply search query filter
    if query:
        groups = groups.filter(
            Q(program__icontains=query) |
            Q(day__icontains=query) |
            Q(time__icontains=query) |
            Q(teacher__full_name__icontains=query)
        )

    day_order = Case(
        When(day__iexact='MONDAY', then=Value(1)),
        When(day__iexact='TUESDAY', then=Value(2)),
        When(day__iexact='WEDNESDAY', then=Value(3)),
        When(day__iexact='THURSDAY', then=Value(4)),
        When(day__iexact='FRIDAY', then=Value(5)),
        When(day__iexact='SATURDAY', then=Value(6)),
        When(day__iexact='SUNDAY', then=Value(7)),
        default=Value(99),  # push unrecognized values to the end
        output_field=IntegerField()
    )

    # Annotate and apply improved order
    groups = groups.annotate(day_order=day_order).order_by('day_order', 'time', 'program', 'teacher__full_name')

    # Process schedules and status
    group_schedules = defaultdict(list)
    status_summary = defaultdict(Counter)

    schedules = StudentSchedule.objects.select_related('student').filter(class_slot_group__in=groups)

    for s in schedules:
        group_schedules[s.class_slot_group_id].append({
            'student': s.student.full_name,
            'level': s.level,
            'status': s.status,
            'mode': s.mode
        })
        status_summary[s.class_slot_group_id][s.status.lower()] += 1

    programs = ClassSlotGroup.objects.values_list('program', flat=True).distinct()
    days = ClassSlotGroup.objects.values_list('day', flat=True).distinct()

    WEEKDAYS_ORDER = ['MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY', 'SATURDAY', 'SUNDAY']
    normalized_days = list(set(day.upper() for day in days))
    available_days_sorted = [d for d in WEEKDAYS_ORDER if d in normalized_days]

    context = {
        'groups': groups,
        'group_schedules': group_schedules,
        'status_summary': status_summary,
        'query': query,
        'available_programs': sorted(programs),
        'available_days': available_days_sorted,
        'selected_day': selected_day,
        'selected_program': selected_program
    }
    return render(request, 'adminhub/setup/class_slot_group_list.html', context)


@role_required('administrator')
def export_class_slot_groups(request):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Class Slot Groups"

    # Header row
    headers = ['Program', 'Day', 'Time', 'Teacher', 'Student Name', 'Level', 'Status', 'Mode']
    ws.append(headers)

    groups = ClassSlotGroup.objects.select_related('teacher').order_by('day', 'time', 'program')
    schedules = StudentSchedule.objects.select_related('student').filter(class_slot_group__in=groups)

    group_map = defaultdict(list)
    for s in schedules:
        group_map[s.class_slot_group_id].append(s)

    for group in groups:
        rows = group_map.get(group.id, [])
        if rows:
            for sched in rows:
                ws.append([
                    group.program,
                    group.day,
                    group.time.strftime('%H:%M'),
                    group.teacher.full_name,
                    sched.student.full_name,
                    sched.level,
                    sched.status,
                    sched.mode,
                ])
        else:
            # Include empty row for groups with no students
            ws.append([
                group.program,
                group.day,
                group.time.strftime('%H:%M'),
                group.teacher.full_name,
                '—', '—', '—', '—'
            ])

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=class_slot_groups.xlsx'
    wb.save(response)
    return response


@role_required('administrator')
def manage_course_pathways(request):
    courses = Courses.objects.filter(archived=False).order_by('description')

    if request.method == "POST":
        source_id = request.POST.get("source_course")
        target_id = request.POST.get("target_course")
        condition = request.POST.get("condition", "").strip()
        comment = request.POST.get("comment", "").strip()

        if source_id and target_id and source_id != target_id:
            CourseProgressionMap.objects.update_or_create(
                source_course_id=source_id,
                target_course_id=target_id,
                defaults={"condition": condition, "comment": comment}
            )

        return redirect("course_pathways")

    mappings = CourseProgressionMap.objects.select_related("source_course", "target_course").order_by(
        "source_course__description", "target_course__description"
    )

    return render(request, "adminhub/setup/course_pathways.html", {
        "courses": courses,
        "mappings": mappings
    })

@csrf_exempt
@role_required('administrator')
def ajax_add_course_pathway(request):
    if request.method == "POST":
        data = json.loads(request.body)
        source = data.get("source_course")
        target = data.get("target_course")
        condition = data.get("condition", "").strip()
        comment = data.get("comment", "").strip()
        source_level = data.get("source_level") 
        target_level = data.get("target_level") 


        if source and target and source != target:
            CourseProgressionMap.objects.update_or_create(
                source_course_id=source,
                target_course_id=target,
                defaults={"condition": condition, "comment": comment,
                            "source_level": source_level or None,
                            "target_level": target_level or None}
            )
            return JsonResponse({"status": "ok", "message": "Pathway mapping saved!"})
        return JsonResponse({"status": "fail", "message": "Invalid input."})

@csrf_exempt
@role_required('administrator')
def ajax_edit_course_pathway(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            mapping_id = data.get("id")
            source = data.get("source_course")
            target = data.get("target_course")
            condition = data.get("condition", "").strip()
            comment = data.get("comment", "").strip()

            if not mapping_id or not source or not target:
                return JsonResponse({"status": "fail", "message": "Missing required fields."})

            if str(source) == str(target):
                return JsonResponse({"status": "fail", "message": "Source and target cannot be the same course."})

            # Fetch and update the mapping
            mapping = CourseProgressionMap.objects.get(id=mapping_id)
            mapping.source_course_id = source
            mapping.target_course_id = target
            mapping.condition = condition
            mapping.comment = comment

            source_level = data.get("source_level")
            target_level = data.get("target_level")
            mapping.source_level = int(source_level) if source_level not in [None, ""] else None
            mapping.target_level = int(target_level) if target_level not in [None, ""] else None

            mapping.save()

            return JsonResponse({"status": "ok", "message": "Mapping updated successfully."})

        except CourseProgressionMap.DoesNotExist:
            return JsonResponse({"status": "fail", "message": "Mapping not found."})
        except Exception as e:
            return JsonResponse({"status": "fail", "message": f"Error: {str(e)}"})

@csrf_exempt
@role_required('administrator')
def ajax_delete_course_pathway(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            mapping_id = data.get("id")
            mapping = CourseProgressionMap.objects.get(id=mapping_id)
            mapping.delete()
            return JsonResponse({"status": "ok", "message": "Mapping deleted successfully."})
        except CourseProgressionMap.DoesNotExist:
            return JsonResponse({"status": "fail", "message": "Mapping not found."})
        except Exception as e:
            return JsonResponse({"status": "fail", "message": f"Error: {str(e)}"})


@role_required('administrator')
def course_pathway_map(request):
    mappings = CourseProgressionMap.objects.select_related("source_course", "target_course").all()
    courses_queryset = Courses.objects.filter(deleted=False)
    courses_map = {c.id: c for c in courses_queryset}

    course_levels = {}

    for m in mappings:
        if m.source_level is not None:
            if m.source_course_id not in course_levels or course_levels[m.source_course_id] > m.source_level:
                course_levels[m.source_course_id] = m.source_level

        if m.target_level is not None:
            if m.target_course_id not in course_levels or course_levels[m.target_course_id] > m.target_level:
                course_levels[m.target_course_id] = m.target_level

    grouped_levels = defaultdict(list)
    for course_id, level in course_levels.items():
        if course_id in courses_map:
            grouped_levels[level].append(courses_map[course_id])

    sorted_grouped_levels = sorted(grouped_levels.items())
    for level_num, course_group in sorted_grouped_levels:
        course_group.sort(key=lambda c: c.description)

    progression_table_data = []
    for m in mappings:
        relationship_type = ""
        if m.source_level is not None and m.target_level is not None:
            if m.target_level > m.source_level:
                relationship_type = "Progression"
            elif m.target_level == m.source_level:
                relationship_type = "Parallel"
            else:
                relationship_type = "Requisite"
        
        progression_table_data.append({
            'source_course_name': m.source_course.description,
            'target_course_name': m.target_course.description,
            'condition': m.condition,
            'comment': m.comment,
            'source_level': m.source_level,
            'target_level': m.target_level,
            'relationship_type': relationship_type,
        })

    # Sort the progression table data
    progression_table_data.sort(key=lambda x: (
        x['source_level'] if x['source_level'] is not None else float('inf'),
        x['source_course_name'],
        x['target_level'] if x['target_level'] is not None else float('inf'),
        x['target_course_name']
    ))

    # Assign directly without rowspan processing
    processed_table_data = progression_table_data

    context = {
        'grouped_levels': sorted_grouped_levels,
        'progression_table_data': processed_table_data,
    }
    return render(request, 'adminhub/course_pathway_map.html', context)

@role_required('administrator')
def export_progression_to_excel(request):
    selected_course = request.POST.get('selected_course')

    mappings = CourseProgressionMap.objects.select_related("source_course", "target_course")
    if selected_course:
        mappings = mappings.filter(source_course__description=selected_course)
    progression_table_data = []
    for m in mappings:
        relationship_type = ""
        if m.source_level is not None and m.target_level is not None:
            if m.target_level > m.source_level:
                relationship_type = "Progression"
            elif m.target_level == m.source_level:
                relationship_type = "Parallel"
            else:
                relationship_type = "Requisite"

        # Filter if selected_course is provided
        if selected_course:
            if selected_course not in [m.source_course.description, m.target_course.description]:
                continue

        progression_table_data.append({
            'source_course_name': m.source_course.description,
            'target_course_name': m.target_course.description,
            'condition': m.condition,
            'comment': m.comment,
            'source_level': m.source_level,
            'target_level': m.target_level,
            'relationship_type': relationship_type,
        })

    progression_table_data.sort(key=lambda x: (
        x['source_level'] if x['source_level'] is not None else float('inf'),
        x['source_course_name'],
        x['target_level'] if x['target_level'] is not None else float('inf'),
        x['target_course_name']
    ))

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Course Progression"

    headers = [
        "Source Course", "Source Level", "Relationship Type",
        "Target Course", "Target Level", "Condition", "Comment"
    ]
    ws.append(headers)

    for entry in progression_table_data:
        ws.append([
            entry['source_course_name'],
            entry['source_level'],
            entry['relationship_type'],
            entry['target_course_name'],
            entry['target_level'],
            entry['condition'],
            entry['comment']
        ])

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    filename = f"course_progression_{selected_course or 'all'}.xlsx"
    response['Content-Disposition'] = f'attachment; filename={filename}'
    wb.save(response)
    return response
