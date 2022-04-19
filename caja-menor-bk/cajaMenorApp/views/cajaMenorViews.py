from django.conf                                      import settings
from django.db.models.query import EmptyQuerySet
from django.http                                      import request
from rest_framework                                   import generics, status
from rest_framework.response                          import Response
from rest_framework.permissions                       import IsAuthenticated
from rest_framework_simplejwt.backends                import TokenBackend
from cajaMenorApp.models.cajaMenor                    import CajaMenor
from cajaMenorApp.models.user                         import User
from cajaMenorApp.serializers.cajaMenorSerializaer    import CajaMenorSerializer
from cajaMenorApp.serializers.userSerializer          import UserSerializer

class CajaMenorCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        token = request.META.get('HTTP_AUTHORIZATION')[7:]
        tokenBackend = TokenBackend(algorithm=settings.SIMPLE_JWT['ALGORITHM'])
        valid_data = tokenBackend.decode(token,verify=False)
        if valid_data['user_id'] != kwargs['user']:
            stringResponse = {'detail':'Unauthorized Request'}
            return Response(stringResponse, status=status.HTTP_401_UNAUTHORIZED)
        serializer = CajaMenorSerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data

            cajaMenor = CajaMenor(**validated_data)
            cajaMenor.save()
            serializer_response = CajaMenorSerializer(cajaMenor)  

            return Response(serializer_response.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CajaMenorDetailView(generics.RetrieveAPIView):
    queryset           = CajaMenor.objects.all()
    serializer_class   = CajaMenorSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        token        = self.request.META.get('HTTP_AUTHORIZATION')[7:]
        tokenBackend = TokenBackend(algorithm=settings.SIMPLE_JWT['ALGORITHM'])
        valid_data   = tokenBackend.decode(token,verify=False)
        
        if valid_data['user_id'] != self.kwargs['user']:
            stringResponse = {'detail':'Unauthorized Request'}
            return Response(stringResponse, status=status.HTTP_401_UNAUTHORIZED)
        return super().get_object()


class CajaMenorListView(generics.ListAPIView):
    serializer_class   = CajaMenorSerializer
    permission_classes = (IsAuthenticated,)
    
    def get_queryset(self):
        token        = self.request.META.get('HTTP_AUTHORIZATION')[7:]
        tokenBackend = TokenBackend(algorithm=settings.SIMPLE_JWT['ALGORITHM'])
        valid_data   = tokenBackend.decode(token,verify=False)
        
        if valid_data['user_id'] != self.kwargs['user']:
            stringResponse = {'detail':'Unauthorized Request'}
            return Response(stringResponse, status=status.HTTP_401_UNAUTHORIZED)
        
        queryset = CajaMenor.objects.all()
        return queryset


class CajaMenorUpdateView(generics.UpdateAPIView):
    queryset           = CajaMenor.objects.all()
    serializer_class   = CajaMenorSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        token        = self.request.META.get('HTTP_AUTHORIZATION')[7:]
        tokenBackend = TokenBackend(algorithm=settings.SIMPLE_JWT['ALGORITHM'])
        valid_data   = tokenBackend.decode(token,verify=False)
        
        if valid_data['user_id'] != self.kwargs['user']:
            stringResponse = {'detail':'Unauthorized Request'}
            return Response(stringResponse, status=status.HTTP_401_UNAUTHORIZED)
        return super().get_object()

    def put(self, request, *args, **kwargs):
        token        = self.request.META.get('HTTP_AUTHORIZATION')[7:]
        tokenBackend = TokenBackend(algorithm=settings.SIMPLE_JWT['ALGORITHM'])
        valid_data   = tokenBackend.decode(token,verify=False)
        
        if valid_data['user_id'] != self.kwargs['user']:
            stringResponse = {'detail':'Unauthorized Request'}
            return Response(stringResponse, status=status.HTTP_401_UNAUTHORIZED)
        return super().put(request, *args, **kwargs)


class CajaMenorDeleteView(generics.DestroyAPIView):
    queryset           = CajaMenor.objects.all()
    serializer_class   = CajaMenorSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        token        = self.request.META.get('HTTP_AUTHORIZATION')[7:]
        tokenBackend = TokenBackend(algorithm=settings.SIMPLE_JWT['ALGORITHM'])
        valid_data   = tokenBackend.decode(token,verify=False)
        
        if valid_data['user_id'] != self.kwargs['user']:
            stringResponse = {'detail':'Unauthorized Request'}
            return Response(stringResponse, status=status.HTTP_401_UNAUTHORIZED)
        return super().get_object()

    def delete(self, request, *args, **kwargs):
        token        = self.request.META.get('HTTP_AUTHORIZATION')[7:]
        tokenBackend = TokenBackend(algorithm=settings.SIMPLE_JWT['ALGORITHM'])
        valid_data   = tokenBackend.decode(token,verify=False)
        
        if valid_data['user_id'] != self.kwargs['user']:
            stringResponse = {'detail':'Unauthorized Request'}
            return Response(stringResponse, status=status.HTTP_401_UNAUTHORIZED)
        return super().delete(request, *args, **kwargs)