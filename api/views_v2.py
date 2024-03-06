from rest_framework import status
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from django.http import HttpResponse
import logging

from .models import DropDownMenu, LandingPageImage, MenuList, Product
from .serializers import DropDownMenuSerializer, LandingPageImageSerializer, MenuListSerializer, ProductSerializer

special_cases = {
    "sev-drulo-series": "sev-drulo series",
    "sev-drulo-sofa": "sev-drulo sofa",
    "sev-drulo-club-chair": "sev-drulo club chair",
    "sev-drulo-sectional-sofa": "sev-drulo sectional sofa",
    "wall-mount-luggage-rack": "Wall-mount Luggage Rack",
    "sev-drulo-ottoman": "sev-drulo ottoman",
    "robe-tile-coffe-table": "robe-tile coffee table",
}

logger = logging.getLogger('watchtower')

@api_view(["GET", "PUT"])
@parser_classes([MultiPartParser, FormParser])
def products(request, product_name_slug):
    instance = None
    serializer_class = None

    # Log the request method and slug
    logger.info(f"Received {request.method} request for slug: {product_name_slug}")

    if product_name_slug not in special_cases.keys():
        product_name_slug = product_name_slug.lower().replace("-", " ").replace("captains", "captain's").replace("admirals", "admiral's")
    else:
        product_name_slug = special_cases[product_name_slug]

    instance = Product.objects.get(name__iexact=product_name_slug)
    serializer_class = ProductSerializer
    logger.info(f"Product instance found for slug: {product_name_slug}")

    if request.method == "GET":
        serializer = serializer_class(instance)
        body_response = {"body": serializer.data}
        logger.info(f"GET request successful for slug: {product_name_slug}, returning data")
        return Response(body_response, status=status.HTTP_200_OK)

    elif request.method == "PUT":
        serializer = serializer_class(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info(f"PUT request successful for slug: {product_name_slug}, data updated")
            return Response(serializer.data)
        logger.warning(f"PUT request data invalid for slug: {product_name_slug}, returning errors")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    logger.warning(f"Method {request.method} not allowed for slug: {product_name_slug}")

    return Response({"error": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(["GET", "PUT"])
@parser_classes([MultiPartParser, FormParser])
def menu_lists(request, menu_list_slug):
    instance = None
    serializer_class = None

    # Log the request method and slug
    logger.info(f"Received {request.method} request for slug: {menu_list_slug}")

    if menu_list_slug not in special_cases.keys():
        menu_list_slug = menu_list_slug.lower().replace("-", " ").replace("captains", "captain's").replace("admirals", "admiral's")
    else:
        menu_list_slug = special_cases[menu_list_slug]

    instance = MenuList.objects.get(name__iexact=menu_list_slug)
    serializer_class = MenuListSerializer
    logger.info(f"MenuList instance found for slug: {menu_list_slug}")

    if request.method == "GET":
        serializer = serializer_class(instance)
        body_response = {"body": serializer.data}
        logger.info(f"GET request successful for slug: {menu_list_slug}, returning data")
        return Response(body_response, status=status.HTTP_200_OK)

    elif request.method == "PUT":
        serializer = serializer_class(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info(f"PUT request successful for slug: {menu_list_slug}, data updated")
            return Response(serializer.data)
        logger.warning(f"PUT request data invalid for slug: {menu_list_slug}, returning errors")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    logger.warning(f"Method {request.method} not allowed for slug: {menu_list_slug}")
    return Response({"error": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(["GET", "PUT"])
@parser_classes([MultiPartParser, FormParser])
def menu_list_items(request, menu_list_item_id):
    if request.method == 'GET':
        # Handle GET request
        pass
    elif request.method == 'POST':
        # Handle POST request
        pass
    else:
        return HttpResponse("HTTP method not supported", status=405)

@api_view(["GET", "PUT"])
@parser_classes([MultiPartParser, FormParser])
def product_images(request, product_image_id):
    if request.method == 'GET':
        # Handle GET request
        pass
    elif request.method == 'POST':
        # Handle POST request
        pass
    else:
        return HttpResponse("HTTP method not supported", status=405)


@api_view(["GET", "PUT"])
@parser_classes([MultiPartParser, FormParser])
def landing_page_images(request, landing_page_image_id):
    if request.method == 'GET':
        # Handle GET request
        pass
    elif request.method == 'POST':
        # Handle POST request
        pass
    else:
        return HttpResponse("HTTP method not supported", status=405)
