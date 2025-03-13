from authentication.models import UserAccount

def customer_context(request):
    user = None  

    if 'customer_id' in request.session:
        try:
            user = UserAccount.objects.get(id=request.session['customer_id'])
        except UserAccount.DoesNotExist: 
            request.session.flush()  # Clear session if user doesn't exist

    return {'user': user}  # Make `user` available in all templates

def account_type(request):
    return {"account_type": request.session.get("account_type", "user")}




