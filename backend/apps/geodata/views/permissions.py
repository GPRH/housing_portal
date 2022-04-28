from rest_framework.permissions import BasePermission
from apps.geodata.models import AOI


class AOIPermission(BasePermission):
    """
        Check user permission on an AOI
        using either an id or a slug.
    """

    def has_permission(self, request, view):
        aoi_id = view.kwargs.get('aoi_id', None)
        slug = view.kwargs.get('aoi', None)
        aoi = None
        if aoi_id is None and slug is None:
            return False
        if aoi_id:
            try:
                aoi = AOI.objects.get(id=aoi_id)
            except AOI.DoesNotExist:
                return False
        if slug and not aoi:
            try:
                aoi = AOI.objects.get(slug=slug)
            except AOI.DoesNotExist:
                return False
        user = request.user
        groups = user.groups.all()
        perms = []
        for group in groups:
            perms = perms + [
                perm.codename.split('_')[1]
                for perm in group.permissions.all()
            ]
        perms = list(set(perms))
        return any([
            True for perm in perms
            if ''.join(aoi.city.lower().split()) == perm
        ])


class DownloadPermission(BasePermission):
    def has_permission(self, request, view):
        return any([
            True for group in request.user.groups.all()
            if 'Admin' in group.name or 'Government' in group.name
        ])
