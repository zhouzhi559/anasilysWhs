from common.db import DB
from common.get_companys import get_company_list





class get_one_project_anycompany_times:

    """
    前端传入一个项目（cost_center）, 返回一个公司公司列表：
    {'无界工场(上海)软件科技有限公司': 0, '时新(上海)产品设计有限公司': 0, '无界工场(上海)设计科技有限公司': 0, '上海慧瞰科技有限公司': 0, '无界国创（成都）科技有限公司': 0, '无界工场（上海）知识产权服务有限公司': 0}
    """

    def get_one_project_companys(self,start_time, end_time, project):

        db = DB()
        get_company = get_company_list()
        one_project_company = {}
        project_names = []
        company_time = {}
        chinese_company_time = {}
        one_pro_com_time = {}

        company_list = get_company.get_all_databases()
        for company in company_list:
            if company != "zhitest" and company != "msgtest":
                conn = db.get_connection(company)
                sql_name = """
                SELECT project_name FROM {0}.project_info where cost_center = '{1}'
                """
                sql_name_format = sql_name.format(company, project)
                project_name = db.execute_sql(conn, sql_name_format)
                if project_name:
                    project_names.append(project_name)
                else:
                    pass

                if len(project) != 8 and len(project) != 0:

                    sql = """
                    SELECT cost_center,project_name,sum(m_branches_department_preset_working_hours) FROM 
                    {0}.project_info as a left join {0}.m_main as b on a.project_id = b.m_m_project_id
                     left join {0}.m_branches as c on c.m_main_code=b.m_main_code 
                     left join {0}.m_branches_department as d on d.m_branches_code=c.m_branches_code
                      where m_branches_preset_start_at>='{1}' 
                      and m_branches_preset_end_at<='{2}' 
                      and cost_center='{3}' group by cost_center
                        """

                    sql_main = sql.format(company, start_time, end_time, project)

                    drs = db.execute_sql(conn, sql_main)
                    # print(drs)
                    if len(drs) == 0:
                        company_time[company] = 0
                    else:
                        company_time[company] = drs[0][2]

                else:
                    project_jieduan = project[-4:]
                    sql = """
                     SELECT cost_center,project_name,sum(m_branches_department_preset_working_hours) FROM 
                    {0}.project_info as a left join {0}.m_main as b on a.project_id = b.m_m_project_id
                     left join {0}.m_branches as c on c.m_main_code=b.m_main_code 
                     left join {0}.m_branches_department as d on d.m_branches_code=c.m_branches_code
                      where m_branches_preset_start_at>='{1}' 
                      and m_branches_preset_end_at<='{2}' 
                      and cost_center like '%{3}' group by cost_center
                    
                    """
                    sql_main = sql.format(company, start_time, end_time, project_jieduan)

                    # print(sql_main)

                    drs = db.execute_sql(conn, sql_main)
                    print(drs)
                    if len(drs) == 0:
                        company_time[company] = 0
                    else:
                        company_time[company] = drs[0][2]

                # if len(drs) == 0:
                #     one_project_company
                #
                # print("-----------------")
                # print(drs)
                # print(len(drs))

                db.close_connection(conn)
        # return drs


        # print(project_names[0][0][0])

        # print("------")


        chinese_company_time['无界工场(上海)软件科技有限公司'] = company_time["software"]
        chinese_company_time['时新(上海)产品设计有限公司'] = company_time["imotion"]
        chinese_company_time['无界工场(上海)设计科技有限公司'] = company_time["wjtech"]
        chinese_company_time['上海慧瞰科技有限公司'] = company_time["pawithub"]
        chinese_company_time['无界国创（成都）科技有限公司'] = company_time["wjchin"]
        chinese_company_time['无界工场（上海）知识产权服务有限公司'] = company_time["wjip"]

        # print(chinese_company_time)

        # one_pro_com_time[project_names[0][0][0]] = chinese_company_time

        return chinese_company_time