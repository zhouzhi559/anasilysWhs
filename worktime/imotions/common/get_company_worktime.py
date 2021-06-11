from common.db import DB
from common.get_companys import get_company_list

class get_com_work:

    """
    返回的是每个公司的总工时， {{'companyXAxisData': ['无界工场(上海)软件科技有限公司', '时新(上海)产品设计有限公司', '无界工场(上海)设计科技有限公司', '上海慧瞰科技有限公司', '无界国创（成都）科技有限公司', '无界工场（上海）知识产权服务有限公司'], 'companyProjectHoursData': [1229.0, 15825.0, 1325.0, 578.0, 0, 372.0], 'companyWorkHoursData': [
2520, 27790.5, 3528, 1008, 504, 1512], 'companyPredictProjectTimes': [0, 0, 0, 0, 0, 0]}
每个公司的实际总工时，每个公司的预测总工时
}

    """

    def get_com_time(self, start_time, end_time):

        company_worktime = {}
        company_predict_worktime = {}

        data = {}

        realiy_work_time = []
        predict_work_time = []
        company_worktime_data = {}
        start_time = '2021-05-01 00:00:00.000000'
        end_time = '2021-06-01 00:00:00.000000'

        db = DB()

        get_list = get_company_list()
        get_compa_list = get_list.get_all_databases()

        for company in get_compa_list:

            if company != "zhitest" and company != "msgtest":
                conn = db.get_connection(company)

                sql = """
                SELECT sum(m_department_person_preset_working_hours) FROM {0}.m_department_person
                 where m_department_person_preset_start_at>="{1}" 
                 and m_department_person_preset_end_at<="{2}";               
                """
                sql_main = sql.format(company, start_time,  end_time)
                drs = db.execute_sql(conn, sql_main)

                print(len(drs))

                print("=======")

                sql_apply = """
                SELECT sum(m_main_department_preset_working_hours) FROM {0}.m_main_department_apply 
                where m_main_department_preset_start_at>="{1}" 
                 and m_main_department_preset_end_at<="{2}"
                
                """
                sql_apply_main = sql_apply.format(company, start_time, end_time)

                predict_drs = db.execute_sql(conn, sql_apply_main)


                if len(predict_drs) != 0:
                    for predict_dr in predict_drs:
                        if predict_dr[0]:
                            company_predict_worktime[company] = predict_dr[0]
                            predict_work_time.append(predict_dr[0])
                        else:
                            company_predict_worktime[company] = 0
                            predict_work_time.append(0)




                if len(drs) != 0:
                    for dr in drs:

                        if len(dr) != 0:
                            if dr[0]:
                                realiy_work_time.append(dr[0])
                                company_worktime[company] = dr[0]
                            else:
                                company_worktime[company] = 0
                                realiy_work_time.append(0)




        company_worktime_data['无界工场(上海)软件科技有限公司'] = company_worktime["software"] + company_predict_worktime["software"]
        company_worktime_data['时新(上海)产品设计有限公司'] = company_worktime["imotion"] + company_predict_worktime["imotion"]
        company_worktime_data['无界工场(上海)设计科技有限公司'] = company_worktime["wjtech"]+ company_predict_worktime["wjtech"]
        company_worktime_data['上海慧瞰科技有限公司'] = company_worktime["pawithub"]+ company_predict_worktime["pawithub"]
        company_worktime_data['无界国创（成都）科技有限公司'] = company_worktime["wjchin"]+ company_predict_worktime["wjchin"]
        company_worktime_data['无界工场（上海）知识产权服务有限公司'] = company_worktime["wjip"]+ company_predict_worktime["wjip"]


        print(company_worktime_data)

        print(predict_work_time)

        print(realiy_work_time)

        data['company_worktime_data'] = company_worktime_data
        data['predict_work_time'] = predict_work_time
        data['realiy_work_time'] = realiy_work_time



        return data






