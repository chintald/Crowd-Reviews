import json
import graphene
from graphene_django.forms.converter import convert_form_field
from graphene_django.converter import convert_django_field
from api.core.filters import EnumFilter
from api.core.filters import ObjectTypeFilter
from graphql.language import ast
from graphene.types import Scalar
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.db import models as gis_models

class GISScalar(Scalar):
    @property
    def geom_typeid(self):
        raise NotImplementedError(
            "GEOSScalar is an abstract class and doesn't have a 'geom_typeid'. \
            Instantiate a concrete subtype instead."
        )

    @staticmethod
    def serialize(geometry):
        return eval(geometry.geojson)

    @classmethod
    def parse_literal(cls, node):
        assert isinstance(node, ast.StringValue)
        geometry = GEOSGeometry(node.value)
        return eval(geometry.geojson)

    @classmethod
    def parse_value(cls, node):
        geometry = GEOSGeometry(node.value)
        return eval(geometry.geojson)


class PointScalar(GISScalar):
    geom_typeid = 0

    class Meta:
        description = "A GIS Point geojson"


GIS_FIELD_SCALAR = {
    "PointField": PointScalar
}


@convert_form_field.register(ObjectTypeFilter)
@convert_form_field.register(EnumFilter)
def convert_convert_enum(field):
    return field.input_class()


@convert_django_field.register(gis_models.PointField)
def gis_converter(field, registry=None):
    class_name = field.__class__.__name__
    return GIS_FIELD_SCALAR[class_name](
        required=not field.null, description=field.help_text
    )
