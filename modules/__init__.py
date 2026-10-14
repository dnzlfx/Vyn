"""
VYN v1.2 - Modules Package
Specialized functionality modules

Los submodulos se cargan de forma perezosa (PEP 562). Importar el paquete por
si mismo ya no arrastra dependencias opcionales/pesadas (``paramiko``,
``requests``, ...): cada submodulo se importa solo cuando se usa realmente.
Esto permite, por ejemplo, importar ``modules.command_policy`` en tests sin
tener el stack completo instalado.
"""

import importlib
from typing import TYPE_CHECKING

_EXPORTS = {
    'CommandPolicy': '.command_policy',
    'HomeLab': '.homelab',
    'RAGManager': '.rag',
    'VisionAnalyzer': '.vision',
    'CVEScanner': '.security',
    'SecurityLayer': '.security_layer',
    'DockerHelper': '.docker_helper',
}

__all__ = list(_EXPORTS)

if TYPE_CHECKING:  # solo para type-checkers / IDEs
    from .command_policy import CommandPolicy  # noqa: F401
    from .homelab import HomeLab  # noqa: F401
    from .rag import RAGManager  # noqa: F401
    from .vision import VisionAnalyzer  # noqa: F401
    from .security import CVEScanner  # noqa: F401
    from .security_layer import SecurityLayer  # noqa: F401
    from .docker_helper import DockerHelper  # noqa: F401


def __getattr__(name):
    """Carga perezosa de los simbolos exportados por el paquete."""
    try:
        module_path = _EXPORTS[name]
    except KeyError:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    module = importlib.import_module(module_path, __name__)
    value = getattr(module, name)
    globals()[name] = value
    return value


def __dir__():
    return sorted(set(globals()) | set(__all__))
