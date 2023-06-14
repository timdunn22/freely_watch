# import pandas as pd
#
# df=pd.read_csv('test_csv.txt',sep=';')
#
# #print(df)
#
# row_iter = df.iterrows()
#
# objs = [
#
#     myClass_in_model(
#
#         field_1 = row['Name'],
#
#         field_2  = row['Description'],
#
#         field_3  = row['Notes'],
#
#         field_4  = row['Votes']
#
#     )
#
#     for index, row in row_iter
#
# ]
#
# myClass_in_model.objects.bulk_create(objs)
