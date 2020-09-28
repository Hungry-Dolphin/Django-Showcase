from uuid import UUID


def check_clearance(request, obj):
    try:
        if int(request.user.profile.clearance) >= obj.clearance:
            return True
        else:
            return False
    except obj.DoesNotExist:
        return False


def check_uuid(string):
    try:
        temp = UUID(string)
        return True
    except ValueError:
        return False


def get_default_arguments(request):
    return {'user': request.user}
