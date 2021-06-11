from common.db import DB
from common.get_companys import get_company_list


class get_one_company_worktimes:

    """

    前端传入公司和start_time和end_time 返回一个公司的总工时
    """

    def get_one_company_worktimes(self, company, start_time, end_time):

        db = DB()
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

        person_num = dr_person_nums[0][0]



        sql_over_worktimes = """
                         SELECT duration FROM {0}.overtime_records
                          where payment_method="加班薪资" and start_at >="{1}" and end_at<="{2}"              
                        """
        sql_overtimes_main = sql_over_worktimes.format(company, start_time, end_time)

        drs_overtime = db.execute_sql(conn, sql_overtimes_main)

        if drs_overtime:
            # dr_overtime = drs_overtime[0]

            print("-------")
            dr_overtime = 0
            for i in drs_overtime:
                for j in i:
                    dr_overtime+=j





            # for dr in drs_overtime:
            #     dr_overtimes += dr

        else:
            dr_overtime = 0

        one_company_times_num = person_num * dr_int_work_days * 8 + dr_overtime




        return float(one_company_times_num)