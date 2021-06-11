from common.db import DB
from common.get_companys import get_company_list


class company_analysis_project:
    """

    得到一个公司在一个时间段里面的项目，  公司是前端输入， 以公司的角度去分析
    """

    def get_company_analysis_project(self, company, start_time, end_time):

        db = DB()

        company_project = {}

        conn = db.get_connection(company)

        sql = """
        SELECT project_name,cost_center,sum(m_branches_department_preset_working_hours) FROM {0}.project_info as a left join {0}.m_main as b on a.project_id = b.m_m_project_id left join {0}.m_branches as c on c.m_main_code=b.m_main_code left join {0}.m_branches_department as d on d.m_branches_code=c.m_branches_code where m_branches_preset_start_at>='{1}' and m_branches_preset_end_at<='{2}' group by cost_center;
        """
        sql_main = sql.format(company, start_time, end_time)
        print('=======================')
        print(sql_main)

        drs = db.execute_sql(conn, sql_main)

        for dr in drs:
            company_project[dr[0]] = dr[2]

        db.close_connection(conn)

        print("------")

        print(company_project)

        return company_project