import pandas as pd
from raw_lab_data import VisualizeRaw


# Read data
df = pd.read_excel('excel_data/worm1.xlsx')
print(df.columns)

raw = VisualizeRaw(df, 'time')
raw.split_trials()

trial_data = raw.trial_data

print(trial_data)

raw.plot_trials('trial_plots/worm1', 'signal')

for i, df in enumerate(trial_data):
    df.to_excel(f'trial_data/worm1/trial{i}.xlsx', index=False)
