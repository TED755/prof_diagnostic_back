from diagnostic.models import Recomendation
import yaml
import os

class DiagnosticHelpers():
    def load_recomendations_to_db(file_name: str, diagnostic_type: str):
        # print(file_name)

        if not os.path.exists(file_name):
            print(404)
            return {'status': 404, 'message':'File not found'}

        with open(file=file_name) as fh:
            read_data = yaml.load(fh, Loader=yaml.FullLoader)

        for index, str in enumerate(read_data):
            recomendation = Recomendation(index=index + 1, diagnostic_type=diagnostic_type, 
                level_1=str['f'], level_2=str['s'], level_3=str['t'])
            recomendation.save()
            


