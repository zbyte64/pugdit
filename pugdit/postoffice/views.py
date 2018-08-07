from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import tempfile
from .models import Asset
from .mailtruck import client


def add_asset(request):
    assert request.method == 'POST'
    key, file_o = next(request.FILES.items())
    asset = pin_asset(file_o, filename=key, user=request.user)
    return HttpResponse(asset.get_absolute_url())


def add_assets(request):
    assets = {}
    for key, file_o in request.FILES.items():
        asset = pin_asset(file_o, filename=key, user=request.user)
        assets[key] = asset
    return assets


def pin_asset(upload, filename, user):
    with tempfile.TemporaryDirectory() as tmpdirname:
        destination_path = os.path.join(tmpdirname, filename)
        with open(destination_path, 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)
        add_result = client.add(destination_path)
    asset, _c = Asset.objects.get_or_create(ipfs_hash=add_result['Hash'])
    asset.users.add(user)
    return asset
