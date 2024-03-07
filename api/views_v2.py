import logging

from rest_framework import status
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from django.http import HttpResponse

from .models import MenuList, Product, ProductImage
from .serializers import MenuListSerializer, ProductSerializer, ProductImageSerializer
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

@api_view(["POST", "DELETE"])
@parser_classes([MultiPartParser, FormParser])
def product_images(request, product_image_id=None):

    if request.method == 'DELETE':

        logging.info(f"DELETE request ProductImage with product_image_id: {product_image_id}")
        try:
            ProductImage.objects.get(id=product_image_id).delete()
            logging.info(f"DELETE success product_image_id: {product_image_id}")
            return Response(status=status.HTTP_200_OK)
        except ProductImage.DoesNotExist:
            logging.info(f"DELETE failed product_image_id: {product_image_id}")
            return Response(status=status.HTTP_200_OK)

    if request.method == 'POST':

        logging.info(f"POST request ProductImage with request data: {request.data}")

        images_data = []

        for key in request.data.keys():
            if key.startswith("productimages["):
                index, field = key.split("[")[1].split("].")
                index = int(index)  # Convert index to integer

                # Initialize a new dictionary or update existing
                while index >= len(images_data):
                    images_data.append({})
                images_data[index][field] = request.data[key]

        logging.info(f"POST request data processed into {images_data}")

        serializer = ProductImageSerializer(data=images_data, many=True)

        if serializer.is_valid():
            serializer.save()
            logging.info(f"POST request successful for ProductImage, ProductImage created: {serializer.data}")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            logging.info(f"POST request failed for ProductImage, ProductImage: {serializer.errors}")
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
