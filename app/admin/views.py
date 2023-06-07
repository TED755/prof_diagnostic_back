from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from admin.admin_model.migrate_data import MigrateData
import json


@csrf_exempt
def migrate_hist(request):
    # check auth
    migration = MigrateData()
    # migration.read_and_backup(list_num=0, drop_dubl=True)
    # migration.read_and_backup(list_num=1, drop_dubl=True)
    migration.save_to_db('standard')

    return HttpResponse(json.dumps({}), content_type="application/json", charset='utf-8', status=200)