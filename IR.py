from __future__ import annotations
from typing import *

class Type:
  def __eq__(self, other):
    raise NotImplementedError
  
  def __hash__(self):
    raise NotImplementedError

class Value:
  def __init__(self, type: Type, defining_op: Operation | None, name: str = ''):
    self.type = type
    self.defining_op = defining_op
    self.name = name
    self.users: Set[Operation] = set()

  def type(self):
    return self.type

  def defining_op(self):
    return self.defining_op

  def add_user(self, user: Operation):
    self.users.add(user)

  def remove_user(self, user: Operation):
    self.users.remove(user)

  def replace_all_uses_with(self, new_value: Value):
    for user in self.users.keys():
      user.replace_operand(new_value)
    
class Operation:
  def __init__(self, name: str, operands: List[Value], result_types: List[Type], attributes: Dict[str, Any] = {}, traits: Dict[str, Any] = {}):
    self.name = name
    self.operands = operands
    self.attributes = attributes
    self.traits = traits

    self.results = [Value(defining_op = self, name = f'{name}_out_{i}') for i, type in enumerate(result_types)]

    for operand in operands:
      operand.add_user(self)

  def replace_operand(self, old_val: Value, new_val: Value):
    for i in range(len(self.operands)):
      if self.operands[i] is old_val:
        self.operands[i] = new_val

        new_val.add_user(self)

    old_val.remove_user(self)

  def delete(self):
    if any(len(result.uses) for result in self.results):
      raise RuntimeError(f'Cannot erase {self.name}: results still in use.')
    
    for operand in self.operands:
      operand.remove_user(self)