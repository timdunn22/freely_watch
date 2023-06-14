import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'movies.settings'
from scripts.common_methods import merged_dicts, not_null_value, flatten, convert_xy_columns
import pandas as pd
import numpy as np


class ForeignModelDfFromKey:

    def __init__(self, df, model_class, key, foreign_models_dict) -> None:
        self.df = df
        self.model_class = model_class
        self.key = key
        self.foreign_df = None
        self.foreign_models_dict = foreign_models_dict
        self.key_value = self.foreign_models_dict.get(key)
        self.foreign_field = self.model_class._meta.get_field(key)
        self.foreign_model_object = self.foreign_field.related_model
        self.foreign_pk = self.foreign_model_object._meta.pk.attname
        self.foreign_column = self.foreign_field.attname

    def create_foreign_df(self):
        filter_args = self.get_filter_args()
        data = self.foreign_model_object.objects.filter(**filter_args).values()
        self.foreign_df = pd.DataFrame(data=data)

    def get_filter_args(self):
        return {f'{self.key_value}__in': self.df[self.key]}
    
    def merge_df_w_foreign_df(self):
        self.df = pd.merge(self.df, self.foreign_df, left_on=self.key, right_on=self.key_value, how='left')

    def add_foreign_columns_to_df(self):
        self.merge_df_w_foreign_df()
        self.df[self.foreign_column] = self.df[self.foreign_pk]
        cols_to_drop = [column for column in self.foreign_df.columns if column in self.df.columns]
        self.df.drop(cols_to_drop, axis=1, inplace=True)
    
    def get_foreign_merge_column(self):
        id_columns = [column for column in self.df.columns if column.startswith(f'{self.foreign_pk}_')]
        if len(id_columns) > 0:
            return id_columns[0]
        return self.foreign_pk

    def process_and_merge(self):
        self.create_foreign_df()
        if not self.foreign_df.empty:
            self.add_foreign_columns_to_df()
        return self.df
        
class ImportData:

    def __init__(self, df, model_class, identity, foreign_models) -> None:
        self.model_class = model_class
        self.df = df
        self.identity = identity
        self.foreign_models_dict = dict()
        if foreign_models:
            self.foreign_models_dict = merged_dicts(foreign_models)
        self.merged_df = None
        self.created_df = None
        self.updated_df = None
        self.create_objects = None
        self.update_objects = None
        self.pk_field = self.model_class._meta.pk.attname
        self.identity_fields = self.get_identity_fields()
        self.merge_fields = [field for field in self.identity_fields if field != self.pk_field]
        self.model_fields = [column for column in self.model_class._meta.local_fields if column != self.pk_field]

    def set_dfs(self):
        self.assign_foreign_models()
        self.drop_foreign_keys()
        self.set_db_df()
        self.set_merge_df()
        self.set_created_df()
        self.set_updated_df()

    def set_movie_object(self, df):
        if df is not None:
            if not df.empty:
                row_results = df.apply(lambda row: self.create_dict_from_row(row), axis=1)
                if list(row_results) not in [None, [None], []]:
                    return [result for result in list(row_results) if result]
    
    def get_initial_dict(self, row):
        initial_dict = {key: value for key, value in dict(row).items() if not_null_value(value)}
        return {key: self.value_converted(key, value) for key, value in initial_dict.items()}

    def create_dict_from_row(self, row):
        the_dict = self.get_initial_dict(row)
        if len(the_dict.keys()) > 0:
            return self.model_class(**the_dict)
    
    def create_dict_from_row(self, row):
        the_dict = self.get_initial_dict(row)
        if len(the_dict.keys()) > 0:
            return self.model_class(**the_dict)
    
    def get_update_fields(self):
        try:
            return [column for column in self.updated_df.columns if column not in self.identity_fields]
        except:
            return list()
    
    def process_df(self):
        self.set_dfs()
        self.set_movie_objects()
        self.create_records()
        self.update_records()

    def create_records(self):
        if self.create_objects:
            self.model_class.objects.bulk_create(self.create_objects, batch_size=100000)

    def update_records(self):
        update_fields = self.get_update_fields()
        if self.update_objects and len(update_fields) > 0:
            self.model_class.objects.bulk_update(self.update_objects, 
            batch_size=10000, fields=update_fields)
        
    def set_updated_df(self):
        if self.db_df.size > 0:
            self.updated_df = self.merged_df.loc[~self.pk_is_null() & self.merge_fields_not_null()]
            self.get_changed_records_df()

    def get_changed_records_df(self):
        concated_df = pd.concat([self.updated_df, self.db_df])
        self.normalize_concated_df(concated_df)
        if not self.updated_df.empty:
            self.updated_df = concated_df.loc[~concated_df.duplicated(subset=self.updated_df.columns, keep=False)]

    def field_type(self, field_type):
        return [column.attname for column in self.model_fields if field_type in str(column.__class__)]

    def integer_fields(self):
        return self.field_type('IntegerField')

    def float_fields(self):
        return self.field_type('FloatField')

    def boolean_fields(self):
        return self.field_type('BooleanField')

    def normalize_concated_df(self, concated_df):
        for column in concated_df.columns:
            if self.column_is_number_type(column):
                self.convert_number_col(column, concated_df)
            elif self.column_is_string_type(column):
                self.convert_string_type(column, concated_df)
            elif self.column_is_boolean_type(column, concated_df):
                self.convert_boolean_type(column, concated_df)

    def column_is_boolean_type(self, column, df):
        return column in self.boolean_fields()

    def convert_number_col(self, column, df):
        self.convert_col(column, df, 0)

    def convert_boolean_type(self, column, df):
        self.convert_col(column, df, False)

    def convert_string_type(self, column, df):
        self.convert_col(column, df, 'unknown')

    def convert_col(self, column, df, default_value):
        column_type = self.get_column_type(column, df)
        df[column].fillna(default_value, inplace=True)
        self.set_default_to_problem_data(column, df, default_value, column_type)
        df[column] = df[column].astype(column_type)

    def set_default_to_problem_data(self, column, df, default_value, column_type):
        column_values = np.unique(df[column].astype(str))
        problem_values = list(filter(lambda value: self.try_value_conversion(value, column_type), column_values))
        df.loc[df[column].astype(str).isin(problem_values)] = default_value

    def try_value_conversion(self, value, column_type):
        try:
            column_type(value)
            return False
        except:
            return True

    def get_column_type(self, column, df):
        if column in self.integer_fields() or column in self.field_type('AutoField'):
            return int
        elif column in self.float_fields():
            return float
        elif column in self.boolean_fields():
            return bool
        else:
            return str

    def column_is_number_type(self, column):
        return column in self.float_fields() or column in self.integer_fields()

    def column_is_string_type(self, column):
        string_fields = [self.field_type('CharField'), self.field_type('TextField'), 
                         self.field_type('URLField')]
        return column in flatten(string_fields)

    def set_created_df(self):
        if not self.db_df.empty:
            self.created_df = self.merged_df.loc[self.merge_fields_not_null()]
        else:
            convert_xy_columns(self.df)
            self.created_df = self.df.loc[self.df[self.merge_fields].notnull().values.all(1)]
        important_fields = [field for field in self.identity_fields if field != self.pk_field]
        self.created_df = self.created_df.loc[~self.created_df.duplicated(subset=important_fields)]
        if self.db_df.size > 0 and self.created_df.size > 0:
            self.created_df = self.created_df.loc[self.pk_is_null()]

    def merge_fields_not_null(self):
        return self.merged_df[self.merge_fields].notnull().values.all(1)

    def set_merge_df(self):
        if self.db_df.size > 0:
            self.merged_df = pd.merge(self.df, self.db_df.loc[:, self.identity_fields], on=self.merge_fields, how='left')
            convert_xy_columns(self.merged_df)

    def pk_is_null(self):
        return self.merged_df[self.pk_field].isnull()

    def drop_foreign_keys(self):
        self.df.drop(list(self.foreign_models_dict.keys()), axis=1, inplace=True)

    def get_identity_fields(self):
        main_identity_fields = [field for field in self.identity if field not in self.foreign_models_dict.keys()]
        foreign_fields = [self.model_class._meta.get_field(field).attname for field
                          in self.foreign_models_dict.keys() if field in self.identity]
        return flatten([[self.pk_field], foreign_fields, main_identity_fields])
    
    def set_db_df(self):
        filter_args = self.get_filter_args()
        identity_objects = self.model_class.objects.filter(**filter_args).values()
        self.db_df = pd.DataFrame(data=identity_objects)

    def get_filter_args(self):
        return merged_dicts([self.args_from_field(field) for field in self.merge_fields])

    def args_from_field(self, field):
        values = self.df.loc[self.df[field].notnull(), field]
        return {f'{field}__in': values}

    def set_movie_objects(self):
        self.create_objects = self.set_movie_object(self.created_df)
        self.update_objects = self.set_movie_object(self.updated_df)
    
    def value_converted(self, key, value):
        if key in self.boolean_fields() and value not in [None, 0, 1, True, False]:
            return False
        elif key in self.integer_fields() and f'_{self.pk_field}' not in key:
            try:
                int(value)
            except:
                return 0
        return value
    
    def assign_foreign_models(self):
        for key in self.foreign_models_dict.keys():
            self.df = self.process_and_merge_key(key)

    def process_and_merge_key(self, key):
        return ForeignModelDfFromKey(self.df, model_class=self.model_class, key=key, foreign_models_dict=self.foreign_models_dict).process_and_merge()


class DataToDb:

    def __init__(self, model_class, file_path, identity=None, foreign_models=None):
        self.model_class = model_class
        self.file_path = file_path
        self.foreign_models = foreign_models
        self.identity = identity
        self.current_import_object = None

    def process_in_chunks(self):
        with pd.read_csv(self.file_path, chunksize=100000) as reader:
            for df in reader:
                self.import_chunk(df)
                
    def import_chunk(self, df):
        self.current_import_object = ImportData(df=df, model_class=self.model_class, identity=self.identity, 
                   foreign_models=self.foreign_models)
        self.current_import_object.process_df()
