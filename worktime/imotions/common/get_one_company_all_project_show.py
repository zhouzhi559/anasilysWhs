from common.db import DB
from common.get_companys import get_company_list


class get_one_company_all_project:

    """

    得到一个公司所有的项目 和每个项目的工时

    例如：{公司1：{项目1：工时}}
    """

    def get_one_company_all_project(self, start_time, end_time):
        all_company_project_data = {}

        # start_time = '2021-05-01 00:00:00.000000'
        # end_time = '2021-06-01 00:00:00.000000'

        db = DB()
        get_list = get_company_list()
        get_compa_list = get_list.get_all_databases()

        all_company_project = {}


        for company in get_compa_list:

            if company != "zhitest" and company != "msgtest":

                company_project = {}
                conn = db.get_connection(company)
                sql = """
                
                SELECT project_name,sum(m_branches_department_preset_working_hours) FROM {0}.project_info 
                as a left join {0}.m_main as b on a.project_id = b.m_m_project_id 
                left join {0}.m_branches as c on c.m_main_code=b.m_main_code 
                left join {0}.m_branches_department as d on d.m_branches_code=c.m_branches_code 
                where m_branches_preset_start_at>='{1}' 
                and m_branches_preset_end_at<='{2}' group by m_main_cost_center;               
                """

                sql_main = sql.format(company, start_time, end_time)

                drs = db.execute_sql(conn, sql_main)
                db.close_connection(conn)

                for dr in drs:
                    company_project[dr[0]] = dr[1]

                all_company_project[company] = company_project
                # company_cos_name.append(company_project)
        print("----------")

        # print(company_cos_name)



        all_company_project_data["无界工场(上海)软件科技有限公司"] = all_company_project["software"]
        all_company_project_data["时新(上海)产品设计有限公司"] = all_company_project["imotion"]
        all_company_project_data["无界工场(上海)设计科技有限公司"] = all_company_project["wjtech"]
        all_company_project_data["上海慧瞰科技有限公司"] = all_company_project["pawithub"]
        all_company_project_data["无界国创（成都）科技有限公司"] = all_company_project["wjchin"]
        all_company_project_data["无界工场（上海）知识产权服务有限公司"] = all_company_project["wjip"]
        print(all_company_project_data)
        return all_company_project_data

