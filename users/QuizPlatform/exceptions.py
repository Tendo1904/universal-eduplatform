from rest_framework.views import exception_handler


def core_exception_handler(exc, context):
    """
    Handles core exceptions by delegating to specific exception handlers if available.
    
    Parameters:
    - exc: The exception instance raised.
    - context: The context in which the exception occurred.
    
    Returns:
    Response after handling the exception depending on the exception class.
    
    Args:
    - exc (Exception): The exception instance raised.
    - context (str): The context in which the exception occurred.
    
    Return:
    - Returns the response after handling the exception based on the exception class.
    """
    response = exception_handler(exc, context)
    handlers = {
        'ValidationError': _handle_generic_error
    }

    exception_class = exc.__class__.__name__

    if exception_class in handlers:
        return handlers[exception_class](exc, context, response)

    return response


def _handle_generic_error(exc, context, response):
    """
    Handles a generic error by updating the response data structure.
    
    Parameters:
        - exc: The exception object that triggered the error.
        - context: The context or environment of the error occurrence.
        - response: The response object containing data to be modified.
    
    Returns:
        The updated response object after restructuring the data.
    """
    response.data = {
        'errors': response.data
    }

    return response