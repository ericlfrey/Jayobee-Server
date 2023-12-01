from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from datetime import date
from jayobeeapi.models import Job, Seeker


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

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized Job instance
        """
        uid = request.META['HTTP_AUTHORIZATION']
        user = Seeker.objects.get(uid=uid)
        job = Job.objects.create(
            user=user,
            company=request.data["company"],
            title=request.data["title"],
            status=request.data["status"],
            description=request.data["description"],
            date_created=date.today()
        )

        serializer = JobSerializer(job, context={'request': request})

        return Response(serializer.data)

    def destroy(self, request, pk):
        """Handle DELETE requests for a single job

        Returns:
            Response -- 200, 404, or 500 status code
        """
        uid = request.META['HTTP_AUTHORIZATION']
        try:
            job = Job.objects.get(pk=pk, user__uid=uid)
            job.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Job.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class JobSerializer(serializers.ModelSerializer):
    """JSON serializer for jobs

    Arguments:
        serializer type
    """
    class Meta:
        model = Job
        fields = (
            'id',
            'user',
            'company',
            'title',
            'status',
            'description',
            'date_created'
        )
