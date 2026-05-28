from typing import *
from IR import Type

class TypeSystem:
  _registry: Dict[str, Dict[str, Type[Type]]] = {}
  _cache: Dict[Tuple[str, str, Tuple], Type] = {}

  @classmethod
  def register(cls, namespace: str, name: str):
    def inner_wrapper(wrapped_class: Type[Type]) -> Type[Type]:
      if (namespace, name) in cls._registry:
        raise Exception(f'Type {name} already registered in namespace {namespace}.')
      
      cls._registry[(namespace, name)] = wrapped_class

      return wrapped_class

    return inner_wrapper
  
  @classmethod
  def get_type(cls, namespace: str, name: str, **attributes) -> Type:
    try:
      hashable_attributes = tuple(sorted(attributes.items()))
    except:
      raise Exception('Attributes not hashable')
    
    if (namespace, name, hashable_attributes) in cls._cache:
      return cls._cache[(namespace, name, hashable_attributes)]
    
    if namespace not in cls._registry:
      raise Exception(f'Namespace {namespace} not registered.')
    elif name not in cls._registry[namespace]:
      raise Exception(f'Type {name} not defined in namespace {namespace}.')
    
    new_type = cls._registry[namespace][name](**attributes)
    cls._cache[(namespace, name, hashable_attributes)] = new_type

    return new_type