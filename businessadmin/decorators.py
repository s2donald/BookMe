from .models import ExceptionLog
from django.utils import timezone
from django.http import HttpResponse
 
 
def log_exceptions(view_name):
    """
    Logs all the exceptions occuring in a Django view, to the
    ExceptionLog model.
    'view_name' denotes an identifier for the view that is
    being debug-logged.
    """
 
    def real_decorator(actual_view):
        """
        This is the actual decorator.
        """
 
        def wrapped_view(request):
            """
            This is the version of the view that will monitor
            itself for any un-expected Exception, and maintain basic
            logs of the same.
            """
            try:
                #Run the view code
                response = actual_view(request)
                #If a response is generated without any Exception
                #coming up, return it
                return response
            except Exception as e:
                #If an unexpected Exception occurs, make a debug entry
                #and save it
                debug_entry = ExceptionLog(
                    timestamp=timezone.now(),
                    view=view_name,
                    exceptionclass=str(e.__class__),
                    message=str(e))
                debug_entry.save()
                #Return the Server Error(500) status code
                return HttpResponse(status=500)
 
        return wrapped_view
 
    return real_decorator