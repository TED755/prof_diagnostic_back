from diagnostic.models import Recomendation
import yaml
import json
import os

class DiagnosticHelpers():
    def load_recomendations_to_db(file_name: str, diagnostic_type: str):
        if not os.path.exists(file_name):
            return {'status': 404, 'message':'File not found'}

        with open(file=file_name) as fh:
            read_data = yaml.load(fh, Loader=yaml.FullLoader)

        for index, str in enumerate(read_data):
            recomendation = Recomendation(index=index + 1, diagnostic_type=diagnostic_type, 
                level_1=str['f'], level_2=str['s'], level_3=str['t'])
            recomendation.save()

        fh.close()

    def read_quetions(diagnostic_type: str)->json:
        questions_path = 'files/questions.json'
        if not os.path.exists(questions_path):
            return {'status':500, 'message':'Internal server error'}

        with open(questions_path, 'r', encoding='utf-8') as f: #открыли файл с данными
            read_data = json.load(f)
        # with open(file=questions_path) as fh:
        # read_data = json.loads(questions_path)

        questions = read_data[diagnostic_type]
        # fh.close()
        return questions

    def generate_results(results_list: list)->hash:
        # настроить динамичное получение типов дигностики

        gen_results = {
            'standard':[],
            'dppsh':[],
            'competence':''
        }

        if not results_list:
            return gen_results
        for res in results_list:
            if res.diagnostic_type not in gen_results:
                gen_results[res.diagnostic_type] = []
            gen_results[res.diagnostic_type].append(res.hash_recomendation())
                

        gen_results['competence'] = results_list[0].competence_lvl
        return gen_results
