from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from jayobeeapi.models import Job


class JobView(ViewSet):
    """Job ViewSet"""

    def retrieve(self, request, pk=None):
        """Handle GET requests for single job

        Returns:
            Response -- JSON serialized job instance
        """
        # only get jobs for the current user
        uid = request.META['HTTP_AUTHORIZATION']
        try:
            job = Job.objects.get(pk=pk, user__uid=uid)
            serializer = JobSerializer(
                job, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to jobs resource

        Returns:
            Response -- JSON serialized list of jobs
        """
        uid = request.META['HTTP_AUTHORIZATION']
        # only get jobs for the current user
        jobs = Job.objects.filter(user__uid=uid)

        serializer = JobSerializer(
            jobs, many=True, context={'request': request})
        return Response(serializer.data)


class JobSerializer(serializers.ModelSerializer):
    """JSON serializer for jobs

    Arguments:
        serializer type
    """
    class Meta:
        model = Job
        fields = (
            'user',
            'company',
            'title',
            'status',
            'description',
            'date_created'
        )
