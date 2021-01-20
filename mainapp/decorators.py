from django.shortcuts import render
from django.shortcuts import redirect


def authenticated(viewFunc):
    def wrapperFunc(request, *args, **kwargs):
        if request.user.is_authenticated:
            return viewFunc(request, *args, **kwargs)
        else:
            return redirect('loginpage')
            
    return wrapperFunc
    
    
def unauthenticated(viewFunc):
    def wrapperFunc(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard')
        else:
            return viewFunc(request, *args, **kwargs)
            
    return wrapperFunc
    
    
# def allowedUsers(allowedRoles=[]):
#     def viewpage(viewFunc):
#         def wrapperFunc(request, *args, **kwargs):
#             group = None
#             if request.user.groups.exists():
#                 group = request.user.groups.all()[0].name

#             if group in allowedRoles:
#                 return viewFunc(request, *args, **kwargs)
#             else:
#                 return redirect('logoutpage')
            
#         return wrapperFunc
#     return viewpage