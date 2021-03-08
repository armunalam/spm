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
                ) TotalPlo;
            '''.format(student_id, ploNum))
            temp = cursor.fetchone()
            if temp is not None:
                row.append((temp[0], ploNum))
    return row
    
    
def getDepartmentWisePLO(deptID):
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
                            SELECT SUM(e.obtainedMarks) AS PLO, SUM(a.marks) AS TotalCoMark
                            FROM mainapp_enrollment_t en,
                                mainapp_evaluation_t e,
                                mainapp_assessment_t a,
                                mainapp_co_t c,
                                mainapp_plo_t p,
                                mainapp_student_t st
                            WHERE st.department_id = '{}'
                            AND st.studentID = en.student_id
                            AND en.enrollmentID = e.enrollment_id
                            AND e.assessment_id = a.assessmentNo
                            AND a.co_id = c.id
                            AND c.plo_id = '{}'
                            GROUP BY en.section_id
                        ) ploPer
                    ) TotalPlo;
            '''.format(deptID, ploNum))
            temp = cursor.fetchone()
            if temp is not None:
                row.append((deptID, ploNum, temp[0]))
    return row
    
    
def getCourseWisePLO(student_id):
    row = []

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
    
    
def getCourseWisePLOChart(student_id):
    row = []

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
                    tempTable.append(np.round(k[3], 1))
                    found = True
            if not found:
                tempTable.append(0)
        table.append(tempTable)
        
    dataRow = np.array(table)[:, 1:].astype(float)
    for i in range(dataRow.shape[1]):
        dataRow[:, i] = np.round(dataRow[:, i] / np.sum(dataRow[:, i]) * 100, 3)
        
    table = dataRow.tolist()
        
    return (plo, courses, table)


def getStudentProgressView(student_id, year):
    plo = ['PLO01', 'PLO02', 'PLO03', 'PLO04', 'PLO05', 'PLO06', 'PLO07', 'PLO08', 'PLO09', 'PLO10', 'PLO11', 'PLO12']
    semesterActual = []
    semesterAttempted = []
    for i in range(3):
        counterActual = 0
        counterAttempted = 0
        for j in plo:
            with connection.cursor() as cursor:
                cursor.execute('''
                    SELECT COUNT(Acheived.ActualPlo) AS PLoacheivedornot
                    FROM(
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
                                    AND en.semester = '{}'
                                    AND en.year = '{}'
                                    AND en.enrollmentID = e.enrollment_id
                                    AND e.assessment_id = a.assessmentNo
                                    AND a.co_id = c.id
                                    AND c.plo_id = '{}'
                                GROUP BY en.semester
                            ) ploPer
                        ) TotalPlo
                    ) Acheived
                    WHERE Acheived.ActualPlo >=40;
                '''.format(student_id, i + 1, year, j))
                temp = cursor.fetchall()
                if temp is not None:
                    row = temp
                    if row[0][0] > 0:
                        counterActual += 1
            
            with connection.cursor() as cursor:
                cursor.execute('''
                    SELECT COUNT(Acheived.ActualPlo) AS PLoacheivedornot
                    FROM(
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
                                    AND en.semester = '{}'
                                    AND en.year = '{}'
                                    AND en.enrollmentID = e.enrollment_id
                                    AND e.assessment_id = a.assessmentNo
                                    AND a.co_id = c.id
                                    AND c.plo_id = '{}'
                                GROUP BY en.semester
                            ) ploPer
                        ) TotalPlo
                    ) Acheived
                '''.format(student_id, i + 1, year, j))
                temp = cursor.fetchall()
                if temp is not None:
                    row = temp
                    if row[0][0] > 0:
                        counterAttempted += 1
        semesterActual.append(counterActual)
        semesterAttempted.append(counterAttempted)
    
    semester = ['Spring', 'Summer', 'Autumn']
    return (semester, semesterActual, semesterAttempted)
        
def getSemesterWiseStudentProgress(semester, year):
    plo = ['PLO01', 'PLO02', 'PLO03', 'PLO04', 'PLO05', 'PLO06', 'PLO07', 'PLO08', 'PLO09', 'PLO10', 'PLO11', 'PLO12']
    semesterActual = []
    semesterAttempted = []
    row = []
    
    for j in plo:
        with connection.cursor() as cursor:
            cursor.execute('''
                SELECT COUNT(Acheived.ActualPlo)
                    FROM (
                            SELECT AVG(TotalPlo.PLOpercentage) AS ActualPlo
                            FROM (
                                    SELECT student_id,(PLO / TotalComark * 100) AS PLOpercentage
                                    FROM (
                                            SELECT  en.student_id,SUM( e.obtainedMarks) AS PLO, SUM( a.marks) AS TotalCoMark
                                            FROM mainapp_enrollment_t en,
                                                    mainapp_evaluation_t e,
                                                    mainapp_assessment_t a,
                                                    mainapp_co_t c,
                                                    mainapp_plo_t p
                                            WHERE en.enrollmentID = e.enrollment_id
                                                AND en.semester = '{}'
                                                AND en.year = '{}'
                                                AND e.assessment_id = a.assessmentNo
                                                AND a.co_id = c.id
                                                AND c.plo_id = '{}'
                                            GROUP BY en.student_id
                                        ) ploPer
                                GROUP BY student_id
                                ) TotalPlo
                    GROUP BY student_id
                        ) Acheived
                    WHERE Acheived.ActualPlo >= 40;
            '''.format(semester, year, j))
            row = cursor.fetchall()
            if row is None:
                row = []
            semesterActual.append(row[0][0])
                
        row = []
        with connection.cursor() as cursor:
            cursor.execute('''
                SELECT COUNT(Acheived.ActualPlo)
                    FROM (
                            SELECT AVG(TotalPlo.PLOpercentage) AS ActualPlo
                            FROM (
                                    SELECT student_id,(PLO / TotalComark * 100) AS PLOpercentage
                                    FROM (
                                            SELECT  en.student_id,SUM( e.obtainedMarks) AS PLO, SUM( a.marks) AS TotalCoMark
                                            FROM mainapp_enrollment_t en,
                                                    mainapp_evaluation_t e,
                                                    mainapp_assessment_t a,
                                                    mainapp_co_t c,
                                                    mainapp_plo_t p
                                            WHERE en.enrollmentID = e.enrollment_id
                                                AND en.semester = '{}'
                                                AND en.year = '{}'
                                                AND e.assessment_id = a.assessmentNo
                                                AND a.co_id = c.id
                                                AND c.plo_id = '{}'
                                            GROUP BY en.student_id
                                        ) ploPer
                                GROUP BY student_id
                                ) TotalPlo
                    GROUP BY student_id
                        ) Acheived
            '''.format(semester, year, j))
            row = cursor.fetchall()
            if row is None:
                row = []
            semesterAttempted.append(row[0][0])
    
    return (plo, semesterActual, semesterAttempted)
    
    
def getProgramAchievement(prog):
    plo = ['PLO01', 'PLO02', 'PLO03', 'PLO04', 'PLO05', 'PLO06', 'PLO07', 'PLO08', 'PLO09', 'PLO10', 'PLO11', 'PLO12']
    semesterActual = []
    semesterAttempted = []
    row = []
    
    for j in plo:
        with connection.cursor() as cursor:
            cursor.execute('''
                SELECT COUNT(Acheived.ActualPlo)
                FROM (
                        SELECT AVG(TotalPlo.PLOpercentage) AS ActualPlo
                        FROM (
                                SELECT student_id,(PLO / TotalComark * 100) AS PLOpercentage
                                FROM (
                                        SELECT  en.student_id,SUM(DISTINCT e.obtainedMarks) AS PLO, SUM(DISTINCT a.marks) AS TotalCoMark
                                        FROM mainapp_enrollment_t en,
                                                mainapp_evaluation_t e,
                                                mainapp_assessment_t a,
                                                mainapp_co_t c,
                                                mainapp_plo_t p,
                                                mainapp_program_t pr
                                        WHERE p.program_id = pr.programID
                                            AND pr.programID = '{}'
                                            AND en.enrollmentID = e.enrollment_id
                                            AND e.assessment_id = a.assessmentNo
                                            AND a.co_id = c.id
                                            AND c.plo_id = '{}'
                                        GROUP BY en.student_id
                                    ) ploPer
                            GROUP BY student_id
                            ) TotalPlo
                GROUP BY student_id
                    ) Acheived
                WHERE Acheived.ActualPlo >= 40;
            '''.format(prog, j))
            row = cursor.fetchall()
            if row is None:
                row = []
            semesterActual.append(row[0][0])
                
        row = []
        with connection.cursor() as cursor:
            cursor.execute('''
                SELECT COUNT(Acheived.ActualPlo)
                FROM (
                        SELECT AVG(TotalPlo.PLOpercentage) AS ActualPlo
                        FROM (
                                SELECT student_id,(PLO / TotalComark * 100) AS PLOpercentage
                                FROM (
                                        SELECT  en.student_id,SUM(DISTINCT e.obtainedMarks) AS PLO, SUM(DISTINCT a.marks) AS TotalCoMark
                                        FROM mainapp_enrollment_t en,
                                                mainapp_evaluation_t e,
                                                mainapp_assessment_t a,
                                                mainapp_co_t c,
                                                mainapp_plo_t p,
                                                mainapp_program_t pr
                                        WHERE p.program_id = pr.programID
                                            AND pr.programID = '{}'
                                            AND en.enrollmentID = e.enrollment_id
                                            AND e.assessment_id = a.assessmentNo
                                            AND a.co_id = c.id
                                            AND c.plo_id = '{}'
                                        GROUP BY en.student_id
                                    ) ploPer
                            GROUP BY student_id
                            ) TotalPlo
                GROUP BY student_id
                    ) Acheived
            '''.format(prog, j))
            row = cursor.fetchall()
            if row is None:
                row = []
            semesterAttempted.append(row[0][0])
    
    return (plo, semesterActual, semesterAttempted)
    
    
def getCourseProgressView(course_id, year):
    plo = ['PLO01', 'PLO02', 'PLO03', 'PLO04', 'PLO05', 'PLO06', 'PLO07', 'PLO08', 'PLO09', 'PLO10', 'PLO11', 'PLO12']
    semesterActual = []
    semesterAttempted = []
    for i in range(3):
        ploActual = []
        ploAttempted = 0
        for j in plo:
            with connection.cursor() as cursor:
                cursor.execute('''
                    SELECT COUNT(Acheived.ActualPlo)
                    FROM (
                            SELECT AVG(TotalPlo.PLOpercentage) AS ActualPlo
                            FROM (
                                    SELECT student_id,(PLO / TotalComark * 100) AS PLOpercentage
                                    FROM (
                                            SELECT  en.student_id,SUM(DISTINCT e.obtainedMarks) AS PLO, SUM(DISTINCT a.marks) AS TotalCoMark
                                            FROM mainapp_enrollment_t en,
                                                    mainapp_evaluation_t e,
                                                    mainapp_assessment_t a,
                                                    mainapp_co_t c,
                                                    mainapp_plo_t p
                                            WHERE en.semester ='{}'
                                                AND en.year = '{}'
                                                AND en.enrollmentID = e.enrollment_id
                                                AND e.assessment_id = a.assessmentNo
                                                AND a.co_id = c.id
                                                AND c.course_id = '{}'
                                                AND c.plo_id = '{}'
                                            GROUP BY en.student_id
                                        ) ploPer
                                GROUP BY student_id
                                ) TotalPlo
                    GROUP BY student_id
                        ) Acheived
                    WHERE Acheived.ActualPlo >= 40;
                '''.format(i + 1, year, course_id, j))
                temp = cursor.fetchone()
                if temp is not None:
                    row = temp[0]
                    ploActual.append(row)
        semesterActual.append(ploActual)
            
        for j in plo:
            with connection.cursor() as cursor:
                cursor.execute('''
                    SELECT COUNT(Acheived.ActualPlo)
                    FROM (
                            SELECT AVG(TotalPlo.PLOpercentage) AS ActualPlo
                            FROM (
                                    SELECT student_id,(PLO / TotalComark * 100) AS PLOpercentage
                                    FROM (
                                            SELECT  en.student_id,SUM(DISTINCT e.obtainedMarks) AS PLO, SUM(DISTINCT a.marks) AS TotalCoMark
                                            FROM mainapp_enrollment_t en,
                                                    mainapp_evaluation_t e,
                                                    mainapp_assessment_t a,
                                                    mainapp_co_t c,
                                                    mainapp_plo_t p
                                            WHERE en.semester ='{}'
                                                AND en.year = '{}'
                                                AND en.enrollmentID = e.enrollment_id
                                                AND e.assessment_id = a.assessmentNo
                                                AND a.co_id = c.id
                                                AND c.course_id = '{}'
                                                AND c.plo_id = '{}'
                                            GROUP BY en.student_id
                                        ) ploPer
                                GROUP BY student_id
                                ) TotalPlo
                    GROUP BY student_id
                        ) Acheived;
                '''.format(i + 1, year, course_id, j))
                temp = cursor.fetchone()
                if temp is not None:
                    row = temp[0]
                    ploAttempted += row
        semesterAttempted.append(ploAttempted)
        
    tempActual = np.array(semesterActual)
    
    for i in range(1, tempActual.shape[0]):
        tempActual[i, :] += tempActual[i - 1, :]
    
    tempActual = tempActual.T
    semesterActual = tempActual.tolist()
    
    for i in range(1, len(semesterAttempted)):
        semesterAttempted[i] += semesterAttempted[i - 1]
    
    semester = ['Spring', 'Summer', 'Autumn']
    return (semester, semesterActual, semesterAttempted)


def getVerdictTable(course_id):
    row = []
    total = 0
    with connection.cursor() as cursor:
        
        cursor.execute('''
            SELECT coNo,ploNo,COUNT(TotalPlo.PLOpercentage) AS Acheive
            FROM (
                    SELECT  co.course_id, co.coNo, p.ploNo,(PLO / TotalComark * 100) AS PLOpercentage
                    FROM mainapp_plo_t p,
                        mainapp_co_t co,
                        (
                            SELECT en.student_id,c.course_id,c.coNo,c.plo_id,SUM(DISTINCT e.obtainedMarks) AS PLO,SUM(DISTINCT a.marks)AS TotalCoMark
                            FROM mainapp_enrollment_t en,
                                mainapp_evaluation_t e,
                                mainapp_assessment_t a,
                                mainapp_co_t c,
                                mainapp_plo_t p
                            WHERE en.enrollmentID = e.enrollment_id
                                AND e.assessment_id = a.assessmentNo
                                AND a.co_id = c.id
                                AND c.course_id = '{}'
                                AND c.plo_id = p.ploNo
                            GROUP BY  student_id,c.course_id,c.coNo,p.ploNo
                        ) ploPer
                    WHERE co.coNo = ploPer.coNo
                    AND p.ploNo = ploPer.plo_id
                    AND co.course_id = ploPer.course_id
                GROUP BY student_id,co.course_id,co.coNo,ploNo
                HAVING PLOpercentage >=40
                )TotalPlo

            GROUP BY course_id,coNo,ploNo;
        '''.format(course_id))
        row = cursor.fetchall()
        if row is None:
            row = []
        
        cursor.execute('''
            SELECT coNo,ploNo,COUNT(TotalPlo.PLOpercentage) AS Acheive
            FROM (
                    SELECT  co.course_id, co.coNo, p.ploNo,(PLO / TotalComark * 100) AS PLOpercentage
                    FROM mainapp_plo_t p,
                        mainapp_co_t co,
                        (
                            SELECT en.student_id,c.course_id,c.coNo,c.plo_id,SUM(DISTINCT e.obtainedMarks) AS PLO,SUM(DISTINCT a.marks)AS TotalCoMark
                            FROM mainapp_enrollment_t en,
                                mainapp_evaluation_t e,
                                mainapp_assessment_t a,
                                mainapp_co_t c,
                                mainapp_plo_t p
                            WHERE en.enrollmentID = e.enrollment_id
                                AND e.assessment_id = a.assessmentNo
                                AND a.co_id = c.id
                                AND c.course_id = '{}'
                                AND c.plo_id = p.ploNo
                            GROUP BY  student_id,c.course_id,c.coNo,p.ploNo
                        ) ploPer
                    WHERE co.coNo = ploPer.coNo
                    AND p.ploNo = ploPer.plo_id
                    AND co.course_id = ploPer.course_id
                GROUP BY student_id,co.course_id,co.coNo,ploNo
                )TotalPlo

            GROUP BY course_id,coNo,ploNo;
        '''.format(course_id))
        total = cursor.fetchone()[2]
        if row is None:
            total = 0
    coplo = []
    tempRow = []
    for i in row:
        tempRow.append(i[2])
        coplo.append([i[0], i[1]])
    tempRow = np.array(tempRow)
    
    success = np.round(tempRow / total * 100, 3)
    failCount = total - tempRow
    fail = np.round(failCount / total * 100, 3)
    row = np.column_stack((tempRow, success, failCount, fail)).tolist()
    
    finalRow = []
    for i in range(len(row)):
        tempRow = coplo[i]
        for j in range(len(row[i])):
            tempRow.append(row[i][j])
        finalRow.append(tempRow)
    
    return (finalRow, total)
    
    
# Student

# Number of PLOs achieved by students
def getNoOfPLOAchieved(student_id):
    number = 0
    with connection.cursor() as cursor:
        cursor.execute('''
            SELECT COUNT(TotalPlo.PLOpercentage) AS Acheive
            FROM (
                    SELECT   student_id,(PLO / TotalComark * 100) AS PLOpercentage
                    FROM mainapp_plo_t p,
                        mainapp_co_t co,
                        (
                            SELECT en.student_id,c.plo_id,SUM(DISTINCT e.obtainedMarks) AS PLO,SUM(DISTINCT a.marks)AS TotalCoMark
                            FROM mainapp_enrollment_t en,
                                mainapp_evaluation_t e,
                                mainapp_assessment_t a,
                                mainapp_co_t c,
                                mainapp_plo_t p,
                                mainapp_section_t sec
                            WHERE en.student_id = '{}'
                            AND en.enrollmentID = e.enrollment_id
                                AND e.assessment_id = a.assessmentNo
                                AND a.co_id = c.id
                                AND c.plo_id = p.ploNo
                            GROUP BY  student_id,p.ploNo
                        ) ploPer
                    WHERE p.ploNo = ploPer.plo_id

                GROUP BY student_id,ploNo
                HAVING PLOpercentage >=40
                ) TotalPlo

            GROUP BY student_id
        '''.format(student_id))
        number = cursor.fetchone()[0]
        if number is None:
            number = 0
            
    return number
    
# PLO Attempted
def getNoOfPLOAttempted(student_id):
    number = 0
    with connection.cursor() as cursor:
        cursor.execute('''
            SELECT COUNT(TotalPlo.PLOpercentage) AS Acheive
            FROM (
                    SELECT   student_id,(PLO / TotalComark * 100) AS PLOpercentage
                    FROM mainapp_plo_t p,
                        mainapp_co_t co,
                        (
                            SELECT en.student_id,c.plo_id,SUM(DISTINCT e.obtainedMarks) AS PLO,SUM(DISTINCT a.marks)AS TotalCoMark
                            FROM mainapp_enrollment_t en,
                                mainapp_evaluation_t e,
                                mainapp_assessment_t a,
                                mainapp_co_t c,
                                mainapp_plo_t p,
                                mainapp_section_t sec
                            WHERE en.student_id = '{}'
                            AND en.enrollmentID = e.enrollment_id
                                AND e.assessment_id = a.assessmentNo
                                AND a.co_id = c.id
                                AND c.plo_id = p.ploNo
                            GROUP BY  student_id,p.ploNo
                        ) ploPer
                    WHERE p.ploNo = ploPer.plo_id

                GROUP BY student_id,ploNo
            
                ) TotalPlo
        '''.format(student_id))
        number = cursor.fetchone()[0]
        if number is None:
            number = 0
            
    return number
    

# min lowest PLO %
def getMinLowestPLO(student_id):
    number = 1000000
    plo = ''
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
                ) TotalPlo;
            '''.format(student_id, ploNum))
            temp = cursor.fetchone()
            if temp is not None:
                if number > temp[0]:
                    number = temp[0]
                    plo = ploNum
                    
    return plo

# PLO Success Rate
def ploSuccessRate(student_id):
    return np.round(getNoOfPLOAchieved(student_id) / getNoOfPLOAttempted(student_id) * 100, 1)


# Higher Management

# Number of Students
def getNumOfStudents(dept_id):
    number = 0
    with connection.cursor() as cursor:
        cursor.execute('''
            SELECT COUNT(studentID) AS NoOfStudent
            FROM mainapp_student_t
            WHERE department_id = '{}'
        '''.format(dept_id))
        number = cursor.fetchone()[0]
        if number is None:
            number = 0
            
    return number

# Number of Faculties
def getNumOfFaculties(dept_id):
    number = 0
    with connection.cursor() as cursor:
        cursor.execute('''
            SELECT COUNT (DISTINCT facultyID ) AS NoFaculty
            FROM mainapp_faculty_t
            WHERE department_id = '{}'
        '''.format(dept_id))
        number = cursor.fetchone()[0]
        if number is None:
            number = 0
            
    return number
    
# Number of courses in a department
def getNumOfCourses():
    number = 0
    with connection.cursor() as cursor:
        cursor.execute('''
            SELECT COUNT(courseID) AS NoOfcourses
            FROM mainapp_course_t
        '''.format())
        number = cursor.fetchone()[0]
        if number is None:
            number = 0
            
    return number

# Average Achieved PLO
def getAverageAchievedPLO():
    number = 0
    with connection.cursor() as cursor:
        cursor.execute('''
            SELECT AVG(AcheivedPLo) AS AVGacheivedPlo
            FROM (
                    SELECT ploNo, COUNT(Acheived.ActualPlo) AS AcheivedPLo
                    FROM (
                            SELECT ploNo, AVG(TotalPlo.PLOpercentage) AS ActualPlo
                            FROM (
                                    SELECT student_id, ploNo, (PLO / TotalComark * 100) AS PLOpercentage
                                    FROM (
                                                SELECT en.student_id,
                                                    ploNo,
                                                    SUM(DISTINCT e.obtainedMarks) AS PLO,
                                                    SUM(DISTINCT a.marks)         AS TotalCoMark
                                                FROM mainapp_enrollment_t en,
                                                    mainapp_evaluation_t e,
                                                    mainapp_assessment_t a,
                                                    mainapp_co_t c,
                                                    mainapp_plo_t p
                                                WHERE en.enrollmentID = e.enrollment_id
                                                AND e.assessment_id = a.assessmentNo
                                                AND a.co_id = c.id
                                                AND c.plo_id = p.ploNo
                                                GROUP BY en.student_id, ploNo
                                            ) ploPer
                                    GROUP BY student_id, ploNo
                                ) TotalPlo
                            GROUP BY student_id, ploNo
                        ) Acheived
                    WHERE Acheived.ActualPlo >= 40
                    GROUP BY ploNo
                )
        '''.format())
        number = cursor.fetchone()[0]
        if number is None:
            number = 0
            
    return np.round(number, 1)
    
    
# Faculty

# Num of Courses
def getNumOfCoursesHead(faculty_id):
    number = 0
    with connection.cursor() as cursor:
        cursor.execute('''
            SELECT COUNT(DISTINCT course_id) AS NoOfCourses
            FROM mainapp_section_t
            WHERE faculty_id = '{}';
        '''.format(faculty_id))
        number = cursor.fetchone()[0]
        if number is None:
            number = 0
            
    return number
    
# Num of Sections
def getNumOfSections(faculty_id):
    number = 0
    with connection.cursor() as cursor:
        cursor.execute('''
            SELECT COUNT(id) AS NoOfSection
            FROM mainapp_section_t
            WHERE faculty_id = '{}';
        '''.format(faculty_id))
        number = cursor.fetchone()[0]
        if number is None:
            number = 0
            
    return number
    
# Average PLO Success Rate
def getAverageSuccessRate(faculty_id):
    achieved = 0
    attempted = 0
    with connection.cursor() as cursor:
        cursor.execute('''
            SELECT AVG(Acheive) AS AVGPloacheivedbyastudent
            FROM (
                    SELECT course_id, coNo, ploNo, COUNT(TotalPlo.PLOpercentage) AS Acheive
                    FROM (
                            SELECT co.course_id, co.coNo, p.ploNo, (PLO / TotalComark * 100) AS PLOpercentage
                            FROM mainapp_plo_t p,
                                mainapp_co_t co,
                                (
                                    SELECT en.student_id,
                                            c.course_id,
                                            c.coNo,
                                            c.plo_id,
                                            SUM(DISTINCT e.obtainedMarks) AS PLO,
                                            SUM(DISTINCT a.marks)         AS TotalCoMark
                                    FROM mainapp_enrollment_t en,
                                            mainapp_section_t sec,
                                            mainapp_evaluation_t e,
                                            mainapp_assessment_t a,
                                            mainapp_co_t c,
                                            mainapp_plo_t p
                                    WHERE en.enrollmentID = e.enrollment_id
                                        AND en.section_id = sec.id
                                        AND faculty_id = '{}'
                                        AND e.assessment_id = a.assessmentNo
                                        AND a.co_id = c.id
                                        AND c.plo_id = p.ploNo
                                    GROUP BY student_id, c.course_id, c.coNo, p.ploNo
                                ) ploPer
                            WHERE co.coNo = ploPer.coNo
                                AND p.ploNo = ploPer.plo_id
                                AND co.course_id = ploPer.course_id
                            GROUP BY student_id, co.course_id, co.coNo, ploNo
                            HAVING PLOpercentage >= 40
                        ) TotalPlo

                    GROUP BY course_id, coNo, ploNo
                )
        '''.format(faculty_id))
        achieved = cursor.fetchone()[0]
        if achieved is None:
            achieved = 0
            
        cursor.execute('''
            SELECT AVG(Acheive) AS AVGPloacheivedbyastudent
            FROM (
                    SELECT course_id, coNo, ploNo, COUNT(TotalPlo.PLOpercentage) AS Acheive
                    FROM (
                            SELECT co.course_id, co.coNo, p.ploNo, (PLO / TotalComark * 100) AS PLOpercentage
                            FROM mainapp_plo_t p,
                                mainapp_co_t co,
                                (
                                    SELECT en.student_id,
                                            c.course_id,
                                            c.coNo,
                                            c.plo_id,
                                            SUM(DISTINCT e.obtainedMarks) AS PLO,
                                            SUM(DISTINCT a.marks)         AS TotalCoMark
                                    FROM mainapp_enrollment_t en,
                                            mainapp_section_t sec,
                                            mainapp_evaluation_t e,
                                            mainapp_assessment_t a,
                                            mainapp_co_t c,
                                            mainapp_plo_t p
                                    WHERE en.enrollmentID = e.enrollment_id
                                        AND en.section_id = sec.id
                                        AND faculty_id = '{}'
                                        AND e.assessment_id = a.assessmentNo
                                        AND a.co_id = c.id
                                        AND c.plo_id = p.ploNo
                                    GROUP BY student_id, c.course_id, c.coNo, p.ploNo
                                ) ploPer
                            WHERE co.coNo = ploPer.coNo
                                AND p.ploNo = ploPer.plo_id
                                AND co.course_id = ploPer.course_id
                            GROUP BY student_id, co.course_id, co.coNo, ploNo
                        ) TotalPlo

                    GROUP BY course_id, coNo, ploNo
                )
        '''.format(faculty_id))
        attempted = cursor.fetchone()[0]
        if attempted is None:
            attempted = 0
            
    return np.round(achieved / attempted * 100, 1)
        

# Total Number of PLOs Taught
def getNumOfPLOsTaught(faculty_id):
    number = 0
    with connection.cursor() as cursor:
        cursor.execute('''
            SELECT COUNT(ploNo) AS TotalNoPlotaught
            FROM (
                    SELECT course_id, coNo, ploNo, COUNT(TotalPlo.PLOpercentage) AS Acheive
                    FROM (
                            SELECT co.course_id, co.coNo, p.ploNo, (PLO / TotalComark * 100) AS PLOpercentage
                            FROM mainapp_plo_t p,
                                mainapp_co_t co,
                                (
                                    SELECT en.student_id,
                                            c.course_id,
                                            c.coNo,
                                            c.plo_id,
                                            SUM(DISTINCT e.obtainedMarks) AS PLO,
                                            SUM(DISTINCT a.marks)         AS TotalCoMark
                                    FROM mainapp_enrollment_t en,
                                            mainapp_section_t sec,
                                            mainapp_evaluation_t e,
                                            mainapp_assessment_t a,
                                            mainapp_co_t c,
                                            mainapp_plo_t p
                                    WHERE en.enrollmentID = e.enrollment_id
                                        AND en.section_id = sec.id
                                        AND faculty_id = '{}'
                                        AND e.assessment_id = a.assessmentNo
                                        AND a.co_id = c.id
                                        AND c.plo_id = p.ploNo
                                    GROUP BY student_id, c.course_id, c.coNo, p.ploNo
                                ) ploPer
                            WHERE co.coNo = ploPer.coNo
                                AND p.ploNo = ploPer.plo_id
                                AND co.course_id = ploPer.course_id
                            GROUP BY student_id, co.course_id, co.coNo, ploNo

                        ) TotalPlo

                    GROUP BY course_id, coNo, ploNo
                )
        '''.format(faculty_id))
        number = cursor.fetchone()[0]
        if number is None:
            number = 0
            
    return number
