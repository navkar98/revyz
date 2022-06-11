from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from kafka.kafka_queue_service import KafkaQueueService
from .models import Citizen, CitizenEducationDetails
from .serializers import CitizenDetailSerializer, CitizenSerializer, CitizenDetailSerializerSimple
from rest_framework import viewsets, status


class CitizenModelViewSet(viewsets.ModelViewSet):
	queryset = Citizen.objects.all()
	serializer_class = CitizenSerializer
	pagination_class = PageNumberPagination

	def create(self, request, *args, **kwargs):
		data = request.data.get('citizen', request.data)
		many = isinstance(data, list)
		print(data, many)
		serializer = self.get_serializer(data=data, many=many)
		serializer.is_valid(raise_exception=True)
		self.perform_create(serializer)
		headers = self.get_success_headers(serializer.data)
		return Response(
			serializer.data,
			status=status.HTTP_201_CREATED,
			headers=headers
		)

class CitizenDetailModelViewSet(viewsets.ModelViewSet):
	queryset = CitizenEducationDetails.objects.all()
	serializer_class = CitizenDetailSerializerSimple
	pagination_class = PageNumberPagination

	def create(self, request, *args, **kwargs):
		data = request.data.get('citizen_detail', request.data)
		many = isinstance(data, list)
		print(data, many)
		serializer = self.get_serializer(data=data, many=many)
		serializer.is_valid(raise_exception=True)
		self.perform_create(serializer)
		headers = self.get_success_headers(serializer.data)
		return Response(
			serializer.data,
			status=status.HTTP_201_CREATED,
			headers=headers
		)

	# Set custom route for fetching analyst docs
	@action(methods=['post'], detail=False)
	def create_pdf(self, request):
		data = request.data.get('citizen_id', request.data)

		topic_name = "PdfCreator"
		kqs_producer = KafkaQueueService(topic_name, 'producer')

		if kqs_producer.producer is None:
			raise Exception("Producer is not available")

		outgoing_data = {"citizen_id": int(data)}
		kqs_producer.outgoing_queue(outgoing_data, True)
