__author__ = 'ad'

import os.path
import pyraml.parser
from collections import OrderedDict
from pyraml.entities import RamlResource, RamlMethod, RamlQueryParameter

fixtures_dir = os.path.join(os.path.dirname(__file__), '..', 'samples')


def test_resource_nested():
    p = pyraml.parser.load(os.path.join(fixtures_dir, 'resource-nested.yaml'))
    assert isinstance(p.resources, OrderedDict), p.resources
    assert len(p.resources) == 1, p.resources

    # Validate root resource
    assert "/media" in p.resources, p.resources
    root_resource = p.resources["/media"]

    assert isinstance(root_resource, RamlResource), p.resources
    assert root_resource.parentResource is None, p.resources
    assert root_resource.methods is not None, p.resources
    assert root_resource.description == "Media Description", root_resource
    assert "get" in root_resource.methods, p.resources
    assert isinstance(root_resource.methods["get"], RamlMethod), p.resources
    assert root_resource.methods["get"].notNull, p.resources

    # validate sub-resources
    assert root_resource.resources is not None, root_resource

    assert "/search" in root_resource.resources is not None, root_resource
    assert root_resource.resources["/search"].displayName == "Media Search", root_resource
    assert root_resource.resources["/search"].description == "Media Search Description", root_resource
    assert "get" in root_resource.resources["/search"].methods, root_resource
    assert root_resource.resources["/search"].methods["get"].notNull, root_resource

    assert "/tags" in root_resource.resources is not None, root_resource
    assert root_resource.resources["/tags"].displayName == "Tags", root_resource
    assert root_resource.resources["/tags"].description == "Tags Description", root_resource
    assert "get" in root_resource.resources["/tags"].methods, root_resource
    assert root_resource.resources["/tags"].methods["get"].notNull, root_resource

    # /media/tags has their own resource /search
    tag_resource = root_resource.resources["/tags"]
    assert tag_resource.resources is not None, tag_resource
    assert "/search" in tag_resource.resources, tag_resource
    assert tag_resource.resources["/search"].displayName == "Tag Search", tag_resource
    assert tag_resource.resources["/search"].description == "Tag Search Description", tag_resource
    assert tag_resource.resources["/search"].methods["get"].notNull, root_resource

    # Ensure than every sub-resource have correct parentResource
    assert root_resource.resources["/search"].parentResource is root_resource
    assert root_resource.resources["/tags"].parentResource is root_resource
    assert tag_resource.resources["/search"].parentResource is tag_resource


def test_resource_with_responses():
    p = pyraml.parser.load(os.path.join(fixtures_dir, 'null-elements.yaml'))
    assert isinstance(p.resources, OrderedDict), p.resources

    assert "/leagues" in p.resources, p

    leagues_resource = p.resources["/leagues"]
    assert leagues_resource.displayName == "Leagues", leagues_resource
    assert leagues_resource.description is None, leagues_resource
    assert leagues_resource.methods, leagues_resource
    assert leagues_resource.methods["get"], leagues_resource

    leagues_resource_get = leagues_resource.methods["get"]
    assert leagues_resource_get.responses, leagues_resource_get
    assert leagues_resource_get.responses[200], leagues_resource_get
    assert leagues_resource_get.responses[200].body, leagues_resource_get

    assert "application/json" in leagues_resource_get.responses[200].body, leagues_resource_get
    assert "text/xml" in leagues_resource_get.responses[200].body, leagues_resource_get


def test_resource_with_params():
    p = pyraml.parser.load(os.path.join(fixtures_dir, 'params', 'param-types.yaml'))
    assert isinstance(p.resources, OrderedDict), p.resources

    assert "/simple" in p.resources, p
    simple_res = p.resources["/simple"]
    assert "get" in simple_res.methods, simple_res

    queryParameters = simple_res.methods["get"].queryParameters

    assert "name" in queryParameters, queryParameters
    assert "age" in queryParameters, queryParameters
    assert "price" in queryParameters, queryParameters
    assert "time" in queryParameters, queryParameters
    assert "alive" in queryParameters, queryParameters
    assert "default-enum" in queryParameters, queryParameters

    queryParam1 = queryParameters["name"]
    assert isinstance(queryParam1, RamlQueryParameter), queryParam1
    assert queryParam1.example == "two", queryParam1
    assert queryParam1.enum == ["one", "two", "three"], queryParam1
    assert queryParam1.displayName == "name name", queryParam1
    assert queryParam1.description == "name description"
    assert queryParam1.default == "three", queryParam1
    assert queryParam1.minLength == 3, queryParam1
    assert queryParam1.type == "string", queryParam1
    assert queryParam1.maxLength == 5, queryParam1
    assert queryParam1.pattern == '[a-z]{3,5}', queryParam1
    assert queryParam1.required == False, queryParam1
    assert queryParam1.repeat == False, queryParam1

