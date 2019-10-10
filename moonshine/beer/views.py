from django.shortcuts import render

from rest_framework import status, views
from rest_framework.response import Response

from beer.models import BeerModel
from beer.serializers import BeerModelSerializer


class BeerView(views.APIView):

    serializer_class = BeerModelSerializer

    def get(self, request, pk=None):
        """
            Method:             GET
            Url:                /api/beer/pk/
            Request headers:
                                {
                                    "Content-Type": "application/json",
                                    "Accept": "application/json",
                                }
            Request body:       None
            Response:
                                {
                                    beer.object.dict
                                }
        """
        try:
            beer = BeerModel.objects.get(id=pk) # pylint: disable=no-member
            beer_serializer = self.serializer_class(beer)

            return Response(
                beer_serializer.data,
                status=status.HTTP_200_OK)

        except Exception as ex:

            return Response(
                {'message': str(ex)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

    def post(self, request, *args, **kwargs):
        """
            Method:             Post
            Url:                /api/beer/
            Request headers:
                                {
                                    "Content-Type": "application/json",
                                    "Accept": "application/json",
                                }
            Request body:       {
                                    name: "",
                                    beertype: "",
                                    description: "",
                                }
            Response:
                                {
                                    beer.object.dict
                                }
        """
        try:
            beer_serializer = self.serializer_class(data=request.data)
            if beer_serializer.is_valid():
                beer_serializer.save()
                return Response(
                    beer_serializer.data,
                    status=status.HTTP_201_CREATED)

            return Response(
                    beer_serializer.data,
                    status=status.HTTP_400_BAD_REQUEST)           

        except Exception as ex:

            return Response(
                {'message': str(ex)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
