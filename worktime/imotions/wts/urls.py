from django.contrib import admin
from django.urls import path, re_path
from wts.views import RedisView, ReadProject, ReadOneProject, ReadCompanyBar, companyName,projectName,ReadOneProjectBar,ReadCompanyProject,ReadCompanyProjectBar,ReadProjectCompany,ReadProjectCompanyBar


urlpatterns = [
    path('admin/', admin.site.urls),
    #path('companyWorkHoursSum', RedisView.as_view())
    re_path(r"^companyWorkHoursSum$", RedisView.as_view()),      #一个公司在一段时间内每个人的总工时相加
    re_path(r"^projectWorkHoursSum$", ReadProject.as_view()),  # 返回每个公司里面在一段时间内的项目和每个项目的工时
    re_path(r"^oneProjectWorkHoursSum$", ReadOneProject.as_view()),   #一个项目在多个公司的工时总数
    re_path(r"^companyWorkHoursSumBar$", ReadCompanyBar.as_view()),   #返回每个公司在一段时间内所有项目的总工时
    re_path(r"^oneProjectWorkHoursSumBar$", ReadOneProjectBar.as_view()),
    #re_path(r"^projectWorkHoursSumBar$", ReadProjectBar.as_view()),
    # re_path(r"^whs$", test.as_view()),
    re_path(r"^companyName$", companyName.as_view()),
    re_path(r"^projectName$", projectName.as_view()),
    re_path(r"^companyWorkHoursSumProject$", ReadCompanyProject.as_view()),
    re_path(r"^companyWorkHoursSumProjectBar$", ReadCompanyProjectBar.as_view()),
    re_path(r"^projectWorkHoursSumCompany$", ReadProjectCompany.as_view()),    #  前端传入一个项目（cost_center），返回一个这个项目在各个公司的工时
    re_path(r"^projectWorkHoursSumCompanyBar$", ReadProjectCompanyBar.as_view())  # 前端传入一个项目（cost_center），返回一个这个项目在各个公司的工时和这个项目在各个公司相加的总工时，柱状图

    # re_path(r"^hhh", ttt.as_view())
    # path('companyWorkHoursSum', RedisView.as_view())

]