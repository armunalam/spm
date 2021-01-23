from django.db import connection

def getStudentWisePLO(student_id):
    row = []
    for i in range(12):
        ploNum = f'PLO0{i + 1}'
        if i + 1 >= 10:
            ploNum = f'PLO{i + 1}'
        with connection.cursor() as cursor:
            cursor.execute('''
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
                    AND a.co_id = c.coNo
                    AND c.plo_id = '{}'
                    GROUP BY en.student_id
                ) ploPer;
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
                        SELECT student_id, (PLO / TotalComark * 100) AS PLOpercentage
                        FROM (
                            SELECT en.student_id, SUM(DISTINCT e.obtainedMarks) AS PLO, SUM(DISTINCT a.marks) AS TotalCoMark
                            FROM mainapp_enrollment_t en,
                                mainapp_evaluation_t e,
                                mainapp_assessment_t a,
                                mainapp_co_t c,
                                mainapp_plo_t p
                            WHERE en.enrollmentID = e.enrollment_id
                                AND e.assessment_id = a.assessmentNo
                                AND a.co_id = c.coNo
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