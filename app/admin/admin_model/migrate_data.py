import pandas as pd
import gspread
from datetime import datetime
from user.user_model.user_helpers import UserHelpers
from user.models import Recomendation as user_rec, User
from diagnostic.models import Diagnostic
import string
import random


class MigrateData():
    def __init__(self):
        self.__FILE_URL_DIAGNOSTIC__ = 'https://docs.google.com/spreadsheets/d/1E7xXd18F1oH8rSod0J7UB-n4Vzdup1S1QEoGHAXY8c0/edit#gid=0'
        self.__KEY_FILE__ = 'admin/admin_model/client_secret.json'

    def read_and_backup(self, list_num: int = 0, sheet_url: str = '', key_file: str = '', drop_dubl: bool = True):
        if not sheet_url:
            sheet_url = self.__FILE_URL_DIAGNOSTIC__
        if not key_file:
            key_file = self.__KEY_FILE__

        service_account = gspread.service_account(filename=key_file)
        sheet = service_account.open_by_url(sheet_url)
        worksheet = sheet.get_worksheet(list_num)
        cells = worksheet.get_values()

        frame = pd.DataFrame(cells, columns=['fio',1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,
            31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,'email','position','teaching_exp','category',
            'raion','region_rf','school','locality_type'])
        # frame = pd.DataFrame(cells)
        # print(frame.head())
        # print(frame.axes[0].size)
        if drop_dubl:
            frame = frame.drop_duplicates(subset=['fio', 'position', 'teaching_exp', 'category'], keep='last')
        
        frame.to_csv(f"admin/admin_model/backup_data/{datetime.utcnow()}_getting_data{list_num}.csv", index=False)
    
    def save_to_db(self, diagnostic_type: str):
        data = pd.read_csv('admin/admin_model/backup_data/2023-06-07 09:20:44.636583_getting_data0.csv')
        print(data.axes[0].size)
        data = data.fillna('nan')
        # i = 0
        for row in data.itertuples():
            answers = []

            for answer in range(2, 47):
                if row[answer] != 0:
                    answers.append(1)
                else:
                    answers.append(0)
            
            if row[47] == 'nan':
                email = 'historical'

            rand_string = string.ascii_letters + string.digits
            password = ''.join(random.sample(rand_string, 12))

            new_user = User(
                name = row[1],
                email = email,
                password = UserHelpers.crypt_password(password),
                category = row[50] if row[50] != 'nan' else '',
                teaching_exp = row[49] if row[49] != 'nan' else '',
                position = row[48] if row[48] != 'nan' else '',
                raion = row[51] if row[51] != 'nan' else '',
                region_rf = row[53] if row[53] != 'nan' else '',
                school = row[52] if row[52] != 'nan' else '',
                locality_type = row[54] if row[54] != 'nan' else ''
            )
            # new_user.save()

            new_user = User.objects.last()
            user_diagnostic = Diagnostic(user_id = new_user.id, 
                                         diagnostic_type = diagnostic_type, 
                                         started = datetime.utcnow(),
                                         ended = datetime.utcnow()
            )

            user_diagnostic.answers = answers
            # user_diagnostic.save()
            # print(new_user.user_info())
            # print(user_diagnostic.diagnostic_info())
            # added counting recomendations
            # if i == 10:
            #     return
            # i += 1
