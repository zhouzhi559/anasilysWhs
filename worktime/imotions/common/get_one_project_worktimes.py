from common.get_companys import get_company_list
from common.db import DB


class get_proiect_times:

    def get_one_pro_worktimes(self):

        # start_time = '2021-05-01 00:00:00.000000'
        # end_time = '2021-06-01 00:00:00.000000'
        all_project_name = []

        all_project = {}

        all_test = []

        db = DB()

        data = get_company_list()

        data_list = data.get_all_databases()

        all_company_dict = {}

        all_list = []

        for company in data_list:

            if company == "imotion":
                imotion_dict = {}
                imotion_data = []
                conn = db.get_connection("imotion")

                sql = """
                     SELECT project_id, project_name, sum(m_branches_department_preset_working_hours),cost_center FROM imotion.project_info as a left join 
                     imotion.m_main as b on a.project_id = b.m_m_project_id 
                     left join imotion.m_branches as c on c.m_main_code=b.m_main_code 
                     left join imotion.m_branches_department as d on d.m_branches_code=c.m_branches_code 
                     where m_branches_preset_start_at>='{0}'
                      and m_branches_preset_end_at<='{1}' group by project_id;
                    """

                sql_main = sql.format(start_time, end_time)

                print(sql_main)

                project_id_names = db.execute_sql(conn, sql_main)

                for project_id_name in project_id_names:
                    imotion_data.append(list(project_id_name))
                    all_list.append(list(project_id_name))

                all_project['imotion'] = imotion_data

                print(imotion_data)

            if company == "software":
                software_dict = {}
                software_data = []
                conn = db.get_connection("software")

                sql = """
                     SELECT project_id, project_name, sum(m_branches_department_preset_working_hours),cost_center FROM software.project_info as a left join 
                     software.m_main as b on a.project_id = b.m_m_project_id 
                     left join software.m_branches as c on c.m_main_code=b.m_main_code 
                     left join software.m_branches_department as d on d.m_branches_code=c.m_branches_code 
                     where m_branches_preset_start_at>='{0}'
                      and m_branches_preset_end_at<='{1}' group by project_id;
                    """

                sql_main = sql.format(start_time, end_time)

                print(sql_main)

                project_id_names = db.execute_sql(conn, sql_main)

                for project_id_name in project_id_names:
                    software_data.append(list(project_id_name))
                    all_list.append(list(project_id_name))

                all_project['software'] = software_data

                print(software_data)

            if company == "wjtech":
                wjtech_dict = {}
                wjtech_data = []
                conn = db.get_connection("wjtech")

                sql = """
                     SELECT project_id, project_name, sum(m_branches_department_preset_working_hours),cost_center FROM wjtech.project_info as a left join 
                     wjtech.m_main as b on a.project_id = b.m_m_project_id 
                     left join wjtech.m_branches as c on c.m_main_code=b.m_main_code 
                     left join wjtech.m_branches_department as d on d.m_branches_code=c.m_branches_code 
                     where m_branches_preset_start_at>='{0}'
                      and m_branches_preset_end_at<='{1}' group by project_id;
                    """

                sql_main = sql.format(start_time, end_time)

                print(sql_main)

                project_id_names = db.execute_sql(conn, sql_main)

                for project_id_name in project_id_names:
                    wjtech_data.append(list(project_id_name))
                    all_list.append(list(project_id_name))

                all_project['wjtech'] = wjtech_data

                print(wjtech_data)


            if company == "pawithub":
                pawithub_dict = {}
                pawithub_data = []
                conn = db.get_connection("pawithub")

                sql = """
                     SELECT project_id, project_name, sum(m_branches_department_preset_working_hours),cost_center FROM pawithub.project_info as a left join 
                     pawithub.m_main as b on a.project_id = b.m_m_project_id 
                     left join pawithub.m_branches as c on c.m_main_code=b.m_main_code 
                     left join pawithub.m_branches_department as d on d.m_branches_code=c.m_branches_code 
                     where m_branches_preset_start_at>='{0}'
                      and m_branches_preset_end_at<='{1}' group by project_id;
                    """

                sql_main = sql.format(start_time, end_time)

                print(sql_main)

                project_id_names = db.execute_sql(conn, sql_main)

                for project_id_name in project_id_names:
                    pawithub_data.append(list(project_id_name))
                    all_list.append(list(project_id_name))

                all_project['pawithub'] = pawithub_data

                print(pawithub_data)

            if company == "wjchin":
                wjchin_dict = {}
                wjchin_data = []
                conn = db.get_connection("wjchin")

                sql = """
                     SELECT project_id, project_name, sum(m_branches_department_preset_working_hours),cost_center FROM wjchin.project_info as a left join 
                     wjchin.m_main as b on a.project_id = b.m_m_project_id 
                     left join wjchin.m_branches as c on c.m_main_code=b.m_main_code 
                     left join wjchin.m_branches_department as d on d.m_branches_code=c.m_branches_code 
                     where m_branches_preset_start_at>='{0}'
                      and m_branches_preset_end_at<='{1}' group by project_id;
                    """

                sql_main = sql.format(start_time, end_time)

                print(sql_main)

                project_id_names = db.execute_sql(conn, sql_main)

                for project_id_name in project_id_names:
                    wjchin_data.append(list(project_id_name))
                    all_list.append(list(project_id_name))

                all_project['wjchin'] = wjchin_data

                print(wjchin_data)

            if company == "wjip":
                wjip_dict = {}
                wjip_data = []
                conn = db.get_connection("wjip")

                sql = """
                     SELECT project_id, project_name, sum(m_branches_department_preset_working_hours),cost_center FROM wjip.project_info as a left join 
                     wjip.m_main as b on a.project_id = b.m_m_project_id 
                     left join wjip.m_branches as c on c.m_main_code=b.m_main_code 
                     left join wjip.m_branches_department as d on d.m_branches_code=c.m_branches_code 
                     where m_branches_preset_start_at>='{0}'
                      and m_branches_preset_end_at<='{1}' group by project_id;
                    """

                sql_main = sql.format(start_time, end_time)

                print(sql_main)

                project_id_names = db.execute_sql(conn, sql_main)

                for project_id_name in project_id_names:
                    wjip_data.append(list(project_id_name))
                    all_list.append(list(project_id_name))

                all_project['wjip'] = wjip_data

                print(wjip_data)

        print("------")

        print(all_project)

        print("=====")

        project_ = []

        print(all_list)


        for i in all_list:

            if len(i[-1]) !=8:
                project_.append(i)

            else:
                pass




                # for project_name_type in project_id_names:
                #     project_name = project_name_type[1]
                #     if project_name not in all_project_name:
                #         all_project_name.append(project_name)
                # db.close_connection(conn)

                # conn = db.get_connection(company)

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
        # return data_list
        # print("----")
        # print(data_list)

# f = get_proiect_times()
#
# f.get_one_pro_worktimes()

# print(f.get_one_pro_worktimes())