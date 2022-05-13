
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

@api_view(['POST'])
def newInjury(request):
    data = request.data
    content = {'under development'}
    return Response(content, status=status.HTTP_501_NOT_IMPLEMENTED)

@api_view(['GET'])
def injurys(request,pk):
    return Response(status=status.HTTP_501_NOT_IMPLEMENTED)

@api_view(['GET'])
def injuryByTimeID(request,pk):
    return Response(status=status.HTTP_501_NOT_IMPLEMENTED)

@api_view(["POST"])
def newConcussion(request):
    return Response(status=status.HTTP_501_NOT_IMPLEMENTED)
