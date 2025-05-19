import pandas as pd
import numpy as np
from scipy import stats

# Чтение данных из CSV файла
# Создание DataFrame df из файла MouseEmpathy.csv

df = pd.read_csv('MouseEmpathy.csv')

# Группы из данных DataFrame
isolated = df[df['treatment'] == 'isolated']['percent.stretching'].values
companion_not_injected = df[df['treatment'] == 'ow']['percent.stretching'].values
companion_injected = df[df['treatment'] == 'bw']['percent.stretching'].values

# Объединение данных в один массив
data = np.concatenate([isolated, companion_not_injected, companion_injected])
groups = np.concatenate([['isolated']*len(isolated),['companion_not_injected']*len(companion_not_injected), ['companion_injected']*len(companion_injected)])

# Выполняем ANOVA
f_statistic, p_value = stats.f_oneway(isolated, companion_not_injected, companion_injected)

print(f"F-статистика: {f_statistic:.2f}")
print(f"P-значение: {p_value:.3f}")

alpha = 0.05
if p_value < alpha:
    print("Отвергаем нулевую гипотезу: существует статистически значимая разница между группами.")
else:
    print("Не отвергаем нулевую гипотезу: нет статистически значимой разницы между группами.")

