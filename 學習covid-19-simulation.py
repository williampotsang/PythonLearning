
import numpy as np
import pandas as pd
import random
import math 
%matplotlib inline
import matplotlib as mpl
import matplotlib.pyplot as plt

from matplotlib.font_manager import FontProperties, fontManager

import warnings
def ignore_warn(*args, **kwargs):
    pass
warnings.warn = ignore_warn #ignore annoying warning 

# below 3 lines are only needed in CoLab
!wget -O TaipeiSansTCBeta-Regular.ttf https://drive.google.com/uc?id=1eGAsTN1HBpJAkeVM57_C7ccp7hbgSz3_&export=download
fontManager.addfont('TaipeiSansTCBeta-Regular.ttf')
mpl.rc('font', family='Taipei Sans TC Beta')

plt.rcParams['font.sans-serif']=['SimHei'] 
plt.rcParams['axes.unicode_minus']=False 
plt.rcParams.update({'font.size': 12})

# 架設條件
num_employees = 100             # 單位員工人數
num_family = 3                  # 平均同住家人人數
sat_ratio = 0.2                 # 最終染疫飽和率
qt_days_inflected = 14          # 染疫後須請假天數
qt_days_fam_inflected1 = 14     # 因家人染疫，需照顧家人無法到班，須請假天數
qt_days_fam_inflected2 = 4      # 家人染疫，不須照顧家人，但須被匡列隔離天數

df = pd.DataFrame(np.arange(1, 110),columns=['day'])
df['logistic'] = df.apply(lambda x: num_employees*sat_ratio/(1+math.exp(-0.1*(x.day-40))), axis=1)
df['inf_ttl'] = df.apply(lambda x: round(x.logistic), axis=1)
df['inf_ttl_last'] = df['inf_ttl'].shift(1)
df['inf_new'] = df.apply(lambda x: x.inf_ttl-x.inf_ttl_last, axis=1)
df['inf_new'].fillna(0, inplace=True)
df['off_inf'] = df['inf_new'].rolling(min_periods=1, window=qt_days_inflected).sum()
df['inf_prob'] = df['logistic'].rolling(window=2).apply(lambda x: x.iloc[1] - x.iloc[0])/num_employees
df['inf_acc'] = df['inf_new'].rolling(min_periods=1, window=1000).sum()

list_emp = []
for i in range(num_employees):
    list_inf_ttl_fam = []
    for i_day, item in df.iterrows():
        list_inf_ttl_fam.append(0)
        fam = []
        for fi in range(num_family):
            fam.append(0)
        for fi in range(num_family):
            if random.randint(1,10000) < item['inf_prob']*10000:
                fam[fi] = 1
        if sum(fam) > 0:
            list_inf_ttl_fam[i_day] = 1
    list_emp.append(list_inf_ttl_fam)

df_emp = pd.DataFrame(list_emp).transpose()
for i_emp in df_emp.columns:
    if random.randint(1,2) == 1:
        qt_days = qt_days_fam_inflected1
    else:
        qt_days = qt_days_fam_inflected2
    df_emp[i_emp] = df_emp[i_emp].rolling(min_periods=1, window=qt_days).max()
df_emp['inf_ttl_fam'] = df_emp.apply(lambda x: x[:].sum(), axis=1)
df['inf_ttl_fam'] = df_emp['inf_ttl_fam']
df['off_ttl'] = df.apply(lambda x: x.off_inf+x.inf_ttl_fam, axis=1)

fig, ax = plt.subplots(figsize=(16,6))
ax.stackplot(df['day'], df['off_inf'],df['inf_ttl_fam'], alpha=0.5, 
             labels=['缺勤 (同仁染疫)', '缺勤 (家人染疫)'])
ax.bar(df['day'], df['inf_new'], label='新染疫同仁')
ax.plot(df['day'], num_employees-df['off_ttl'], label='可到班人數')
ax.plot(df['day'], df['inf_acc'], label='累積染疫同仁')

min_duty = num_employees-df['off_ttl'].max()
for x in range(1000):
    if num_employees-df['off_ttl'][x] == min_duty:
        ax.annotate('第%d天, %.0f人可到班'%(x, min_duty),xy=(x,min_duty-5))
        break

ax.set_ylabel('Persons')
ax.set_xlabel('Day')
ax.set_title('Covid-19 Inflection and Off-Duty Prediction')
ax.annotate('Assumption: \n - 公司內無傳染情況\n - 染疫同仁請假天數%d天\n - 因家人染疫，同仁需請假%d或%d天(機率各半)\n - 最終染疫飽和比例 %.2f\n - 共住家人平均人數%d人\n'%(qt_days_inflected,qt_days_fam_inflected1,qt_days_fam_inflected2,sat_ratio,num_family),xy=(80,40))
ax.legend()
