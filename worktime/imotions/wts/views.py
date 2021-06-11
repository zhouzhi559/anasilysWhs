from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
import json
from common.get_companys import get_company_list
import logging
from pymysql import connect
from common.db import DB
import requests

from common.get_one_project_worktimes import get_proiect_times
from common.get_company_worktime import get_com_work
from common.get_one_company_all_project_show import get_one_company_all_project
from common.get_one_project_all_company_worktime import get_one_project_all_company_times

from common.get_all_times import get_all_times
from common.one_company_worktimes import get_one_company_worktimes

from common.company_analysis_project import company_analysis_project
from common.one_project_anyone_company_worktimes import get_one_project_anycompany_times

logger = logging.getLogger(__name__)

# Create your views here.


class ReadProject(View):

    def get_data(self, start_time, end_time):
        df = get_one_company_all_project()
        data = df.get_one_company_all_project(start_time, end_time)

        return data

    def get(self, request):
        start_time = request.GET.get("startTime")
        end_time = request.GET.get("endTime")

        data = self.get_data(start_time, end_time)

        data = json.dumps(data)
        return HttpResponse(data)








class ReadCompanyBar(View):


    def get_company_worktimes(self, start_time, end_time):

        get_data = get_com_work()

        data = get_data.get_com_time(start_time, end_time)

        return data



    """
      得到每个公司的项目发生工时和累计发生工时 以列表的形式返回
    """

    def get_company_bar(self, start_time, end_time):

        try:

            # start_time = '2021-05-01 00:00:00.000000'  # 前端需要传入的开始时间参数，测试时候写死，实际上需要request.post.get
            # end_time = '2021-06-01 00:00:00.000000'

            data_worktimes = self.get_company_worktimes(start_time, end_time)
            companyXAxisData_list = []
            companyProjectHoursData_list = []
            companyWorkHoursData_list = []
            response_data={}
            company_worktime_dict = {}  # 所有公司的工时，以json形式返回
            department_dict_time = {}  # 所有部门的工时，以json形式返回

            # list_company = tuple()


            # start_time = start_time
            # end_time = end_time

            # start_time = '2021-03-01 00:00:00.000000'    # 前端需要传入的开始时间参数，测试时候写死，实际上需要request.post.get
            # end_time = '2021-03-31 00:00:00.000000'       # 前端需要传入的开始时间参数，测试时候写死，实际上需要request.post.get
            # params = [start_time, end_time]
            db = DB()
            companys = get_company_list()
            company_list = companys.get_all_databases()  # 得到所有的公司

            for data_company in company_list:

                if data_company == "imotion":


                    companyXAxisData_list.append("时新(上海)产品设计有限公司")
                    imotion_project_time = ""
                    imotion_work_time = ""
                    conn = db.get_connection("imotion")
                    sql = """
                    SELECT m_main_department_preset_working_hours
                    FROM imotion.m_main_department where m_main_department_preset_start_at >= '{0}' 
                    and m_main_department_preset_end_at <= '{1}'               
                    """
                    sql = sql.format(start_time, end_time)
                    print(sql)
                    data_departments = db.execute_sql(conn, sql)
                    db.close_connection(conn)
                    # print("+++++++++")
                    # print(data_departments)
                    if len(data_departments) != 0:
                        s = 0
                        for data_department in data_departments:
                            for data_department_str in data_department:
                                s += int(float(data_department_str))

                        imotion_project_time = s

                        print(imotion_project_time)

                        companyProjectHoursData_list.append(imotion_project_time)

                        print(companyProjectHoursData_list)

                    else:
                        imotion_project_time = 0
                        companyProjectHoursData_list.append(imotion_project_time)

                    conn_work = db.get_connection("imotion")
                    sql_work = """
                           SELECT count(Date) FROM imotion.work_date where Description = '工作日' and Date>= '{0}' and Date <='{1}'               
                    """
                    sql_work_format = sql_work.format(start_time, end_time)
                    print(sql_work_format)
                    data_day = db.execute_sql(conn_work, sql_work_format)
                    data_day_int = data_day[0][0]

                    print(data_day_int)

                    sql_get_person = """
                        SELECT count(*) FROM imotion.user_job_info where assess_enable = '1';  
                    
                    """
                    sql_get_person = sql_get_person.format(start_time, end_time)
                    print(sql_get_person)

                    person_all = db.execute_sql(conn_work, sql_get_person)
                    person_all_int = person_all[0][0]

                    print(person_all_int)

                    sql_get_overworktime = """                   
                      SELECT duration FROM imotion.overtime_records where payment_method="加班薪资" and start_at >="{0}" and end_at<="{1}";
                    """
                    sql_get_overworktime = sql_get_overworktime.format(start_time, end_time)

                    overtime_work = db.execute_sql(conn_work, sql_get_overworktime)
                    print("============")

                    print(overtime_work)
                    work_overtime_all = 0
                    for i in overtime_work:
                        for hour_one in i:
                            work_overtime_all+=float(hour_one)

                    print(work_overtime_all)

                    imotion_work_time = data_day_int * 8 * person_all_int + work_overtime_all

                    print("--------------------------------------------------")

                    print(imotion_work_time)
                    companyWorkHoursData_list.append(imotion_work_time)

                    db.close_connection(conn_work)

                if data_company == "software":
                    companyXAxisData_list.append("无界工场(上海)软件科技有限公司")
                    software_project_time = ""
                    software_work_time = ""
                    conn = db.get_connection("software")
                    sql = """
                    SELECT m_main_department_preset_working_hours
                    FROM software.m_main_department where m_main_department_preset_start_at >= '{0}' 
                    and m_main_department_preset_end_at <= '{1}'               
                    """
                    sql = sql.format(start_time, end_time)
                    print(sql)
                    data_departments = db.execute_sql(conn, sql)
                    db.close_connection(conn)
                    # print("+++++++++")
                    # print(data_departments)
                    if len(data_departments) != 0:
                        s = 0
                        for data_department in data_departments:
                            for data_department_str in data_department:
                                s += int(float(data_department_str))

                        software_project_time = s

                        print(software_project_time)

                        companyProjectHoursData_list.append(software_project_time)

                        print(companyProjectHoursData_list)

                    else:
                        software_project_time = 0
                        companyProjectHoursData_list.append(software_project_time)

                    conn_work = db.get_connection("software")
                    sql_work = """
                           SELECT count(Date) FROM software.work_date where Description = '工作日' and Date>= '{0}' and Date <='{1}'               
                    """
                    sql_work_format = sql_work.format(start_time, end_time)
                    print(sql_work_format)
                    data_day = db.execute_sql(conn_work, sql_work_format)
                    data_day_int = data_day[0][0]

                    print(data_day_int)

                    sql_get_person = """
                        SELECT count(*) FROM software.user_job_info where assess_enable = '1';  
                    
                    """
                    sql_get_person = sql_get_person.format(start_time, end_time)
                    print(sql_get_person)

                    person_all = db.execute_sql(conn_work, sql_get_person)
                    person_all_int = person_all[0][0]

                    print(person_all_int)

                    sql_get_overworktime = """                   
                      SELECT duration FROM software.overtime_records where payment_method="加班薪资" and start_at >="{0}" and end_at<="{1}";
                    """
                    sql_get_overworktime = sql_get_overworktime.format(start_time, end_time)

                    overtime_work = db.execute_sql(conn_work, sql_get_overworktime)
                    print("============")

                    if len(overtime_work) != 0:

                        print(overtime_work)
                        work_overtime_all = 0
                        for i in overtime_work:
                            for hour_one in i:
                                work_overtime_all+=float(hour_one)

                        print(work_overtime_all)

                    else:
                        work_overtime_all = 0


                    software_work_time = data_day_int * 8 * person_all_int + work_overtime_all

                    print("--------------------------------------------------")

                    print(software_work_time)

                    db.close_connection(conn_work)
                    companyWorkHoursData_list.append(software_work_time)

                if data_company == "wjtech":
                    companyXAxisData_list.append("无界工场(上海)设计科技有限公司")
                    wjtech_project_time = ""
                    wjtech_work_time = ""
                    conn = db.get_connection("wjtech")
                    sql = """
                    SELECT m_main_department_preset_working_hours
                    FROM wjtech.m_main_department where m_main_department_preset_start_at >= '{0}' 
                    and m_main_department_preset_end_at <= '{1}'               
                    """
                    sql = sql.format(start_time, end_time)
                    print(sql)
                    data_departments = db.execute_sql(conn, sql)
                    db.close_connection(conn)
                    # print("+++++++++")
                    # print(data_departments)
                    if len(data_departments) != 0:
                        s = 0
                        for data_department in data_departments:
                            for data_department_str in data_department:
                                s += int(float(data_department_str))

                        wjtech_project_time = s

                        print(wjtech_project_time)

                        companyProjectHoursData_list.append(wjtech_project_time)

                        print(companyProjectHoursData_list)

                    else:
                        wjtech_project_time = 0
                        companyProjectHoursData_list.append(wjtech_project_time)

                    conn_work = db.get_connection("wjtech")
                    sql_work = """
                           SELECT count(Date) FROM wjtech.work_date where Description = '工作日' and Date>= '{0}' and Date <='{1}'               
                    """
                    sql_work_format = sql_work.format(start_time, end_time)
                    print(sql_work_format)
                    data_day = db.execute_sql(conn_work, sql_work_format)
                    data_day_int = data_day[0][0]

                    print(data_day_int)

                    sql_get_person = """
                        SELECT count(*) FROM wjtech.user_job_info where assess_enable = '1';  
                    
                    """
                    sql_get_person = sql_get_person.format(start_time, end_time)
                    print(sql_get_person)

                    person_all = db.execute_sql(conn_work, sql_get_person)
                    person_all_int = person_all[0][0]

                    print(person_all_int)

                    sql_get_overworktime = """                   
                      SELECT duration FROM wjtech.overtime_records where payment_method="加班薪资" and start_at >="{0}" and end_at<="{1}";
                    """
                    sql_get_overworktime = sql_get_overworktime.format(start_time, end_time)

                    overtime_work = db.execute_sql(conn_work, sql_get_overworktime)
                    print("============")

                    if len(overtime_work) != 0:

                        print(overtime_work)
                        work_overtime_all = 0
                        for i in overtime_work:
                            for hour_one in i:
                                work_overtime_all+=float(hour_one)

                        print(work_overtime_all)

                    else:
                        work_overtime_all = 0


                    wjtech_work_time = data_day_int * 8 * person_all_int + work_overtime_all

                    print("--------------------------------------------------")

                    print(wjtech_work_time)

                    db.close_connection(conn_work)
                    companyWorkHoursData_list.append(wjtech_work_time)


                if data_company == "pawithub":
                    companyXAxisData_list.append("上海慧瞰科技有限公司")
                    pawithub_project_time = ""
                    pawithub_work_time = ""
                    conn = db.get_connection("pawithub")
                    sql = """
                    SELECT m_main_department_preset_working_hours
                    FROM pawithub.m_main_department where m_main_department_preset_start_at >= '{0}' 
                    and m_main_department_preset_end_at <= '{1}'               
                    """
                    sql = sql.format(start_time, end_time)
                    print(sql)
                    data_departments = db.execute_sql(conn, sql)
                    db.close_connection(conn)
                    # print("+++++++++")
                    # print(data_departments)
                    if len(data_departments) != 0:
                        s = 0
                        for data_department in data_departments:
                            for data_department_str in data_department:
                                s += int(float(data_department_str))

                        pawithub_project_time = s

                        print(pawithub_project_time)

                        companyProjectHoursData_list.append(pawithub_project_time)

                        print(companyProjectHoursData_list)

                    else:
                        pawithub_project_time = 0
                        companyProjectHoursData_list.append(pawithub_project_time)

                    conn_work = db.get_connection("pawithub")
                    sql_work = """
                           SELECT count(Date) FROM pawithub.work_date where Description = '工作日' and Date>= '{0}' and Date <='{1}'               
                    """
                    sql_work_format = sql_work.format(start_time, end_time)
                    print(sql_work_format)
                    data_day = db.execute_sql(conn_work, sql_work_format)
                    data_day_int = data_day[0][0]

                    print(data_day_int)

                    sql_get_person = """
                        SELECT count(*) FROM pawithub.user_job_info where assess_enable = '1';  
                    
                    """
                    sql_get_person = sql_get_person.format(start_time, end_time)
                    print(sql_get_person)

                    person_all = db.execute_sql(conn_work, sql_get_person)
                    person_all_int = person_all[0][0]

                    print(person_all_int)

                    sql_get_overworktime = """                   
                      SELECT duration FROM pawithub.overtime_records where payment_method="加班薪资" and start_at >="{0}" and end_at<="{1}";
                    """
                    sql_get_overworktime = sql_get_overworktime.format(start_time, end_time)

                    overtime_work = db.execute_sql(conn_work, sql_get_overworktime)
                    print("============")

                    if len(overtime_work) != 0:

                        print(overtime_work)
                        work_overtime_all = 0
                        for i in overtime_work:
                            for hour_one in i:
                                work_overtime_all+=float(hour_one)

                        print(work_overtime_all)

                    else:
                        work_overtime_all = 0


                    pawithub_work_time = data_day_int * 8 * person_all_int + work_overtime_all

                    print("--------------------------------------------------")

                    print(pawithub_work_time)

                    db.close_connection(conn_work)
                    companyWorkHoursData_list.append(pawithub_work_time)


                if data_company == "wjchin":
                    companyXAxisData_list.append("无界国创（成都）科技有限公司")
                    wjchin_project_time = ""
                    wjchin_work_time = ""
                    conn = db.get_connection("wjchin")
                    sql = """
                    SELECT m_main_department_preset_working_hours
                    FROM wjchin.m_main_department where m_main_department_preset_start_at >= '{0}' 
                    and m_main_department_preset_end_at <= '{1}'               
                    """
                    sql = sql.format(start_time, end_time)
                    print(sql)
                    data_departments = db.execute_sql(conn, sql)
                    db.close_connection(conn)
                    # print("+++++++++")
                    # print(data_departments)
                    if len(data_departments) != 0:
                        s = 0
                        for data_department in data_departments:
                            for data_department_str in data_department:
                                s += int(float(data_department_str))

                        wjchin_project_time = s

                        print(wjchin_project_time)

                        companyProjectHoursData_list.append(wjchin_project_time)

                        print(companyProjectHoursData_list)

                    else:
                        wjchin_project_time = 0
                        companyProjectHoursData_list.append(wjchin_project_time)

                    conn_work = db.get_connection("wjchin")
                    sql_work = """
                           SELECT count(Date) FROM wjchin.work_date where Description = '工作日' and Date>= '{0}' and Date <='{1}'               
                    """
                    sql_work_format = sql_work.format(start_time, end_time)
                    print(sql_work_format)
                    data_day = db.execute_sql(conn_work, sql_work_format)
                    data_day_int = data_day[0][0]

                    print(data_day_int)

                    sql_get_person = """
                        SELECT count(*) FROM wjchin.user_job_info where assess_enable = '1';  
                    
                    """
                    sql_get_person = sql_get_person.format(start_time, end_time)
                    print(sql_get_person)

                    person_all = db.execute_sql(conn_work, sql_get_person)
                    person_all_int = person_all[0][0]

                    print(person_all_int)

                    sql_get_overworktime = """                   
                      SELECT duration FROM wjchin.overtime_records where payment_method="加班薪资" and start_at >="{0}" and end_at<="{1}";
                    """
                    sql_get_overworktime = sql_get_overworktime.format(start_time, end_time)

                    overtime_work = db.execute_sql(conn_work, sql_get_overworktime)
                    print("============")

                    if len(overtime_work) != 0:

                        print(overtime_work)
                        work_overtime_all = 0
                        for i in overtime_work:
                            for hour_one in i:
                                work_overtime_all+=float(hour_one)

                        print(work_overtime_all)

                    else:
                        work_overtime_all = 0


                    wjchin_work_time = data_day_int * 8 * person_all_int + work_overtime_all

                    print("--------------------------------------------------")

                    print(wjchin_work_time)

                    db.close_connection(conn_work)
                    companyWorkHoursData_list.append(wjchin_work_time)

                if data_company == "wjip":
                    companyXAxisData_list.append("无界工场（上海）知识产权服务有限公司")
                    wjip_project_time = ""
                    wjip_work_time = ""
                    conn = db.get_connection("wjip")
                    sql = """
                    SELECT m_main_department_preset_working_hours
                    FROM wjip.m_main_department where m_main_department_preset_start_at >= '{0}' 
                    and m_main_department_preset_end_at <= '{1}'               
                    """
                    sql = sql.format(start_time, end_time)
                    print(sql)
                    data_departments = db.execute_sql(conn, sql)
                    db.close_connection(conn)
                    # print("+++++++++")
                    # print(data_departments)
                    if len(data_departments) != 0:
                        s = 0
                        for data_department in data_departments:
                            for data_department_str in data_department:
                                s += int(float(data_department_str))

                        wjip_project_time = s

                        print(wjip_project_time)

                        companyProjectHoursData_list.append(wjip_project_time)

                        print(companyProjectHoursData_list)

                    else:
                        wjip_project_time = 0
                        companyProjectHoursData_list.append(wjip_project_time)

                    conn_work = db.get_connection("wjip")
                    sql_work = """
                           SELECT count(Date) FROM wjip.work_date where Description = '工作日' and Date>= '{0}' and Date <='{1}'               
                    """
                    sql_work_format = sql_work.format(start_time, end_time)
                    print(sql_work_format)
                    data_day = db.execute_sql(conn_work, sql_work_format)
                    data_day_int = data_day[0][0]

                    print(data_day_int)

                    sql_get_person = """
                        SELECT count(*) FROM wjip.user_job_info where assess_enable = '1';  
                    
                    """
                    sql_get_person = sql_get_person.format(start_time, end_time)
                    print(sql_get_person)

                    person_all = db.execute_sql(conn_work, sql_get_person)
                    person_all_int = person_all[0][0]

                    print(person_all_int)

                    sql_get_overworktime = """                   
                      SELECT duration FROM wjip.overtime_records where payment_method="加班薪资" and start_at >="{0}" and end_at<="{1}";
                    """
                    sql_get_overworktime = sql_get_overworktime.format(start_time, end_time)

                    overtime_work = db.execute_sql(conn_work, sql_get_overworktime)
                    print("============")

                    if len(overtime_work) != 0:

                        print(overtime_work)
                        work_overtime_all = 0
                        for i in overtime_work:
                            for hour_one in i:
                                work_overtime_all+=float(hour_one)

                        print(work_overtime_all)

                    else:
                        work_overtime_all = 0


                    wjip_work_time = data_day_int * 8 * person_all_int + work_overtime_all

                    print("--------------------------------------------------")

                    print(wjip_work_time)

                    db.close_connection(conn_work)
                    companyWorkHoursData_list.append(wjip_work_time)


            companyProjectHoursData_list = list(data_worktimes['realiy_work_time'])
            companyPredictProjectTimes_list = list(data_worktimes['predict_work_time'])

                
            
            response_data['companyXAxisData'] = companyXAxisData_list
            response_data['companyProjectHoursData'] = companyProjectHoursData_list
            response_data['companyWorkHoursData'] = companyWorkHoursData_list
            response_data['companyPredictProjectTimes'] = companyPredictProjectTimes_list

            print(response_data)

            return response_data

            
        except Exception as e:

            print(e)



    def get(self, request):

        start_time = request.GET.get("startTime")
        end_time = request.GET.get("endTime")

        # data = {"message" : "shjakshda"}

        data = self.get_company_bar(start_time, end_time)

        print("-----------")

        print(data)

        data = json.dumps(data)

        return HttpResponse(data)


# class test(View):
#
#
#     def get_data(self):
#
#         df = get_proiect_times()
#
#         df.get_one_pro_worktimes()
#
#     def get(self,request):
#
#         data = {'mesage': 'ok'}
#
#         self.get_data()
#
#
#
#         data = json.dumps(data)
#         return HttpResponse(data)


class companyName(View):

    def get_data(self):

        company_dict = {}

        _flag = "@imotion.group"
        company_list = []
        db = DB()
        conn = db.get_connection("imotionwhs")
        sql = "select companyname, suffix, mail from companyregister"
        dr = db.execute_sql(conn, sql)
        # print(dr)
        # print('end')

        db.close_connection(conn)

        if len(dr) > 0:
            for data in dr:
                if data[1] !="msgtest" and data[1] != "zhitest":
                    company_dict[data[0]] = data[1]

        else:
            company_dict = {}

            # print(company_list)
        return company_dict





    def get(self, request):

        data = self.get_data()

        print(data)






        data = json.dumps(data)

        return HttpResponse(data)

class projectName(View):

    def get_project(self):

        all_pro_dict = {}

        all_list = []

        db = DB()
        all_4_data = []
        get_data = get_company_list()
        get_list = get_data.get_all_databases()
        all_dict = {}
        all_test = []
        imotion_project = []

        all_8_data = []
        conn = db.get_connection('imotion')
        sql = """
        
        SELECT project_id, project_name, cost_center FROM imotion.project_info;
        
        """
        datas = db.execute_sql(conn, sql)
        imotion_project_nt_8 = []
        imotion_project_8 = []

        for data in datas:
            if len(data[-1])!= 8:
                imotion_project_nt_8.append(list(data))
            else:
                imotion_project_8.append(list(data))



        print(imotion_project_nt_8)

        print("-----")

        print(imotion_project_8)
        imotion_project_8_4 = []

        for i in imotion_project_8:
            if i[-1][-5:-1] not in imotion_project_8_4:
                imotion_project_8_4.append(i[-1][-5:-1])

        not_imotion_project = []



        for company in get_list:
            if company != "imotion":
                conn = db.get_connection(company)

                sql = """
                SELECT project_id, project_name, cost_center FROM {0}.project_info;

                """
                sql_main = sql.format(company)

                drs = db.execute_sql(conn, sql_main)

                for dr in drs:

                    if len(dr[-1]) != 8:
                        imotion_project_nt_8.append(list(dr))

                    else:

                        all_8_data.append(list(dr))
        all_set = {}

        imotion_project_8.extend(all_8_data)

        for i in imotion_project_8:

            if i[-1][-5:-1] not in all_set.keys():
                all_set[i[-1][-4:]] = i

        print(all_set)

        print("======")
        print(list(all_set.values()))

        imotion_project_nt_8.extend(list(all_set.values()))

        for i in imotion_project_nt_8:
            all_dict[i[1]] = i[-1]

        print(all_dict)

        dic_new = dict([val, key] for key, val in all_dict.items())

        # print("-----------")
        #
        # print(dic_new)

        all_pro_dict = dict([val, key] for key, val in dic_new.items())

        print(all_pro_dict)




        return all_pro_dict

    def get(self,request):

        self.get_project()

        data = self.get_project()

        data = json.dumps(data)
        return HttpResponse(data)

class RedisView(View):

    def get_data(self, start_time, end_time):

        get_work = get_com_work()

        data = get_work.get_com_time(start_time, end_time)
        data = data['company_worktime_data']

        return data


    def get(self, request):
        start_time = request.GET.get("startTime")
        end_time = request.GET.get("endTime")



        data = self.get_data(start_time, end_time)


        # data = {"op" : 'ooo'}

        data = json.dumps(data)

        return HttpResponse(data)



class ReadOneProject(View):

    def get_data(self, start_time, end_time):
        df = get_one_project_all_company_times()
        data = df.get_one_project_all_com(start_time, end_time)

        return data

    def get(self, request):
        start_time = request.GET.get("startTime")
        end_time = request.GET.get("endTime")
        data = self.get_data(start_time, end_time)

        # data = {"oooo" : "ppppp"}

        data = json.dumps(data)

        return HttpResponse(data)

class ReadOneProjectBar(View):

    def get_data_project_time(self, start_time, end_time):
        df = get_one_project_all_company_times()
        data_project = df.get_one_project_all_com(start_time, end_time)
        return data_project

    def get_data_all_times(self, start_time, end_time):
        df = get_all_times()
        data = df.get_all_times(start_time, end_time)

        return data

    def get(self, request):
        start_time = request.GET.get("startTime")
        end_time = request.GET.get("endTime")
        data = {}

        data1 = self.get_data_all_times(start_time, end_time)
        data2 = self.get_data_project_time(start_time, end_time)

        data["all_worktimes"] = data1
        data["project_times"] = data2

        print(data)

        data = json.dumps(data)

        return HttpResponse(data)


class ReadCompanyProject(View):

    def get_company_analysis_project_data(self,company, start_time, end_time):
        company_project = company_analysis_project()

        data = company_project.get_company_analysis_project(company, start_time, end_time)

        return data



    def get(self, request):
        start_time = request.GET.get("startTime")
        end_time = request.GET.get("endTime")
        company = request.GET.get("suffix")

        # start_time = "2021-05-01 00:00:00.000000"
        # end_time = "2021-06-01 00:00:00.000000"
        # company = "imotion"

        data = self.get_company_analysis_project_data(company, start_time, end_time)


        # data = {"message": 'ok'}

        data = json.dumps(data)

        return HttpResponse(data)


class ReadCompanyProjectBar(View):

    def get_all_time(self, company, start_time, end_time):
        all_times = get_one_company_worktimes()
        all_times_num = all_times.get_one_company_worktimes(company, start_time, end_time)
        return all_times_num
    def get_data(self, company, start_time, end_time):

        company_project = company_analysis_project()
        data = company_project.get_company_analysis_project(company, start_time, end_time)

        return data

    def get(self, request):
        start_time = request.GET.get("startTime")
        end_time = request.GET.get("endTime")
        company = request.GET.get("suffix")
        data = {}

        # start_time = "2021-05-01 00:00:00.000000"
        # end_time = "2021-06-01 00:00:00.000000"
        # company = "imotion"
        data_project = self.get_data(company, start_time, end_time)

        one_company_worktimes = self.get_all_time(company, start_time, end_time)
        # data = {'daya': 'sds'}
        data['one_company_project'] = data_project
        data['one_company_allworktimes'] = one_company_worktimes

        data = json.dumps(data)

        return HttpResponse(data)

class ReadProjectCompany(View):

    def get_data(self, start_time, end_time, cost_center):
        get_data = get_one_project_anycompany_times()
        get_one_project_company = get_data.get_one_project_companys(start_time, end_time, cost_center)

        return get_one_project_company



    def get(self, request):
        start_time = request.GET.get("startTime")
        end_time = request.GET.get("endTime")
        project = request.GET.get("costCenter")

        # start_time = "2021-02-01 00:00:00.000000"
        # end_time = "2021-06-01 00:00:00.000000"
        # project = "11312839"

        data = self.get_data(start_time, end_time, project)

        # data = {"io": 'sdsd'}

        data = json.dumps(data)

        return HttpResponse(data)



class ReadProjectCompanyBar(View):

    def get_data(self, start_time, end_time, cost_center):
        data = {}

        get_data = get_one_project_anycompany_times()
        get_one_project_company = get_data.get_one_project_companys(start_time, end_time, cost_center)
        one_project_wts = get_one_project_company.values()  # 一个项目在各个公司的工时列表
        one_pro_all_wts = sum(one_project_wts)              #一个项目的总工时

        data['one_project_company_wts_list'] = get_one_project_company
        data['one_pro_all_wts'] = one_pro_all_wts



        return data

        


    def get(self, request):
        start_time = request.GET.get("startTime")
        end_time = request.GET.get("endTime")
        project = request.GET.get("costCenter")


        
        # start_time = "2021-02-01 00:00:00.000000"
        # end_time = "2021-06-01 00:00:00.000000"
        # project = "11312839"

        data = self.get_data(start_time, end_time, project)

        print("---------------------")

        print(data)



        # data = {"message": "okkkkk"}

        data = json.dumps(data)

        return HttpResponse(data)










