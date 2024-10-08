from enum import Enum


class Attribute(Enum):
    first_name = 'first_name'
    last_name = 'last_name'
    paid = 'paid'


class AttributeValue(Enum):
    paid_true = 'paid_true'
    paid_false = 'paid_false'


class Compare(Enum):
    equal = 'equal'
    contains = 'contains'
    custom_value = 'custom_value'
    attribute_value = 'value'
