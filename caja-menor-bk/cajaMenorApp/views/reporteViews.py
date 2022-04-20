from django.conf                                      import settings
from django.db.models.query import EmptyQuerySet
from django.http                                      import request
from rest_framework                                   import generics, status
from rest_framework.response                          import Response
from rest_framework.permissions                       import IsAuthenticated
from rest_framework_simplejwt.backends                import TokenBackend
from cajaMenorApp.models.reporte                 import Reporte
from cajaMenorApp.serializers.reporteSerializer import ReporteSerializer
from cajaMenorApp.models.user import User
from cajaMenorApp.serializers.userSerializer import UserSerializer
from cajaMenorApp.models.cajaMenor                 import CajaMenor
from cajaMenorApp.serializers.cajaMenorSerializaer import CajaMenorSerializer

class ReporteCreateView(generics.CreateAPIView):
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
        serializer = ReporteSerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data

            # Update caja menor
            reporte_data = validated_data
            caja_id = reporte_data['caja_menor'].id
            valor = reporte_data['valor']
            tipoServicio = reporte_data['tipoServicio']
            tipoServicio = str(tipoServicio)
            caja_menor = CajaMenor.objects.get(id=caja_id)
            print(caja_id)
            if tipoServicio == 'GASTO':
                caja_menor.gastos = caja_menor.gastos + valor
                caja_menor.saldo = caja_menor.saldo - valor
                caja_menor.save()
            elif tipoServicio == 'INGRESO':
                caja_menor.saldo = caja_menor.saldo + valor
                caja_menor.save()

            

       
            archivo = validated_data['evidence']
            archivo.name = 'evidence.png'
            validated_data['evidence'] = archivo


            registro = Reporte(**validated_data)
            registro.save()
            serializer_response = ReporteSerializer(registro)  

            return Response(serializer_response.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReporteDetailView(generics.RetrieveAPIView):
    queryset           = Reporte.objects.all()
    serializer_class   = ReporteSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        token        = self.request.META.get('HTTP_AUTHORIZATION')[7:]
        tokenBackend = TokenBackend(algorithm=settings.SIMPLE_JWT['ALGORITHM'])
        valid_data   = tokenBackend.decode(token,verify=False)
        
        if valid_data['user_id'] != self.kwargs['user']:
            stringResponse = {'detail':'Unauthorized Request'}
            return Response(stringResponse, status=status.HTTP_401_UNAUTHORIZED)
        return super().get_object()


class ReporteListView(generics.ListAPIView):
    serializer_class   = ReporteSerializer
    permission_classes = (IsAuthenticated,)
    
    def get_queryset(self):
        token        = self.request.META.get('HTTP_AUTHORIZATION')[7:]
        tokenBackend = TokenBackend(algorithm=settings.SIMPLE_JWT['ALGORITHM'])
        valid_data   = tokenBackend.decode(token,verify=False)
        
        if valid_data['user_id'] != self.kwargs['user']:
            stringResponse = {'detail':'Unauthorized Request'}
            return Response(stringResponse, status=status.HTTP_401_UNAUTHORIZED)
        
        queryset = Reporte.objects.all()
        return queryset.order_by('fecha')
        

