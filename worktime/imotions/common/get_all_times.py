from common.db import DB
from common.get_companys import get_company_list
import numpy
class get_all_times:

    """

    得到所有公司的总工时，返回一个数字

    """

    def get_all_times(self, start_time, end_time):
        all_times = {}
        person_list = []
        overtime_list = []

        dr_int_work_days = 0

        # start_time = '2021-05-01 00:00:00.000000'
        # end_time = '2021-06-01 00:00:00.000000'

        db = DB()
        get_list = get_company_list()
        get_compa_list = get_list.get_all_databases()

        for company in get_compa_list:

            if company != "zhitest" and company != "msgtest":
                conn = db.get_connection(company)
                sql = """
                  SELECT count(Date) FROM {0}.work_date where Description = '工作日' and Date>= '{1}' and Date <='{2}'
                """
                sql_main = sql.format(company, start_time, end_time)

                dr_days = db.execute_sql(conn, sql_main)
                dr_int_work_days = dr_days[0][0]
                sql_get_person = """
                     SELECT count(*) FROM {0}.user_job_info where assess_enable = '1';  
                                    """

                sql_person_main = sql_get_person.format(company)

                dr_person_nums = db.execute_sql(conn, sql_person_main)

                for person_nums in dr_person_nums:
                    for person_num in person_nums:
                        person_list.append(person_num)

                sql_over_worktimes = """
                 SELECT duration FROM {0}.overtime_records
                  where payment_method="加班薪资" and start_at >="{1}" and end_at<="{2}"              
                """
                sql_overtimes_main = sql_over_worktimes.format(company, start_time, end_time)

                drs_overtime = db.execute_sql(conn, sql_overtimes_main)

                if len(drs_overtime) == 0:
                    overtime_list.append(0)

                else:
                    s = 0
                    for dr_overtime in drs_overtime:
                        s += dr_overtime[0]

                    overtime_list.append(s)

        print("------")

        print(overtime_list)

        print(person_list)
        print(dr_int_work_days)

        work_times_list = []

        for i in person_list:

            work_times_list.append(i*dr_int_work_days*8)

        print(work_times_list)



        a_array = numpy.array(work_times_list)
        b_array = numpy.array(overtime_list)
        all_work_times = a_array + b_array

        print("-----")

        print(all_work_times)

        all_company_times = 0

        for i in all_work_times:
            all_company_times +=i

        all_company_times = float(all_company_times)

        return all_company_times










