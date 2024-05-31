 
def assigned_color(request):

    assigned_color = None
    if request.user.is_authenticated:
        assigned_color = request.user.userprofile.assigned_color
    return {'assigned_color': assigned_color}