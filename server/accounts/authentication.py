def is_authenticated(request):
    return request.session.get('email')

def get_type(request):
    return request.session.get('type')
