






def create_response_format(msg='',data={},status=400,is_valid=False,headers={},redirect="",token="", success= False,permission_status=None,exception=False,return_context=False,**kwargs):
    context = {}
             
    context['is_valid'] = is_valid 
    if data:
        context['data'] = data     
    if headers:
        context['headers'] = headers                
    if exception and not msg:
        context['message'] = "Something went wrong. Please try again later."        
    if exception and msg:
        context['message'] = msg
    if msg and not exception:
        context['message'] = msg
    if permission_status:
        context['permission_status'] = permission_status
    if success:
        context['success'] = success
    if redirect:
        context['redirect'] = redirect
    if token:
        context['token'] = token

    return context
