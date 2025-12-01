from rest_framework.permissions import BasePermission

from .utils import get_codigos_roles, get_codigos_permisos


class IsStaffLike(BasePermission):
    """Permite acceso a usuarios internos (no ciudadanos).

    Considera como internos a los roles distintos de ROL-005 (Ciudadano).
    """

    def has_permission(self, request, view):
        user = getattr(request, "user", None)
        if not user or not getattr(user, "is_authenticated", False):
            return False

        roles = get_codigos_roles(user)
        if not roles:
            return False

        # Si el usuario solo tiene rol de Ciudadano, se bloquea.
        if roles == {"ROL-005"}:
            return False

        return True


class HasRol(BasePermission):
    """Permite acceso solo si el usuario tiene al menos uno de los roles indicados."""

    def __init__(self, required_roles):
        # required_roles: iterable de codigos de rol (p.ej. ["ROL-002", "ROL-003"])
        self.required_roles = set(required_roles or [])

    def has_permission(self, request, view):
        if not self.required_roles:
            return False

        user = getattr(request, "user", None)
        if not user or not getattr(user, "is_authenticated", False):
            return False

        roles = get_codigos_roles(user)
        return bool(self.required_roles.intersection(roles))


class HasPermiso(BasePermission):
    """Permite acceso solo si el usuario posee alguno de los permisos indicados."""

    def __init__(self, required_perms):
        # required_perms: iterable de codigos de permiso (p.ej. ["PER-010", "PER-011"])
        self.required_perms = set(required_perms or [])

    def has_permission(self, request, view):
        if not self.required_perms:
            return False

        user = getattr(request, "user", None)
        if not user or not getattr(user, "is_authenticated", False):
            return False

        permisos = get_codigos_permisos(user)
        return bool(self.required_perms.intersection(permisos))
