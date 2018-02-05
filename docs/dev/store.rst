*********
Store API
*********

The tozti core provides an API to perform operations on the database prefixed
with ``/api/store``. This API is largely inspired by jsonapi_ so you are
encouraged to go take a look at their specification.

Concepts and Datastructures
===========================

Resources
---------

Resources and `resource objects`_ are the main concept of the store API. A
resource is what we would call an entity in SQL lang or hypermedia in web lang.
A *resource object* is represented as a json object with the following
properties:

``id``
   An UUIDv4_ which uniquely identifies a resource.

``type``
   The name of a `type object`_.

``attributes``
   An arbitrary JSON object where each attribute is constained by the
   type of the resource.

``relationships``
   A JSON object where the keys are relationship names (just strings) and
   values are `relationship objects`_.

``meta``
   A JSON object containing some metadata about the resource. For now it
   only contains ``created`` and ``last-modified`` which are two
   self-explanatory dates in ISO 8601 format (UTC timezone).


.. _relationship objects:

Relationships
-------------

A relationship is a way to create a directed and tagged link between two
resources. Relationships can be *to-one* (resp. *to-many*) in which case
they link to one (resp. a sequence) of other resources. Practicaly, a
*resource object* is a JSON object with the following properties (beware,
here we diverge a little from the `JSON API spec <jsonapi rel>`_):

``self``
   An URL pointing to the current relationship object. This URL can be
   used to operate on this relationship.

``data``
   In the case of a *to-one* relationship, this is a *linkage object*, in the
   case of a *to-many* relationship, this is an array of *linkage objects*.

Linkages are simply pointers to a resource. They are JSON objects with three
properties:

``id``
   The ID of the target resource.

``type``
   The type of the target resource.

``href``
   An URL pointing to the target resource.


.. _type object:

Types
-----

A *type object* is simply a JSON object with the following properties:

``attributes``
    A JSON object where keys are allowed (and required) attribute names for
    resource objects and values are JSON Schemas. A `JSON Schema`_ is a
    format for doing data validation on JSON. For now we support the Draft-04
    version of the specification (which is the latest supported by the library
    we use).

``relationships``
    A JSON object where the keys are allowed (and required) relationship names
    and keys are relationship description objects.

Relationship description objects are of 2 kinds, let's start with the simple
one:

``arity``
   Either ``"to-one"`` or ``"to-many"``, self-explanatory.

``type``
   This property is optional and can be used to restrict what types the targets
   of this relationship can be. It can be either the name of a type object or
   an array of names of allowed type objects.

The other kind of relationship description exists because relationships are
directed. As such, because sometimes bidirectional relationships are useful, we
would want to specify that some relationship is the reverse of another one. To
solve that, instead of giving ``arity`` and ``type``, you may give
``reverse-of`` property is a JSON object with two properties: ``type`` (a type
URL) and ``path`` (a valid relationship name for that type). This will specify
a new *to-many* relationship that will not be writeable and automatically
filled by the Store engine. It will contain as target any resource of the given
type that have the current resource as target in the given relationship name.

Let's show an example, we will consider two types: users and groups.

::

   // http://localhost/types/user.json
   {
       "attributes": {
           "login": {"type": "string"},
           "email": {"type": "string", "format": "email"}
       },
       "relationships": {
           "groups": {
               "reverse-of": {
                   "type": "group",
                   "path": "members"
               }
           }
       }
   }

::

   // http://localhost/types/group.json
   {
       "attributes": {
           "name": {"type": "string"}
       },
       "relationships": {
           "members": {
               "arity": "to-many",
               "type": "user"
           }
       }
   }

Now when creating a user you cannot specify it's groups, but you can specify
members when creating (or updating) a given group and the system will
automagically take care of filling the ``groups`` relationship with the current
up-to-date content.


Endpoints
=========

TODO


.. _jsonapi: http://jsonapi.org/
.. _resource objects: http://jsonapi.org/format/#document-resource-objects
.. _UUIDv4: https://en.wikipedia.org/wiki/Universally_unique_identifier#Version_4_(random)
.. _jsonapi rel: http://jsonapi.org/format/#document-resource-object-relationships
.. _JSON Schema: http://json-schema.org/
