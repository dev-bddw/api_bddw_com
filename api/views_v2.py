import logging

from rest_framework import status
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from django.http import HttpResponse

from .models import DropDownMenu, LandingPageImage, MenuList, Product, ProductImage
from .serializers import DropDownMenuSerializer, LandingPageImageSerializer, MenuListSerializer, ProductSerializer, ProductImageSerializer
from .helpers import handle_special_cases

logger = logging.getLogger('watchtower')

@api_view(["GET", "PUT"])
@parser_classes([MultiPartParser, FormParser])
def products(request, product_name_slug):
    instance = None
    serializer_class = None

    # Log the request method and slug
    logger.info(f"Received {request.method} request for slug: {product_name_slug}")

    product_name_slug = handle_special_cases(product_name_slug)

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

    menu_list_slug = handle_special_cases(menu_list_slug)

    instance = MenuList.objects.get(name__iexact=menu_list_slug)
    serializer_class = MenuListSerializer
    logger.info(f"MenuList instance found for slug: {menu_list_slug}")

    if request.method == "GET":
        serializer = serializer_class(instance)
        body_response = {"body": serializer.data}
        logger.info(f"GET request successful for slug: {menu_list_slug}, returning data")
        return Response(body_response, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        records_data = []
        for key in request.data.keys():
            if key.startswith("records["):
                index, field = key.split("[")[1].split("].")
                index = int(index)  # Convert index to integer

                # Initialize a new dictionary or update existing
                while index >= len(records_data):
                    records_data.append({})
                records_data[index][field] = request.data[key]

        # Include the images data in the request data
        request_data = {
            "name": request.data.get("name"),
            "meta": request.data.get("meta"),
            "records": records_data,
        }

        # Handle POST request
        serializer = MenuListSerializer(data=request_data)
        if serializer.is_valid():
            serializer.save()
            logger.info(f"POST request successful for slug: {menu_list_slug}, MenuList created")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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

@api_view(["POST"])
@parser_classes([MultiPartParser, FormParser])
def product_images(request, product_image_id=None):

    serializer_class = ProductImageSerializer

    if request.method == 'POST':

        logger.info(f"Received POST request for ProductImage w/ body: {request.data}")
        request_data = request.data
        serializer = serializer_class(data=request_data)
        logger.info(f"POST body is valid{serializer.is_valid()}")
        if serializer.is_valid():
            serializer.save()
            logger.info(f"POST request successful for ProductImage, ProductImage created")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    return Response({"error": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


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
