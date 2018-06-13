import pandas as pd
from datetime import datetime
from functools import reduce
currentMonth = datetime.now().month
from datetime import date
lastyear_lastday = date(date.today().year-1, 12, 31)


current_month_file_path = 'Y:/款项登记/18年回款登记/2018-{}月回款/2018-{}月回款.xlsx'.format(currentMonth, currentMonth)
df_currentMonth = pd.read_excel(current_month_file_path, sheet_name='2018年{}月'.format(currentMonth))
df_currentMonth['收款日期'] = pd.to_datetime(df_currentMonth['收款日期'], format='%Y-%m-%d')
df_previous = pd.read_excel('Y:/款项登记/好视通客户成交管理-总表 .xlsx', sheet_name='2018年')
# budget
budget = pd.read_excel('Y:/款项登记/18年回款登记/业绩目标.xlsx', sheet_name=0)
# 离职人员名单
exit_employees = pd.read_excel('Y:/款项登记/18年回款登记/2018年入职登记表.xlsx', sheet_name='离职登记')
exit_employees = exit_employees[['离职日期','部门','姓名']]
exit_employees.离职日期 = pd.to_datetime(exit_employees['离职日期'], format='%Y-%m-%d')
exit_employees = exit_employees[(exit_employees['离职日期'].dt.month == currentMonth-1)]
exit_employee_department = set(exit_employees.部门.unique())
exit_employee_name = set(exit_employees.姓名.unique())


# helper function: return report columns
def make_column(targetColumn, columnName, data):
    df_target = data[['所属部门', targetColumn]].groupby('所属部门').sum()/10000
    df_target = df_target.reset_index()
    df_target = df_target.rename(index=str, columns={targetColumn: columnName})
    df_target = df_target.round(2)
    return df_target


def get_time_series():
    df_currentMonth = pd.read_excel(current_month_file_path, sheet_name='2018年{}月'.format(currentMonth))
    df_previous = pd.read_excel('Y:/款项登记/好视通客户成交管理-总表 .xlsx', sheet_name='2018年')
    df_ytd = df_previous.append(df_currentMonth)
    df_ytd['收款日期'] = pd.to_datetime(df_ytd['收款日期'], format='%Y-%m-%d')
    df_ytd.index = df_ytd['收款日期']
    df_ytd = df_ytd[(df_ytd['收款日期'] > lastyear_lastday)]

    # df_ytd['month'] = df_ytd['收款日期'].dt.strftime('%m')
    df_ytd['week'] = df_ytd['收款日期'].dt.strftime('%W')
    # df_ytd['day'] = df_ytd['收款日期'].dt.strftime('%d')

    df_ytd_week = df_ytd.groupby(['week']).sum()
    df_ytd_week = df_ytd_week.reset_index()
    df_ytd_week = df_ytd_week[['week','净现金业绩','本期收款']]

    return df_ytd_week

df_ytd_week = get_time_series()



def get_汇总表():
    # 本月收款
    本月收款 = make_column('本期收款', '本月收款', df_currentMonth)
    # 软件金额
    软件金额 = make_column('净现金业绩', '软件金额', df_currentMonth)
    # 单数_新签代理
    单数_新签代理 = df_currentMonth[['所属部门', '新单数']].groupby('所属部门').sum()
    单数_新签代理 = 单数_新签代理.reset_index()
    # 当日业绩
    df_currentMonth['收款日期'] = pd.to_datetime(df_currentMonth['收款日期'], format='%Y-%m-%d')
    df_today = df_currentMonth.loc[(df_currentMonth.收款日期 == datetime.today().strftime("%Y-%m-%d"))]
    当日业绩 = make_column('净现金业绩', '当日业绩', df_today)

    currentMonth_column_name = '{}月'.format(currentMonth)
    budget_currentMonth = budget[['部门', currentMonth_column_name, '2018年预测']]
    budget_currentMonth = budget_currentMonth.rename(index=str,
                                                     columns={'部门': '所属部门', budget_currentMonth.columns[1]: '月度任务'})
    # 之前月份累计收款
    之前月总收款 = make_column('本期收款', '之前月总收款', df_previous)
    # 之前月总业绩
    之前月总业绩 = make_column('净现金业绩', '之前月总业绩', df_previous)
    # 合并表
    dfs = [软件金额, budget_currentMonth, 单数_新签代理, 本月收款, 当日业绩, 之前月总收款, 之前月总业绩]
    合并表 = reduce(lambda left, right: pd.merge(left, right, on='所属部门', how='left'), dfs)
    合并表 = 合并表.fillna(0)

    # 年度累计收款
    合并表['年度累计收款'] = 合并表['本月收款'] + 合并表['之前月总收款']
    # 年度累计业绩
    合并表['年度累计业绩'] = 合并表['软件金额'] + 合并表['之前月总业绩']
    汇总 = 合并表.round(2)
    汇总 = 汇总.append(汇总.sum(numeric_only=True), ignore_index=True)
    汇总.iloc[-1, 0] = '汇总'
    汇总['月度完成率(%)'] = 汇总['软件金额'].div(汇总['月度任务']).multiply(100).round(2)
    汇总['年度达成率(%)'] = 汇总['年度累计业绩'].div(汇总['2018年预测']).multiply(100).round(2)
    汇总 = 汇总.round(2)
    汇总 = 汇总.astype(str)
    汇总 = 汇总.replace('inf',0)
    汇总 = 汇总.replace('nan', 0)
    汇总 = 汇总.replace('0.0', 0)
    汇总['月度完成率(%)'] = 汇总['月度完成率(%)'].astype(float)
    return 汇总

汇总 = get_汇总表()



def get_个人业绩YTD():
    # df_currentMonth = pd.read_excel(current_month_file_path, sheet_name='2018年{}月'.format(currentMonth))
    当月业绩 = df_currentMonth[['销售人员', '净现金业绩', '所属部门', '新单数']].groupby(['所属部门', '销售人员']).sum()
    当月业绩 = 当月业绩.reset_index()
    当月业绩 = 当月业绩.rename(index=str, columns={'净现金业绩': '{}月净现金业绩'.format(currentMonth)})

    # 获取：个人排名_前一个月份业绩 列表
    # 获取：个人排名_前一个月份业绩 列表
    i = 1
    df_list = []
    while i < currentMonth:
        previous_month_file_path = 'Y:/款项登记/18年回款登记/2018-{}月回款/2018-{}月回款.xlsx'.format(currentMonth - i,
                                                                                       currentMonth - i)
        last_month_df = pd.read_excel(previous_month_file_path, sheet_name='2018年{}月'.format(currentMonth - i))
        last_month_df = last_month_df[['所属部门', '销售人员', '净现金业绩']].groupby(['所属部门', '销售人员']).sum()
        last_month_df = last_month_df.reset_index()
        last_month_df = last_month_df.rename(index=str, columns={'净现金业绩': '{}月净现金业绩'.format(currentMonth - i)})
        #     last_month_df = last_month_df.reset_index()
        df_list.append(last_month_df)
        i += 1

    前单月业绩合并表 = reduce(lambda left, right: pd.merge(left, right, left_on=['所属部门', '销售人员'],
                                                   right_on=['所属部门', '销售人员'], how='outer'), df_list)
    个人业绩YTD = pd.merge(当月业绩, 前单月业绩合并表, left_on=['所属部门', '销售人员'],
                       right_on=['所属部门', '销售人员'], how='outer')
    个人业绩YTD['1-{}月净现金业绩'.format(currentMonth)] = 个人业绩YTD.sum(numeric_only=True, axis=1)
    个人业绩YTD = 个人业绩YTD.reset_index()
    个人业绩YTD = 个人业绩YTD.round(2)
    # 个人业绩YTD.iloc[:, 2:] = 个人业绩YTD.iloc[:, 2:].astype(float)
    个人业绩YTD = 个人业绩YTD.fillna(0)
    个人业绩YTD = 个人业绩YTD.drop(columns=['index'])
    个人业绩YTD = 个人业绩YTD.sort_values(['所属部门','{}月净现金业绩'.format(currentMonth)], ascending=[True,False])
    个人业绩YTD = 个人业绩YTD[~个人业绩YTD['销售人员'].isin(exit_employee_name) & ~个人业绩YTD['销售人员'].isin(exit_employee_department)]
    return 个人业绩YTD

个人业绩YTD = get_个人业绩YTD()



def get_业绩排名表():
    x = 0
    df_list_2 = []
    累计排名 = 个人业绩YTD[['所属部门','销售人员', '1-{}月净现金业绩'.format(currentMonth)]]
    累计排名['YTD累计排名'] = 累计排名['1-{}月净现金业绩'.format(currentMonth)].rank(ascending=False)
    累计排名 = 累计排名.drop(columns=['1-{}月净现金业绩'.format(currentMonth)])
    累计排名.YTD累计排名 = 累计排名.YTD累计排名.fillna(累计排名.YTD累计排名.max() + 2)

    df_list_2.append(累计排名)
    while x < currentMonth:
        previous_month_file_path='Y:/款项登记/18年回款登记/2018-{}月回款/2018-{}月回款.xlsx'.format(currentMonth-x,
                                                                                       currentMonth - x)
        last_month_df = pd.read_excel(previous_month_file_path, sheet_name='2018年{}月'.format(currentMonth - x))
        last_month_df = last_month_df[['销售人员', '净现金业绩']].groupby(['销售人员']).sum()
        last_month_df['{}月排名'.format(currentMonth - x)] = last_month_df['净现金业绩'].rank(ascending=False)
        last_month_df = last_month_df.drop(columns=['净现金业绩'])
        last_month_df = last_month_df.reset_index()
        df_list_2.append(last_month_df)
        x += 1

    业绩排名表 = reduce(lambda left, right: pd.merge(left, right, on='销售人员', how='outer' ), df_list_2)
    业绩排名表 = 业绩排名表.loc[业绩排名表['所属部门'] != '售后部']
    业绩排名表 = 业绩排名表.fillna(0)
    业绩排名表 = 业绩排名表.sort_values(['所属部门','{}月排名'.format(currentMonth)], ascending=[True,True])
    for column in 业绩排名表.ix[:, 2:]:
        业绩排名表[column] = 业绩排名表[column].fillna(int(业绩排名表[column].max()) + int(1))

    业绩排名表 = 业绩排名表[~业绩排名表['销售人员'].isin(exit_employee_name) & ~业绩排名表['销售人员'].isin(exit_employee_department)]
    return 业绩排名表

业绩排名表 = get_业绩排名表()



def get_办事处汇总表():
    # sales_by_team = 个人业绩YTD[['所属部门','{}月净现金业绩'.format(currentMonth),'1-{}月净现金业绩'.format(currentMonth)]]
    # sales_by_team = sales_by_team.groupby(['所属部门']).sum()/10000
    # sales_by_team = sales_by_team.reset_index()
    subset_汇总 = 汇总[['所属部门','软件金额','之前月总业绩','月度任务','月度完成率(%)']]
    subset_汇总 = subset_汇总.rename(index=str, columns={'软件金额': '{}月净现金业绩'.format(currentMonth)})
    # sales_by_team = pd.merge(sales_by_team, subset_汇总, on=['所属部门'])
    sales_by_team = subset_汇总.round(2)
    return sales_by_team

sales_by_team = get_办事处汇总表()

# export data files

encoding='gbk'
sep=','
export_path = 'C:/Users/Administrator/Desktop/db2/'

df_ytd_week.to_csv(export_path+'df_ytd_week.csv',encoding=encoding,index=False)
汇总.to_csv(export_path+'total.csv', encoding=encoding, sep=',', index=False)
个人业绩YTD.to_csv(export_path+'sales_figures.csv', encoding=encoding, index=False)
业绩排名表.to_csv(export_path+'sales_ranking.csv',encoding=encoding,index=False)
sales_by_team.to_csv(export_path+'sales_by_team.csv',encoding=encoding,index=False)