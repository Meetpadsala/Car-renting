from django.http import Http404
from .models import login_table

def user_context(request):
    context = {}
    try:
        uid = request.session.get('log_id')
        if uid:
            userdata = login_table.objects.get(id=uid)
            Owner = (userdata.usertype == "Lessor")
            context = {
                'userdata': userdata,
                'Owner': Owner,
            }
    except:
        pass
    return context

