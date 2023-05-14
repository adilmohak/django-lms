from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from accounts.models import User, Student
from app.models import Session, Semester
from course.models import Course
from accounts.decorators import lecturer_required, student_required
from .models import TakenCourse, Result

#pdf
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, JsonResponse

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, LongTable
from reportlab.lib.styles import getSampleStyleSheet, black, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY,TA_LEFT,TA_CENTER,TA_RIGHT
from reportlab.platypus.tables import Table
from reportlab.lib.units import inch
from reportlab.lib import colors
from .models import *

cm = 2.54

# ########################################################
# Score Add & Add for
# ########################################################
@login_required
@lecturer_required
def add_score(request):
    """ 
    Shows a page where a lecturer will select a course allocated to him for score entry.
    in a specific semester and session 

    """
    current_session = Session.objects.get(is_current_session=True)
    current_semester = get_object_or_404(Semester, is_current_semester=True, session=current_session)
    # semester = Course.objects.filter(allocated_course__lecturer__pk=request.user.id, semester=current_semester)
    courses = Course.objects.filter(allocated_course__lecturer__pk=request.user.id).filter(semester=current_semester)
    context = {
        "current_session": current_session,
        "current_semester": current_semester,
        "courses": courses,
    }
    return render(request, 'result/add_score.html', context)


@login_required
@lecturer_required
def add_score_for(request, id):
    """
    Shows a page where a lecturer will add score for students that are taking courses allocated to him
    in a specific semester and session 
    """
    current_session = Session.objects.get(is_current_session=True)
    current_semester = get_object_or_404(Semester, is_current_semester=True, session=current_session)
    if request.method == 'GET':
        courses = Course.objects.filter(allocated_course__lecturer__pk=request.user.id).filter(
            semester=current_semester)
        course = Course.objects.get(pk=id)
        # myclass = Class.objects.get(lecturer__pk=request.user.id)
        # myclass = get_object_or_404(Class, lecturer__pk=request.user.id)

        # students = TakenCourse.objects.filter(course__allocated_course__lecturer__pk=request.user.id).filter(
        #     course__id=id).filter(student__allocated_student__lecturer__pk=request.user.id).filter(
        #         course__semester=current_semester)
        students = TakenCourse.objects.filter(course__allocated_course__lecturer__pk=request.user.id).filter(
            course__id=id).filter(course__semester=current_semester)
        context = {
            "title": "Submit Score | DjangoSMS",
            "courses": courses,
            "course": course,
            # "myclass": myclass,
            "students": students,
            "current_session": current_session,
            "current_semester": current_semester,
        }
        return render(request, 'result/add_score_for.html', context)

    if request.method == 'POST':
        ids = ()
        data = request.POST.copy()
        data.pop('csrfmiddlewaretoken', None)  # remove csrf_token
        for key in data.keys():
            ids = ids + (str(key),)  # gather all the all students id (i.e the keys) in a tuple
        for s in range(0, len(ids)):  # iterate over the list of student ids gathered above
            student = TakenCourse.objects.get(id=ids[s])
            # print(student)
            # print(student.student)
            # print(student.student.department.id)
            courses = Course.objects.filter(level=student.student.level).filter(program__pk=student.student.department.id).filter(
                semester=current_semester)  # all courses of a specific level in current semester
            total_credit_in_semester = 0
            for i in courses:
                if i == courses.count():
                    break
                else:
                    total_credit_in_semester += int(i.credit)
            score = data.getlist(ids[s])  # get list of score for current student in the loop
            assignment = score[0]  # subscript the list to get the fisrt value > ca score
            mid_exam = score[1]  # do the same for exam score
            quiz = score[2]
            attendance = score[3]
            final_exam = score[4]
            obj = TakenCourse.objects.get(pk=ids[s])  # get the current student data
            obj.assignment = assignment  # set current student assignment score
            obj.mid_exam = mid_exam  # set current student mid_exam score
            obj.quiz = quiz  # set current student quiz score
            obj.attendance = attendance  # set current student attendance score
            obj.final_exam = final_exam  # set current student final_exam score

            obj.total = obj.get_total(assignment=assignment, mid_exam=mid_exam, quiz=quiz, attendance=attendance, final_exam=final_exam)
            obj.grade = obj.get_grade(total=obj.total)

            # obj.total = obj.get_total(assignment, mid_exam, quiz, attendance, final_exam)
            # obj.grade = obj.get_grade(assignment, mid_exam, quiz, attendance, final_exam)

            obj.point = obj.get_point(grade=obj.grade)

            obj.comment = obj.get_comment(grade=obj.grade)
            # obj.carry_over(obj.grade)
            # obj.is_repeating()
            obj.save()
            gpa = obj.calculate_gpa(total_credit_in_semester)
            cgpa = obj.calculate_cgpa()

            try:
                a = Result.objects.get(student=student.student, semester=current_semester, session=current_session, level=student.student.level)
                a.gpa = gpa
                a.cgpa = cgpa
                a.save()
            except:
                Result.objects.get_or_create(student=student.student, gpa=gpa, semester=current_semester,
                                             session=current_session, level=student.student.level)

            # try:
            #     a = Result.objects.get(student=student.student, semester=current_semester, level=student.student.level)
            #     a.gpa = gpa
            #     a.cgpa = cgpa
            #     a.save()
            # except:
            #     Result.objects.get_or_create(student=student.student, gpa=gpa, semester=current_semester, level=student.student.level)

        messages.success(request, 'Successfully Recorded! ')
        return HttpResponseRedirect(reverse_lazy('add_score_for', kwargs={'id': id}))
    return HttpResponseRedirect(reverse_lazy('add_score_for', kwargs={'id': id}))
# ########################################################


@login_required
@student_required
def grade_result(request):
    student = Student.objects.get(student__pk=request.user.id)
    courses = TakenCourse.objects.filter(student__student__pk=request.user.id).filter(course__level=student.level)
    # total_credit_in_semester = 0
    results = Result.objects.filter(student__student__pk=request.user.id)

    result_set = set()

    for result in results:
        result_set.add(result.session)

    sorted_result = sorted(result_set)

    total_first_semester_credit = 0
    total_sec_semester_credit = 0
    for i in courses:
        if i.course.semester == "First":
            total_first_semester_credit += int(i.course.credit)
        if i.course.semester == "Second":
            total_sec_semester_credit += int(i.course.credit)

    previousCGPA = 0
    # previousLEVEL = 0
    # calculate_cgpa
    for i in results:
        previousLEVEL = i.level
        try:
            a = Result.objects.get(student__student__pk=request.user.id, level=previousLEVEL, semester="Second")
            previousCGPA = a.cgpa
            break
        except:
            previousCGPA = 0

    context = {
        "courses": courses,
        "results": results,
        "sorted_result": sorted_result,
        "student": student,
        'total_first_semester_credit': total_first_semester_credit,
        'total_sec_semester_credit': total_sec_semester_credit,
        'total_first_and_second_semester_credit': total_first_semester_credit + total_sec_semester_credit,
        "previousCGPA": previousCGPA,
    }

    return render(request, 'result/grade_results.html', context)


@login_required
@student_required
def assessment_result(request):
    student = Student.objects.get(student__pk=request.user.id)
    courses = TakenCourse.objects.filter(student__student__pk=request.user.id, course__level=student.level)
    result = Result.objects.filter(student__student__pk=request.user.id)

    context = {
        "courses": courses,
        "result": result,
        "student": student,
    }
    
    return render(request, 'result/assessment_results.html', context)


@login_required
@lecturer_required
def result_sheet_pdf_view(request, id):
    current_semester = Semester.objects.get(is_current_semester=True)
    current_session = Session.objects.get(is_current_session=True)
    result = TakenCourse.objects.filter(course__pk=id)
    course = get_object_or_404(Course, id=id)
    no_of_pass = TakenCourse.objects.filter(course__pk=id, comment="PASS").count()
    no_of_fail = TakenCourse.objects.filter(course__pk=id, comment="FAIL").count()
    fname = str(current_semester) + '_semester_' + str(current_session) + '_' + str(course) + '_resultSheet.pdf'
    fname = fname.replace("/", "-")
    flocation = settings.MEDIA_ROOT + "/result_sheet/" + fname

    doc = SimpleDocTemplate(flocation, rightMargin=0, leftMargin=6.5 * cm, topMargin=0.3 * cm, bottomMargin=0)
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle( name="ParagraphTitle", fontSize=11, fontName="FreeSansBold"))
    Story = [Spacer(1,.2)]
    style = styles["Normal"]

    # picture = request.user.picture
    # l_pic = Image(picture, 1*inch, 1*inch)
    # l_pic.__setattr__("_offs_x", 200)
    # l_pic.__setattr__("_offs_y", -130)
    # Story.append(l_pic)

    # logo = settings.MEDIA_ROOT + "/logo/logo-mini.png"
    # im_logo = Image(logo, 1*inch, 1*inch)
    # im_logo.__setattr__("_offs_x", -218)
    # im_logo.__setattr__("_offs_y", -60)
    # Story.append(im_logo)

    print("\nsettings.MEDIA_ROOT", settings.MEDIA_ROOT)
    print("\nsettings.STATICFILES_DIRS[0]", settings.STATICFILES_DIRS[0])
    logo = settings.STATICFILES_DIRS[0] + "/img/logo.png"
    im = Image(logo, 1*inch, 1*inch)
    im.__setattr__("_offs_x", -200)
    im.__setattr__("_offs_y", -45)
    Story.append(im)
    
    style = getSampleStyleSheet()
    normal = style["Normal"]
    normal.alignment = TA_CENTER
    normal.fontName = "Helvetica"
    normal.fontSize = 12
    normal.leading = 15
    title = "<b> "+str(current_semester) + " Semester " + str(current_session) + " Result Sheet</b>" 
    title = Paragraph(title.upper(), normal)
    Story.append(title)
    Story.append(Spacer(1,0.1*inch))

    style = getSampleStyleSheet()
    normal = style["Normal"]
    normal.alignment = TA_CENTER
    normal.fontName = "Helvetica"
    normal.fontSize = 10
    normal.leading = 15
    title = "<b>Course lecturer: " + request.user.get_full_name + "</b>"
    title = Paragraph(title.upper(), normal)
    Story.append(title)
    Story.append(Spacer(1,0.1*inch))

    normal = style["Normal"]
    normal.alignment = TA_CENTER
    normal.fontName = "Helvetica"
    normal.fontSize = 10
    normal.leading = 15
    level = result.filter(course_id=id).first()
    title = "<b>Level: </b>" + str(level.course.level)
    title = Paragraph(title.upper(), normal)
    Story.append(title)
    Story.append(Spacer(1,.6*inch))
    
    elements = []
    count = 0
    header = [('S/N', 'ID NO.', 'FULL NAME', 'TOTAL', 'GRADE', 'POINT', 'COMMENT')]

    table_header = Table(header, [inch], [0.5*inch])
    table_header.setStyle(
        TableStyle([
            ('BACKGROUND',(0,0),(-1,-1),colors.black),
            ('TEXTCOLOR',(1,0),(-1,-1),colors.white),
            ('TEXTCOLOR',(0,0),(0,0),colors.cyan),
            ('ALIGN',(0,0),(-1,-1),'CENTER'),
            ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
            ('BOX',(0,0),(-1,-1),1,colors.black),
            ]))
    Story.append(table_header)

    for student in result:

        data = [(count+1, student.student.student.username.upper(), Paragraph(student.student.student.get_full_name.capitalize(), styles['Normal']),  
        student.total, student.grade, student.point, student.comment)]
        color = colors.black
        if student.grade == 'F':
            color = colors.red
        count += 1

        t_body = Table(data, colWidths=[inch])
        t_body.setStyle(
            TableStyle([
                ('INNERGRID', (0,0), (-1,-1), 0.05, colors.black),
                ('BOX', (0,0), (-1,-1), 0.1, colors.black),
                ]))
        Story.append(t_body)

    Story.append(Spacer(1,1*inch))
    style_right = ParagraphStyle(name='right', parent=styles['Normal'], alignment=TA_RIGHT)
    tbl_data = [
    [Paragraph("<b>Date:</b>_____________________________", styles["Normal"]), Paragraph("<b>No. of PASS:</b> " + str(no_of_pass), style_right)],
    [Paragraph("<b>Siganture / Stamp:</b> _____________________________", styles["Normal"]), Paragraph("<b>No. of FAIL: </b>" + str(no_of_fail), style_right)]]
    tbl = Table(tbl_data)
    Story.append(tbl)

    doc.build(Story)

    fs = FileSystemStorage(settings.MEDIA_ROOT + "/result_sheet")
    with fs.open(fname) as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename=' + fname + ''
        return response
    return response


@login_required
@student_required
def course_registration_form(request):
    current_semester = Semester.objects.get(is_current_semester=True)
    current_session = Session.objects.get(is_current_session=True)
    courses = TakenCourse.objects.filter(student__student__id=request.user.id)
    fname = request.user.username + '.pdf'
    fname = fname.replace("/", "-")
    # flocation = '/tmp/' + fname
    # print(MEDIA_ROOT + "\\" + fname)
    flocation = settings.MEDIA_ROOT + "/registration_form/" + fname
    doc = SimpleDocTemplate(flocation, rightMargin=15, leftMargin=15, topMargin=0, bottomMargin=0)
    styles = getSampleStyleSheet()

    Story = [Spacer(1,0.5)]
    Story.append(Spacer(1,0.4*inch))
    style = styles["Normal"]

    style = getSampleStyleSheet()
    normal = style["Normal"]
    normal.alignment = TA_CENTER
    normal.fontName = "Helvetica"
    normal.fontSize = 12
    normal.leading = 18
    title = "<b>EZOD UNIVERSITY OF TECHNOLOGY, ADAMA</b>" 
    title = Paragraph(title.upper(), normal)
    Story.append(title)
    style = getSampleStyleSheet()
    
    school = style["Normal"]
    school.alignment = TA_CENTER
    school.fontName = "Helvetica"
    school.fontSize = 10
    school.leading = 18
    school_title = "<b>SCHOOL OF ELECTRICAL ENGINEERING & COMPUTING</b>"
    school_title = Paragraph(school_title.upper(), school)
    Story.append(school_title)

    style = getSampleStyleSheet()
    Story.append(Spacer(1,0.1*inch))
    department = style["Normal"]
    department.alignment = TA_CENTER
    department.fontName = "Helvetica"
    department.fontSize = 9
    department.leading = 18
    department_title = "<b>DEPARTMENT OF COMPUTER SCIENCE & ENGINEERING</b>"
    department_title = Paragraph(department_title, department)
    Story.append(department_title)
    Story.append(Spacer(1,.3*inch))
    
    title = "<b><u>STUDENT COURSE REGISTRATION FORM</u></b>"
    title = Paragraph(title.upper(), normal)
    Story.append(title)
    student = Student.objects.get(student__pk=request.user.id)

    style_right = ParagraphStyle(name='right', parent=styles['Normal'])
    tbl_data = [
        [Paragraph("<b>Registration Number : " + request.user.username.upper() + "</b>", styles["Normal"])],
        [Paragraph("<b>Name : " + request.user.get_full_name.upper() + "</b>", styles["Normal"])],
        [Paragraph("<b>Session : " + current_session.session.upper() + "</b>", styles["Normal"]), Paragraph("<b>Level: " + student.level + "</b>", styles["Normal"])
        ]]
    tbl = Table(tbl_data)
    Story.append(tbl)
    Story.append(Spacer(1, 0.6*inch))

    style = getSampleStyleSheet()
    semester = style["Normal"]
    semester.alignment = TA_LEFT
    semester.fontName = "Helvetica"
    semester.fontSize = 9
    semester.leading = 18
    semester_title = "<b>FIRST SEMESTER</b>"
    semester_title = Paragraph(semester_title, semester)
    Story.append(semester_title)

    elements = []

    # FIRST SEMESTER
    count = 0
    header = [('S/No', 'Course Code', 'Course Title', 'Unit', Paragraph('Name, Siganture of course lecturer & Date', style['Normal']))]
    table_header = Table(header,1*[1.4*inch], 1*[0.5*inch])
    table_header.setStyle(
        TableStyle([
                ('ALIGN',(-2,-2), (-2,-2),'CENTER'),
                ('VALIGN',(-2,-2), (-2,-2),'MIDDLE'),
                ('ALIGN',(1,0), (1,0),'CENTER'),
                ('VALIGN',(1,0), (1,0),'MIDDLE'),
                ('ALIGN',(0,0), (0,0),'CENTER'),
                ('VALIGN',(0,0), (0,0),'MIDDLE'),
                ('ALIGN',(-4,0), (-4,0),'LEFT'),
                ('VALIGN',(-4,0), (-4,0),'MIDDLE'),
                ('ALIGN',(-3,0), (-3,0),'LEFT'),
                ('VALIGN',(-3,0), (-3,0),'MIDDLE'),
                ('TEXTCOLOR',(0,-1),(-1,-1),colors.black),
                ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                ('BOX', (0,0), (-1,-1), 0.25, colors.black),
            ]))
    Story.append(table_header)

    first_semester_unit = 0
    for course in courses:
        if course.course.semester == FIRST:
            first_semester_unit += int(course.course.credit)
            data = [(count+1, course.course.code.upper(), Paragraph(course.course.title, style['Normal']), course.course.credit, '')]
            color = colors.black
            count += 1
            table_body=Table(data,1*[1.4*inch], 1*[0.3*inch])
            table_body.setStyle(
                TableStyle([
                    ('ALIGN',(-2,-2), (-2,-2),'CENTER'),
                    ('ALIGN',(1,0), (1,0),'CENTER'),
                    ('ALIGN',(0,0), (0,0),'CENTER'),
                    ('ALIGN',(-4,0), (-4,0),'LEFT'),
                    ('TEXTCOLOR',(0,-1),(-1,-1),colors.black),
                    ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                    ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                    ]))
            Story.append(table_body)

    style = getSampleStyleSheet()
    semester = style["Normal"]
    semester.alignment = TA_LEFT
    semester.fontName = "Helvetica"
    semester.fontSize = 8
    semester.leading = 18
    semester_title = "<b>Total Second First Credit : " + str(first_semester_unit) + "</b>"
    semester_title = Paragraph(semester_title, semester)
    Story.append(semester_title)

    # FIRST SEMESTER ENDS HERE
    Story.append(Spacer(1, 0.6*inch))

    style = getSampleStyleSheet()
    semester = style["Normal"]
    semester.alignment = TA_LEFT
    semester.fontName = "Helvetica"
    semester.fontSize = 9
    semester.leading = 18
    semester_title = "<b>SECOND SEMESTER</b>"
    semester_title = Paragraph(semester_title, semester)
    Story.append(semester_title)
    # SECOND SEMESTER
    count = 0
    header = [('S/No', 'Course Code', 'Course Title', 'Unit', Paragraph('<b>Name, Signature of course lecturer & Date</b>', style['Normal']))]
    table_header = Table(header,1*[1.4*inch], 1*[0.5*inch])
    table_header.setStyle(
        TableStyle([
                ('ALIGN',(-2,-2), (-2,-2),'CENTER'),
                ('VALIGN',(-2,-2), (-2,-2),'MIDDLE'),
                ('ALIGN',(1,0), (1,0),'CENTER'),
                ('VALIGN',(1,0), (1,0),'MIDDLE'),
                ('ALIGN',(0,0), (0,0),'CENTER'),
                ('VALIGN',(0,0), (0,0),'MIDDLE'),
                ('ALIGN',(-4,0), (-4,0),'LEFT'),
                ('VALIGN',(-4,0), (-4,0),'MIDDLE'),
                ('ALIGN',(-3,0), (-3,0),'LEFT'),
                ('VALIGN',(-3,0), (-3,0),'MIDDLE'),
                ('TEXTCOLOR',(0,-1),(-1,-1),colors.black),
                ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                ('BOX', (0,0), (-1,-1), 0.25, colors.black),
            ]))
    Story.append(table_header)

    second_semester_unit = 0
    for course in courses:
        if course.course.semester == SECOND:
            second_semester_unit += int(course.course.credit)
            data = [(count+1, course.course.code.upper(), Paragraph(course.course.title, style['Normal']), course.course.credit, '')]
            color = colors.black
            count += 1
            table_body=Table(data,1*[1.4*inch], 1*[0.3*inch])
            table_body.setStyle(
                TableStyle([
                    ('ALIGN',(-2,-2), (-2,-2),'CENTER'),
                    ('ALIGN',(1,0), (1,0),'CENTER'),
                    ('ALIGN',(0,0), (0,0),'CENTER'),
                    ('ALIGN',(-4,0), (-4,0),'LEFT'),
                    ('TEXTCOLOR',(0,-1),(-1,-1),colors.black),
                    ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                    ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                    ]))
            Story.append(table_body)

    style = getSampleStyleSheet()
    semester = style["Normal"]
    semester.alignment = TA_LEFT
    semester.fontName = "Helvetica"
    semester.fontSize = 8
    semester.leading = 18
    semester_title = "<b>Total Second Semester Credit : " + str(second_semester_unit) + "</b>"
    semester_title = Paragraph(semester_title, semester)
    Story.append(semester_title)

    Story.append(Spacer(1, 2))
    style = getSampleStyleSheet()
    certification = style["Normal"]
    certification.alignment = TA_JUSTIFY
    certification.fontName = "Helvetica"
    certification.fontSize = 8
    certification.leading = 18
    student = Student.objects.get(student__pk=request.user.id)
    certification_text = "CERTIFICATION OF REGISTRATION: I certify that <b>" + str(request.user.get_full_name.upper()) + "</b>\
    has been duly registered for the <b>" + student.level + " level </b> of study in the department\
    of COMPUTER SICENCE & ENGINEERING and that the courses and credits registered are as approved by the senate of the University"
    certification_text = Paragraph(certification_text, certification)
    Story.append(certification_text)

    # FIRST SEMESTER ENDS HERE

    logo = settings.STATICFILES_DIRS[0] + "/img/logo.png"
    im_logo = Image(logo, 1*inch, 1*inch)
    im_logo.__setattr__("_offs_x", -218)
    im_logo.__setattr__("_offs_y", 480)
    Story.append(im_logo)

    picture =  settings.BASE_DIR + request.user.get_picture()
    im = Image(picture, 1.0*inch, 1.0*inch)
    im.__setattr__("_offs_x", 218)
    im.__setattr__("_offs_y", 550)
    Story.append(im)

    doc.build(Story)
    fs = FileSystemStorage(settings.MEDIA_ROOT + "/registration_form")
    with fs.open(fname) as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename='+fname+''
        return response
    return response
