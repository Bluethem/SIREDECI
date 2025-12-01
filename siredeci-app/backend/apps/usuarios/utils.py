from typing import Iterable, Set

from .models import Usuario, Rol, Permiso, UsuarioRol, RolPermiso


def get_roles(usuario: Usuario) -> Iterable[Rol]:
    """Retorna los roles asociados a un usuario dado."""
    if not usuario:
        return Rol.objects.none()
    return (
        Rol.objects
        .filter(usuariorol__id_usuario=usuario, esta_activo=True)
        .distinct()
    )


def get_codigos_roles(usuario: Usuario) -> Set[str]:
    """Retorna el conjunto de codigos de rol (codigo_rol) de un usuario."""
    return {r.codigo_rol for r in get_roles(usuario)}


def get_permisos(usuario: Usuario) -> Iterable[Permiso]:
    """Retorna los permisos efectivos de un usuario via sus roles."""
    if not usuario:
        return Permiso.objects.none()
    return (
        Permiso.objects
        .filter(rolpermiso__id_rol__usuariorol__id_usuario=usuario)
        .distinct()
    )


def get_codigos_permisos(usuario: Usuario) -> Set[str]:
    """Retorna el conjunto de codigos de permiso (codigo_permiso) de un usuario."""
    return {p.codigo_permiso for p in get_permisos(usuario)}
