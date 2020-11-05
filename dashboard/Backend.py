from joblib import dump
import pandas as pd
from sklearn.tree import DecisionTreeRegressor

# data inlezen en omzetten naar bruikbare vorm
df = pd.read_csv('../Testing2/sap_storing_data_hu_project.csv', low_memory=False)
df2 = df[['stm_oorz_groep', 'stm_oorz_code', 'stm_prioriteit', 'stm_contractgeb_mld', 'stm_contractgeb_gst',
          'stm_sap_meldtijd', 'stm_aanntpl_dd', 'stm_aanntpl_tijd', 'stm_fh_ddt']].copy()
df2['reparatietijd'] = (pd.to_datetime(df2['stm_fh_ddt']) -
                        pd.to_datetime(df2['stm_aanntpl_dd'] + " " +
                                       df2['stm_aanntpl_tijd'])).dt.total_seconds().div(60)
df2 = df2[['stm_oorz_groep', 'stm_oorz_code', 'stm_prioriteit', 'stm_contractgeb_gst', 'stm_sap_meldtijd',
           'reparatietijd']].copy()

# Alle Nan waardes, waardes die niet voorkomen in de csv bestanden en duplicaten verwijderen
df2 = df2.dropna()
df2 = df2[(df2['stm_contractgeb_gst'].isin([17, 50, 53, 54, 55, 56, 57, 62, 64, 82, 83])) == False]
df2 = df2[(df2['stm_oorz_code'].isin([33, 48, 51, 999])) == False]
df2 = df2[df2.duplicated(keep='last') == False]

# Oorzaak groepen encoden naar numeric waardes mbv get_dummies
df2 = pd.get_dummies(df2, columns=['stm_oorz_groep'])
df2 = pd.get_dummies(df2, columns=['stm_oorz_code'])
df2 = pd.get_dummies(df2, columns=['stm_contractgeb_gst'])

# alle ongeldige meldtijden verwijderen en omzetten naar hele uren
df2 = df2[df2['stm_sap_meldtijd'] != "::"]
df2['stm_sap_meldtijd_uren'] = round(pd.to_timedelta(df2['stm_sap_meldtijd']).dt.total_seconds().div(3600)).astype(int)
df2 = df2.drop('stm_sap_meldtijd', axis=1)
df2['stm_sap_meldtijd_uren'] = df2['stm_sap_meldtijd_uren'].replace(24, 0)
df2 = pd.get_dummies(df2, columns=['stm_sap_meldtijd_uren'])

# Data selectie is een range is van 15 en 480.
df2 = df2[(df2['reparatietijd'] >= 15) & (df2['reparatietijd'] <= 480)]

# data voor divregs voor marge
df1 = df2[df2['reparatietijd'] >= df2['reparatietijd'].quantile(.75)]
df3 = df2[df2['reparatietijd'] <= df2['reparatietijd'].quantile(.25)]

# define features en targets

features1 = df1.drop('reparatietijd', axis=1)
target1 = df1['reparatietijd']

features2 = df2.drop('reparatietijd', axis=1)
target2 = df2['reparatietijd']

features3 = df3.drop('reparatietijd', axis=1)
target3 = df3['reparatietijd']


# Maak model

divreg1 = DecisionTreeRegressor()
divreg2 = DecisionTreeRegressor()
divreg3 = DecisionTreeRegressor()

# fit model
divreg1.fit(features1, target1)
divreg2.fit(features2, target2)
divreg3.fit(features3, target3)

# zet database en division tree om in files
dump(divreg1, 'divreg1.joblib')
dump(divreg2, 'divreg2.joblib')
dump(divreg3, 'divreg3.joblib')

dummiedf = pd.DataFrame(data=None, columns=features2.columns)
dummiedf.to_pickle('dummiedf.pkl')
