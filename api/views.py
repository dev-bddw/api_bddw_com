from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from .models import Product, MenuList, DropDownMenu
from .serializers import ProductSerializer, MenuListSerializer, DropDownMenuSerializer

hyphen_dict = { 'sev-drulo-series': 'sev-drulo series'}


@api_view(["GET", "PUT"])
@parser_classes([MultiPartParser, FormParser])
def api_response(request, slug=None):
    instance = None
    serializer_class = None

    if slug not in special_cases.keys():
        slug = slug.lower().replace("-", " ")
    else:
        slug = hyphen_dict[slug]

    # Try to get MenuList by slug
    try:
        instance = MenuList.objects.get(name__iexact=slug)
        serializer_class = MenuListSerializer
    except MenuList.DoesNotExist:
        # If MenuList not found, try to get Product by slug
        try:
            instance = Product.objects.get(name__iexact=slug)
            serializer_class = ProductSerializer
        except Product.DoesNotExist:
            # If neither is found, return an error response
            return Response({"error": "No matching MenuList or Product found"}, status=status.HTTP_404_NOT_FOUND)

    # Handle GET request
    if request.method == "GET":
        serializer = serializer_class(instance)
        body_response = {'body': serializer.data}
        return Response(body_response, status=status.HTTP_200_OK)

    # Handle PUT request
    elif request.method == "PUT":
        serializer = serializer_class(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Other HTTP methods are not supported
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

@api_view(['GET'])
def api_drop_down_menu(request):
    dropdown_menus = DropDownMenu.objects.all()
    serializer = DropDownMenuSerializer(dropdown_menus.first())
    body_response = {'body': serializer.data['data']}
    return Response(body_response)

