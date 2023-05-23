from diagnostic.models import Recomendation
import yaml
import json
import os

class DiagnosticHelpers():
    @DeprecationWarning # use read_recomendations
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

    def read_recomendations(diagnostic_type: str, file_name:str = '')->list:
        if not file_name:
            if diagnostic_type == 'standard':
                file_name = 'files/DPO_text.yaml'
            elif diagnostic_type == 'dppsh':
                file_name = 'files/DPO_text_dppsh.yaml'
            else:
                return []

        recomendations_list = []
        if not os.path.exists(file_name):
            return []
        with open(file=file_name) as fh:
            read_data = yaml.load(fh, Loader=yaml.FullLoader)

        for index, str in enumerate(read_data):
            recomendation = Recomendation(index=index + 1, diagnostic_type=diagnostic_type, 
                level_1=str['f'], level_2=str['s'], level_3=str['t'])
            recomendations_list.append(recomendation)
        
        fh.close()

        return recomendations_list

    def read_quetions(diagnostic_type: str)->json:
        questions_path = 'files/questions.json'
        if not os.path.exists(questions_path):
            return {'status':500, 'message':'Internal server error'}

        with open(questions_path, 'r', encoding='utf-8') as f: #открыли файл с данными
            read_data = json.load(f)
        # with open(file=questions_path) as fh:
        # read_data = json.loads(questions_path)

        questions = read_data[diagnostic_type]
        
        f.close()
        return questions

    def generate_results(results_list: list)->hash:
        # настроить динамичное получение типов дигностики

        gen_results = {
            'standard':[],
            'dppsh':[],
            'competence':''
        }
        
        links_path = 'files/more_info_links_standard.json'
        if not os.path.exists(links_path):
            return {'status':500, 'message':'Internal server error'}

        with open(links_path, 'r', encoding='utf-8') as f: #открыли файл с данными
            links_data = json.load(f)
        f.close()
        
        more_info_links = links_data['links']

        if not results_list:
            return gen_results
        for res in results_list:
            if res.diagnostic_type not in gen_results:
                gen_results[res.diagnostic_type] = []
            
            tmp_hash = res.hash_recomendation()
            if res.diagnostic_type == 'standard':
                tmp_hash['link'] = more_info_links[res.index - 1]
            else:
                tmp_hash['link'] = ""

            gen_results[res.diagnostic_type].append(tmp_hash)
                

        gen_results['competence'] = results_list[0].competence_lvl
        return gen_results
