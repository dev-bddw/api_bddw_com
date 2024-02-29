from rest_framework import status
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
import logging

from .models import DropDownMenu, LandingPageImage, MenuList, Product
from .serializers import DropDownMenuSerializer, LandingPageImageSerializer, MenuListSerializer, ProductSerializer
####
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
def api_response(request, slug=None):
    instance = None
    serializer_class = None

    # Log the request method and slug
    logger.info(f"Received {request.method} request for slug: {slug}")

    if slug not in special_cases.keys():
        slug = slug.lower().replace("-", " ").replace("captains", "captain's").replace("admirals", "admiral's")
    else:
        slug = special_cases[slug]

    try:
        instance = MenuList.objects.get(name__iexact=slug)
        serializer_class = MenuListSerializer
        logger.info(f"MenuList instance found for slug: {slug}")
    except MenuList.DoesNotExist:
        try:
            instance = Product.objects.get(name__iexact=slug)
            serializer_class = ProductSerializer
            logger.info(f"Product instance found for slug: {slug}")
        except Product.DoesNotExist:
            logger.error(f"No matching MenuList or Product found for slug: {slug}")
            return Response({"error": "No matching MenuList or Product found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = serializer_class(instance)
        body_response = {"body": serializer.data}
        logger.info(f"GET request successful for slug: {slug}, returning data")
        return Response(body_response, status=status.HTTP_200_OK)

    elif request.method == "PUT":
        serializer = serializer_class(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info(f"PUT request successful for slug: {slug}, data updated")
            return Response(serializer.data)
        logger.warning(f"PUT request data invalid for slug: {slug}, returning errors")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    logger.warning(f"Method {request.method} not allowed for slug: {slug}")
    return Response({"error": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(["POST"])
@parser_classes([MultiPartParser, FormParser])
def api_create_product(request):
    # Extract and restructure images data if necessary
    images_data = []
    for key in request.data.keys():
        if key.startswith("images["):
            index, field = key.split("[")[1].split("].")
            index = int(index)  # Convert index to integer

            # Initialize a new dictionary or update existing
            while index >= len(images_data):
                images_data.append({})
            images_data[index][field] = request.data[key]

    # Include the images data in the request data
    request_data = {
        "name": request.data.get("name"),
        "blurb": request.data.get("blurb"),
        "meta": request.data.get("meta"),
        "images": images_data,
    }

    # Handle POST request
    serializer = ProductSerializer(data=request_data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@parser_classes([MultiPartParser, FormParser])
def api_create_menulist(request):
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

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def api_drop_down_menu(request):
    dropdown_menus = DropDownMenu.objects.all()
    serializer = DropDownMenuSerializer(dropdown_menus.first())
    body_response = {"body": serializer.data["data"]}
    return Response(body_response)


@api_view(["GET"])
def api_landing_page_images(request):
    landing_page_image = LandingPageImage.objects.all().order_by("?").first()
    serializer = LandingPageImageSerializer(landing_page_image)
    body_response = {"body": serializer.data}
    return Response(body_response)
