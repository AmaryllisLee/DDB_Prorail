from joblib import dump
import pandas as pd
from sklearn.linear_model import LinearRegression

df = pd.read_csv('sap_storing_data_hu_project.csv', low_memory=False)
df2 = df[['stm_oorz_groep', 'stm_oorz_code', 'stm_prioriteit', 'stm_fh_duur']].copy()

# Alle Nan waardes verwijderen
df2 = df2.dropna()
df2 = df2[(df2['stm_oorz_code'].isin([33, 48, 51, 999])) == False]

# Oorzaak groepen encoden naar numeric waardes mbv get_dummies . Explain one hote eencoding/get_Dummies
df2 = pd.get_dummies(df2, columns=["stm_oorz_groep"])

# Data selectie is een range is van 15 en 480.
df2 = df2[(df2['stm_fh_duur'] >= 15) & (df2['stm_fh_duur'] <= 480)]

# data voor linregs voor marge
df1 = df2[df2['stm_fh_duur'] >= df2['stm_fh_duur'].quantile(.75)]
df3 = df2[df2['stm_fh_duur'] <= df2['stm_fh_duur'].quantile(.25)]

# define values

features1 = df1[['stm_oorz_code', 'stm_prioriteit',
                'stm_oorz_groep_ONR-DERD', 'stm_oorz_groep_ONR-RIB',
                'stm_oorz_groep_TECHONV', 'stm_oorz_groep_WEER']]
target1 = df1['stm_fh_duur']

features2 = df2[['stm_oorz_code', 'stm_prioriteit',
                'stm_oorz_groep_ONR-DERD', 'stm_oorz_groep_ONR-RIB',
                'stm_oorz_groep_TECHONV', 'stm_oorz_groep_WEER']]
target2 = df2['stm_fh_duur']

features3 = df3[['stm_oorz_code', 'stm_prioriteit',
                'stm_oorz_groep_ONR-DERD', 'stm_oorz_groep_ONR-RIB',
                'stm_oorz_groep_TECHONV', 'stm_oorz_groep_WEER']]
target3 = df3['stm_fh_duur']


# Maak model

linreg1 = LinearRegression()
linreg2 = LinearRegression()
linreg3 = LinearRegression()

# fit model
linreg1.fit(features1, target1)
linreg2.fit(features2, target2)
linreg3.fit(features3, target3)

dump(linreg1, 'linreg1.joblib')
dump(linreg2, 'linreg2.joblib')
dump(linreg3, 'linreg3.joblib')
