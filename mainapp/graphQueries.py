from django.db import connection
import numpy as np

def getStudentWisePLO(student_id):
    row = []
    for i in range(12):
        ploNum = f'PLO0{i + 1}'
        if i + 1 >= 10:
            ploNum = f'PLO{i + 1}'
        with connection.cursor() as cursor:
            cursor.execute('''
                SELECT AVG(TotalPlo.PLOpercentage) AS ActualPlo
                FROM (
                SELECT (PLO / TotalComark * 100) AS PLOpercentage
                FROM (
                        SELECT SUM(DISTINCT e.obtainedMarks) AS PLO, SUM(DISTINCT a.marks) AS TotalCoMark
                        FROM mainapp_enrollment_t en,
                            mainapp_evaluation_t e,
                            mainapp_assessment_t a,
                            mainapp_co_t c,
                            mainapp_plo_t p
                        WHERE en.student_id = '{}'
                            AND en.enrollmentID = e.enrollment_id
                            AND e.assessment_id = a.assessmentNo
                            AND a.co_id = c.id
                            AND c.plo_id = '{}'
                        GROUP BY en.section_id
                    ) ploPer
                )TotalPlo;
            '''.format(student_id, ploNum))
            temp = cursor.fetchone()
            if temp is not None:
                row.append((temp[0], ploNum))
    return row
    
def getDepartmentWisePLO():
    row = []
    for i in range(12):
        ploNum = f'PLO0{i + 1}'
        if i + 1 >= 10:
            ploNum = f'PLO{i + 1}'
        with connection.cursor() as cursor:
            cursor.execute('''
                SELECT d.departmentID, AVG(ploPercentages.PLOpercentage)
                FROM mainapp_department_t d,
                    mainapp_student_t s, (
                        SELECT DISTINCT student_id, (PLO / TotalComark * 100) AS PLOpercentage
                        FROM (
                            SELECT en.student_id, SUM(DISTINCT e.obtainedMarks) AS PLO, SUM(DISTINCT a.marks) AS TotalCoMark
                            FROM mainapp_enrollment_t en,
                                mainapp_evaluation_t e,
                                mainapp_assessment_t a,
                                mainapp_co_t c,
                                mainapp_plo_t p
                            WHERE en.enrollmentID = e.enrollment_id
                                AND e.assessment_id = a.assessmentNo
                                AND a.co_id = c.id
                                AND c.plo_id = '{}'
                            GROUP BY en.student_id
                        ) ploPer
                    ) ploPercentages
                WHERE d.departmentID = s.department_id
                    AND ploPercentages.student_id = s.studentID
                GROUP BY d.departmentID
            '''.format(ploNum))
            temp = cursor.fetchone()
            if temp is not None:
                row.append((temp[0], ploNum, temp[1]))
    return row
    
    
def getCourseWisePLO(student_id):
    row = []
    # student_id = '1625654'

    with connection.cursor() as cursor:
        cursor.execute('''
            SELECT DISTINCT co.course_id, co.coNo, p.ploNo, (PLO / TotalComark * 100) AS PLOpercentage
                FROM mainapp_plo_t p, mainapp_co_t co, (
                    SELECT DISTINCT c.course_id,c.coNo, c.plo_id, SUM(DISTINCT e.obtainedMarks) AS PLO, SUM(DISTINCT a.marks) AS TotalCoMark
                    FROM mainapp_enrollment_t en,
                        mainapp_evaluation_t e,
                        mainapp_assessment_t a,
                        mainapp_co_t c,
                        mainapp_plo_t p
                    WHERE en.student_id = '{}'
                        AND en.enrollmentID = e.enrollment_id
                        AND e.assessment_id = a.assessmentNo
                        AND a.co_id = c.id
                        AND c.plo_id = p.ploNo
                    GROUP BY en.section_id,c.plo_id
                    ORDER BY c.plo_id
                ) ploPer
            WHERE co.coNo = ploPer.coNo
                AND p.ploNo = ploPer.plo_id
                AND co.course_id = ploPer.course_id;
        '''.format(student_id))
        temp = cursor.fetchall()
        if temp is not None:
            row = temp

    courses = []
    for i in row:
        if i[0] not in courses:
            courses.append(i[0])

    table = []
    plo = ['PLO01', 'PLO02', 'PLO03', 'PLO04', 'PLO05', 'PLO06', 'PLO07', 'PLO08', 'PLO09', 'PLO10', 'PLO11', 'PLO12']
    for i in courses:
        tempTable = [i]
        for j in plo:
            found = False
            for k in row:
                if j == k[2] and i == k[0]:
                    tempTable.append(f'{np.round(k[3], 1)}%')
                    found = True
            if not found:
                tempTable.append('N/A')
        table.append(tempTable)
        
    return table