from rest_framework.decorators import api_view
from rest_framework.response import Response
from jayobeeapi.models import Seeker


@api_view(['POST'])
def check_user(request):
    '''Checks to see if User has Associated Seeker

    Method arguments: request -- The full HTTP request object
    '''
    uid = request.META['HTTP_AUTHORIZATION']
    # uid = request.data['uid']

    # Use the built-in authenticate method to verify
    # authenticate returns the user object or None if no user is found
    # pylint: disable=E1101
    seeker = Seeker.objects.filter(uid=uid).first()

    # If authentication was successful, respond with their token
    if seeker is not None:
        data = {
            'id': seeker.id,
            'uid': seeker.uid,
            'username': seeker.username,
        }
        return Response(data)
    else:
        # Bad login details were provided. So we can't log the user in.
        data = {'valid': False}
        return Response(data)


@api_view(['POST'])
def register_user(request):
    '''Handles the creation of a new seeker for authentication

    Method arguments: request -- The full HTTP request object
    '''

    # Uses the built-in Django method to create a new user
    # pylint: disable=E1101
    seeker = Seeker.objects.create(
        uid=request.META['HTTP_AUTHORIZATION'],
        username=request.data['username'],
    )

    # Return the client info to the client
    data = {
        'id': seeker.id,
        'uid': seeker.uid,
        'username': seeker.username,
    }
    return Response(data)
