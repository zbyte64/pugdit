from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
import tempfile
import json
import os
from .models import Asset
from .mailtruck import client


@login_required
def add_asset(request):
    assert request.method == 'POST'
    print(request.FILES)
    print(request.POST)
    if request.FILES:
        _, file_o = next(request.FILES.items())
        filename = file_o.name
    else:
        data = json.loads(request.body)
        filename = data['filename']
        file_o = data['content'].encode('utf8')
    asset, ipfs_path = pin_asset(file_o, filename=filename, user=request.user)
    return HttpResponse(ipfs_path)


def add_assets(request):
    #TODO upload as a single directory
    assets = {}
    for key, file_o in request.FILES.items():
        asset = pin_asset(file_o, filename=key, user=request.user)
        assets[key] = asset
    return assets


def pin_asset(upload, filename, user):
    with tempfile.TemporaryDirectory() as tmpdirname:
        destination_path = os.path.join(tmpdirname, filename)
        with open(destination_path, 'wb+') as destination:
            if hasattr(upload, 'chunks'):
                for chunk in upload.chunks():
                    destination.write(chunk)
            else:
                destination.write(upload)
        #TODO don't assume first is the file, make path instead
        add_results = client.add(destination_path, wrap_with_directory=True)
        print('add_results:', add_results)
        path = [o['Name'] or o['Hash'] for o in add_results]
        ipfs_path = '/ipfs/' + '/'.join(reversed(path))
        add_result = add_results[0]
    print(add_result)
    asset, _c = Asset.objects.get_or_create(ipfs_hash=add_result['Hash'])
    asset.users.add(user)
    #TODO add paths
    if ipfs_path not in asset.ipfs_paths:
        asset.ipfs_paths.append(ipfs_path)
        asset.save()
    return asset, ipfs_path
