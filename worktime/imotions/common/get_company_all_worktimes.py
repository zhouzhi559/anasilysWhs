# from common.db import DB
# from common.get_companys import get_company_list
#
# class get_company_times:
#
#     def get_company_worktimes(self, start_time, end_time):
#
#         start_time = '2021-05-01 00:00:00.000000'
#         end_time = '2021-06-01 00:00:00.000000'
#         db = DB()
#         data = get_company_list()
#         data_list = data.get_all_databases()
#
#         company_dict_add_worktime = {}
#         company_dict_worktime = {}
#
#         company_dict_predict_data = {}
#
#         all_company_dict = {}
#
#         for company in data_list:
#
#             if company != "msgtest" and company != "zhitest":
#
#                 one_pro_dict = "one_pro_dict_" + company
#
#                 one_company_dict = {}
#
#                 conn = db.get_connection(company)
#
#                 sql = """
#                     SELECT m_department_person_preset_working_hours FROM {0}.m_department_person where m_department_person_preset_start_at >='{1}'
#                     and m_department_person_preset_end_at <='{2}'
#                     """
#                 sql_main = sql.format(company, start_time, end_time)
#
#                 print(sql_main)
#
#                 sql_apply = """
#                        SELECT m_main_department_preset_working_hours_proportion FROM {0}.m_main_department_apply
#                        where m_main_department_preset_start_at >='{1}'
#                        and m_main_department_preset_end_at <='{2}'
#
#                 """
#
#                 sql_apply_format = sql_apply.format(company, start_time, end_time)
#
#
#                 department_person_tables = db.execute_sql(conn, sql_main)
#
#                 predict_datas = db.execute_sql(conn, sql_apply_format)
#
#                 if len(department_person_tables) != 0:
#                     for department_person_table in department_person_tables:
#                         if company not in company_dict_add_worktime.keys():
#                             company_dict_add_worktime[company] = float(department_person_table[0])
#
#                         else:
#                             company_dict_add_worktime[company] = company_dict_add_worktime[company] + float(department_person_table[0])
#                 else:
#                     company_dict_add_worktime[company] = 0
#
#                 if len(predict_datas) == 0:
#                     company_dict_predict_data[company] = 0
#
#                 else:
#                     for predict_data in predict_datas:
#                         if company not in company_dict_predict_data.keys():
#                             company_dict_predict_data[company] = float(predict_data[0])
#
#                         else:
#                             company_dict_predict_data[company] = company_dict_predict_data[company] + float(predict_data[0])
#
#
#         #print(company_dict_predict_data)
#
#         for com in company_dict_predict_data.keys():
#             if com in company_dict_add_worktime.keys():
#                 company_dict_add_worktime[com] = company_dict_add_worktime[com] + company_dict_predict_data[com]
#
#         #print(company_dict_add_worktime)
#
#         print("-----------")
#
#
#
#         print(company_dict_add_worktime)
#         company_dict_worktime['无界工场(上海)软件科技有限公司'] = company_dict_add_worktime['software']
#         company_dict_worktime['时新(上海)产品设计有限公司'] = company_dict_add_worktime['imotion']
#         company_dict_worktime['无界工场(上海)设计科技有限公司'] = company_dict_add_worktime['wjtech']
#         company_dict_worktime['上海慧瞰科技有限公司'] = company_dict_add_worktime['pawithub']
#         company_dict_worktime['无界国创（成都）科技有限公司'] = company_dict_add_worktime['wjchin']
#         company_dict_worktime['无界工场（上海）知识产权服务有限公司'] = company_dict_add_worktime['wjip']
#
#         print(company_dict_worktime)
#
#         return company_dict_worktime


                # project_id_names = db.execute_sql(conn, sql_main)
        #
        #         project_id_names = db.execute_sql(conn, sql_main)
        #
        #         for project_name_type in project_id_names:
        #             project_name = project_name_type[1]
        #             if project_name not in all_project_name:
        #                 all_project_name.append(project_name)
        #         # db.close_connection(conn)
        #
        #         # conn = db.get_connection(company)
        #
        #         for project_ids in project_id_names:
        #             # for project_id in project_ids:
        #             sql_main1 = """
        #                                  SELECT m_main_code FROM {0}.m_main where m_m_project_id = "{1}" and
        #                                  m_main_preset_start_at >= "{2}" and
        #                                  m_main_preset_end_at <= "{3}"
        #                                """
        #             sql_main = sql_main1.format(company, project_ids[0], start_time, end_time)
        #             project_code = db.execute_sql(conn, sql_main)
        #             if len(project_code) != 0:
        #                 for m_main_code in project_code:
        #                     for main_code_str in m_main_code:
        #                         sql_code = """
        #                                                SELECT m_main_department_preset_working_hours FROM {0}.m_main_department where m_main_code = '{1}'
        #                                                """
        #                         sql = sql_code.format(company, main_code_str)
        #                         project_time = db.execute_sql(conn, sql)
        #                         s = 0
        #                         for one_code_time_tuple in project_time:
        #                             for one_code_time in one_code_time_tuple:
        #                                 s += float(one_code_time)
        #                         if project_ids[1] not in one_pro_dict.keys():
        #                             one_pro_dict[project_ids[1]] = s
        #                         else:
        #                             one_pro_dict[project_ids[1]] = s + float(
        #                                 one_pro_dict[project_ids[1]])
        #         db.close_connection(conn)
        #
        #         all_test.append(one_pro_dict)
        #
        #         all_company_dict[company] = one_pro_dict
        #
        # print(all_project_name)
        #
        # print("------")
        #
        # print(all_company_dict)
        #
        # return data_list




        # print("----")
        # print(data_list)

