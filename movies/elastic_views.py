# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# import requests

# @api_view(['POST'])
# def movies(request):
#     if request.method == 'POST':
#         return Response(requests.post('http://localhost:9200/_search/', data=request.data).text)