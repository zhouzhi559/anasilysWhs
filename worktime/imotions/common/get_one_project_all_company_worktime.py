from common.db import DB
from common.get_companys import get_company_list


class get_one_project_all_company_times:

    """
    得到一个项目在所有公司相加的总工时

    """


    def cos_and_project_name(self):

        db = DB()
        get_list = get_company_list()
        get_compa_list = get_list.get_all_databases()

        all_list = []


        list1 = ["imotion", "software", 'wjtech', 'pawithub', 'wjchin', 'wjip']

        for com in list1:
            if com == "imotion":
                conn = db.get_connection('imotion')
                sql = """                
                SELECT cost_center,project_name FROM imotion.project_info
                """
                drs = db.execute_sql(conn, sql)
                # print("*********")
                # print(drs)
                db.close_connection(conn)

                for dr in drs:
                    all_list.append([dr[0],dr[1]])

            if com == "software":
                conn = db.get_connection('software')
                sql = """
                                SELECT cost_center,project_name FROM software.project_info
                                """
                drs = db.execute_sql(conn, sql)
                db.close_connection(conn)

                for dr in drs:
                    if len(dr[0]) !=8:
                        all_list.append([dr[0], dr[1]])

                    else:
                        for i in all_list:
                            if len(i[0])== 8 and i[0][-4:] != dr[0][-4:0]:
                                all_list.append([dr[0], dr[1]])


            if com == "wjtech":
                conn = db.get_connection('wjtech')
                sql = """
                                SELECT cost_center,project_name FROM wjtech.project_info
                                """
                drs = db.execute_sql(conn, sql)
                db.close_connection(conn)

                for dr in drs:
                    if len(dr[0]) !=8:
                        all_list.append([dr[0], dr[1]])

                    else:
                        for i in all_list:
                            if len(i[0])== 8 and i[0][-4:] != dr[0][-4:0]:
                                all_list.append([dr[0], dr[1]])

            if com == "pawithub":
                conn = db.get_connection('pawithub')
                sql = """
                                SELECT cost_center,project_name FROM pawithub.project_info
                                """
                drs = db.execute_sql(conn, sql)
                db.close_connection(conn)

                for dr in drs:
                    if len(dr[0]) !=8:
                        all_list.append([dr[0], dr[1]])

                    else:
                        for i in all_list:
                            if len(i[0])== 8 and i[0][-4:] != dr[0][-4:0]:
                                all_list.append([dr[0], dr[1]])

            if com == "wjchin":
                conn = db.get_connection('wjchin')
                sql = """
                                SELECT cost_center,project_name FROM wjchin.project_info
                                """
                drs = db.execute_sql(conn, sql)
                db.close_connection(conn)

                for dr in drs:
                    if len(dr[0]) !=8:
                        all_list.append([dr[0], dr[1]])

                    else:
                        for i in all_list:
                            if len(i[0])== 8 and i[0][-4:] != dr[0][-4:0]:
                                all_list.append([dr[0], dr[1]])

            if com == "wjip":
                conn = db.get_connection('wjip')
                sql = """
                                SELECT cost_center,project_name FROM wjip.project_info
                                """
                drs = db.execute_sql(conn, sql)
                db.close_connection(conn)

                for dr in drs:
                    if len(dr[0]) !=8:
                        all_list.append([dr[0], dr[1]])

                    else:
                        for i in all_list:
                            if len(i[0])== 8 and i[0][-4:] != dr[0][-4:0]:
                                all_list.append([dr[0], dr[1]])



            return all_list


    def get_one_project_all_com(self, start_time, end_time):
        # cos_name = []
        cos_names = self.cos_and_project_name()

        # print(cos_names)

        project_name_dict = {}

        one_project_name_dict = {}
        # start_time = '2021-05-01 00:00:00.000000'
        # end_time = '2021-06-01 00:00:00.000000'

        db = DB()
        one_project_dict = {}
        get_list = get_company_list()
        get_compa_list = get_list.get_all_databases()
        for company in get_compa_list:
            if company =="imotion":
                conn = db.get_connection('imotion')
                sql = """
                SELECT cost_center,sum(m_branches_department_preset_working_hours), project_name              
                FROM imotion.project_info as a left join imotion.m_main as b 
                on a.project_id = b.m_m_project_id left join imotion.m_branches as c 
                on c.m_main_code=b.m_main_code left join imotion.m_branches_department as d 
                on d.m_branches_code=c.m_branches_code 
                where m_branches_preset_start_at>='{0}' 
                and m_branches_preset_end_at<='{1}' group by m_main_cost_center;
                """
                sql_main = sql.format(start_time, end_time)
                drs = db.execute_sql(conn, sql_main)
                db.close_connection(conn)
                for dr in drs:

                    one_project_dict[dr[0]] = dr[1]
                    one_project_name_dict[dr[2]] = dr[1]

            if company == "software":
                conn = db.get_connection('software')
                sql = """
                               SELECT cost_center,sum(m_branches_department_preset_working_hours)               
                               FROM software.project_info as a left join software.m_main as b 
                               on a.project_id = b.m_m_project_id left join software.m_branches as c 
                               on c.m_main_code=b.m_main_code left join software.m_branches_department as d 
                               on d.m_branches_code=c.m_branches_code 
                               where m_branches_preset_start_at>='{0}' 
                               and m_branches_preset_end_at<='{1}' group by m_main_cost_center;
                               """
                sql_main = sql.format(start_time, end_time)
                drs = db.execute_sql(conn, sql_main)
                db.close_connection(conn)
                for dr in drs:
                    if len(dr[0]) == 8:
                        imotion_keys = one_project_dict.keys()
                        for i in list(imotion_keys):
                            if len(i) == 8 and dr[0][-4:] == i[-4:]:
                                one_project_dict[i] = one_project_dict[i] + dr[1]

                                # print("------")
                                # print(one_project_name_dict)

                            else:
                                one_project_dict[dr[0]] = dr[1]
                    else:
                        one_project_dict[dr[0]] = dr[1]

            if company == "wjtech":
                conn = db.get_connection('wjtech')
                sql = """
                               SELECT cost_center,sum(m_branches_department_preset_working_hours)
                               FROM wjtech.project_info as a left join wjtech.m_main as b
                               on a.project_id = b.m_m_project_id left join wjtech.m_branches as c
                               on c.m_main_code=b.m_main_code left join wjtech.m_branches_department as d
                               on d.m_branches_code=c.m_branches_code
                               where m_branches_preset_start_at>='{0}'
                               and m_branches_preset_end_at<='{1}' group by m_main_cost_center;
                               """
                sql_main = sql.format(start_time, end_time)
                drs = db.execute_sql(conn, sql_main)
                db.close_connection(conn)
                for dr in drs:

                    #print(dr)
                    if len(dr[0]) == 8:
                        imotion_keys = one_project_dict.keys()
                        for i in list(imotion_keys):
                            if len(i) == 8 and dr[0][-4:] == i[-4:]:
                                one_project_dict[i] = one_project_dict[i] + dr[1]

                            else:
                                one_project_dict[dr[0]] = dr[1]
                    else:
                        one_project_dict[dr[0]] = dr[1]

            if company == "pawithub":
                conn = db.get_connection('pawithub')
                sql = """
                               SELECT cost_center,sum(m_branches_department_preset_working_hours)
                               FROM pawithub.project_info as a left join pawithub.m_main as b
                               on a.project_id = b.m_m_project_id left join pawithub.m_branches as c
                               on c.m_main_code=b.m_main_code left join pawithub.m_branches_department as d
                               on d.m_branches_code=c.m_branches_code
                               where m_branches_preset_start_at>='{0}'
                               and m_branches_preset_end_at<='{1}' group by m_main_cost_center;
                               """
                sql_main = sql.format(start_time, end_time)
                drs = db.execute_sql(conn, sql_main)
                db.close_connection(conn)
                for dr in drs:
                    # print(dr)
                    if len(dr[0]) == 8:
                        imotion_keys = one_project_dict.keys()
                        for i in list(imotion_keys):
                            if len(i) == 8 and dr[0][-4:] == i[-4:]:
                                one_project_dict[i] = one_project_dict[i] + dr[1]

                            else:
                                one_project_dict[dr[0]] = dr[1]
                    else:
                        one_project_dict[dr[0]] = dr[1]

            if company == "wjchin":
                conn = db.get_connection('wjchin')
                sql = """
                               SELECT cost_center,sum(m_branches_department_preset_working_hours)
                               FROM wjchin.project_info as a left join wjchin.m_main as b
                               on a.project_id = b.m_m_project_id left join wjchin.m_branches as c
                               on c.m_main_code=b.m_main_code left join wjchin.m_branches_department as d
                               on d.m_branches_code=c.m_branches_code
                               where m_branches_preset_start_at>='{0}'
                               and m_branches_preset_end_at<='{1}' group by m_main_cost_center;
                               """
                sql_main = sql.format(start_time, end_time)
                drs = db.execute_sql(conn, sql_main)
                db.close_connection(conn)
                for dr in drs:
                    print(dr)
                    if len(dr[0]) == 8:
                        imotion_keys = one_project_dict.keys()
                        for i in list(imotion_keys):
                            if len(i) == 8 and dr[0][-4:] == i[-4:]:
                                one_project_dict[i] = one_project_dict[i] + dr[1]

                            else:
                                one_project_dict[dr[0]] = dr[1]
                    else:
                        one_project_dict[dr[0]] = dr[1]

            if company == "wjip":
                conn = db.get_connection('wjip')
                sql = """
                               SELECT cost_center,sum(m_branches_department_preset_working_hours)
                               FROM wjip.project_info as a left join wjip.m_main as b
                               on a.project_id = b.m_m_project_id left join wjip.m_branches as c
                               on c.m_main_code=b.m_main_code left join wjip.m_branches_department as d
                               on d.m_branches_code=c.m_branches_code
                               where m_branches_preset_start_at>='{0}'
                               and m_branches_preset_end_at<='{1}' group by m_main_cost_center;
                               """
                sql_main = sql.format(start_time, end_time)
                drs = db.execute_sql(conn, sql_main)
                db.close_connection(conn)
                for dr in drs:
                    print(dr)
                    if len(dr[0]) == 8:
                        imotion_keys = one_project_dict.keys()
                        for i in list(imotion_keys):
                            if len(i) == 8 and dr[0][-4:] == i[-4:]:
                                one_project_dict[i] = one_project_dict[i] + dr[1]

                            else:
                                one_project_dict[dr[0]] = dr[1]
                    else:
                        one_project_dict[dr[0]] = dr[1]


        for cos_name_project in cos_names:
            if cos_name_project[0] in one_project_dict.keys():
                project_name_dict[cos_name_project[1]] = one_project_dict[cos_name_project[0]]

        print("=====================")
        print(project_name_dict)













        # print("---------")
        # print(one_project_dict)

        return project_name_dict



