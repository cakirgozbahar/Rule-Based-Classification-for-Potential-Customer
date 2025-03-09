
import pandas as pd


pd.set_option('display.max_columns',None)
pd.set_option('display.width',500)
df = pd.read_csv('persona.csv')

# print(df.shape)
# print(df.head(10))
# print(df['SOURCE'].nunique())
# print(df['SOURCE'].value_counts())
# print(df['PRICE'].nunique())
# print(df['PRICE'].value_counts())
# print(df['COUNTRY'].nunique())
# print(df['COUNTRY'].value_counts())
# print(df.groupby('COUNTRY').agg({"PRICE":"sum"}))
# print(df.groupby('COUNTRY').agg({"PRICE":"mean"}))
# print(df.groupby('SOURCE').agg({"PRICE":"mean"}))
# print(df.groupby(['COUNTRY','SOURCE']).agg({"PRICE":"mean"}))

agg_df = df.groupby(['COUNTRY','SOURCE','SEX','AGE']).agg({"PRICE":"mean"}).sort_values("PRICE",ascending=False)
agg_df.reset_index(inplace=True)
# print(agg_df['AGE'].describe())
# print(agg_df)

bins=[0,18,23,30,40,agg_df['AGE'].max()]
labels = ["0_18","19_23","24_30","31_40","41_" + str(agg_df['AGE'].max())]

agg_df['AGE_CAT']=pd.cut(agg_df['AGE'],bins,labels=labels)

# customers_level_based
agg_df["customers_level_based"] = agg_df[['COUNTRY','SOURCE','SEX','AGE_CAT']].agg(lambda x : '_'.join(x).upper(),axis=1)
#print(agg_df.groupby("customers_level_based").agg({"PRICE":"mean"}))
agg_df["SEGMENT"] = pd.qcut(agg_df["PRICE"],4,["D","C","B","A"])
agg_df.groupby("SEGMENT").agg({"PRICE":{"mean","min","max","sum"}})
# print(agg_df.sort_values("PRICE"))

# agg_df = agg_df[["customers_level_based","PRICE","SEGMENT"]]
agg_df=agg_df.groupby("customers_level_based").agg({"PRICE":"mean","SEGMENT": lambda x: x.iloc[0]})
agg_df=agg_df.reset_index()
print(agg_df.info())
new_user ="FRA_IOS_FEMALE_31_40"
print(agg_df[agg_df["customers_level_based"]==new_user])