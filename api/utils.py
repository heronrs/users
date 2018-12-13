from flask import jsonify, url_for
from flask_mongoengine import BaseQuerySet
from mongoengine.errors import DoesNotExist, MultipleObjectsReturned, ValidationError

from api.exceptions import APIException


class CustomBaseQuerySet(BaseQuerySet):
    def get_or_raise(self, *args, **kwargs):
        try:
            return self.get(*args, **kwargs)

        except DoesNotExist:
            raise APIException(
                "Resource not found %s %s" % (args, kwargs), status_code=404
            )
        except MultipleObjectsReturned:
            raise APIException(
                "Multiple resources found %s %s" % (args, kwargs), status_code=404
            )
        except ValidationError:
            raise APIException(
                "Invalid values provided %s %s" % (args, kwargs), status_code=400
            )


def paginated_response(paginator, view_name, payload, filters):
    payload["count"] = paginator.total

    if paginator.has_next:
        payload["next"] = url_for(
            view_name, page=paginator.next_num, per_page=paginator.per_page, **filters
        )

    if paginator.has_prev:
        payload["previous"] = url_for(
            view_name, page=paginator.prev_num, per_page=paginator.per_page, **filters
        )

    return jsonify(payload), 200


def clean_keys(filters, remove_text=""):
    """Remove arbitrary text from dictionary keys

        Example:
            dict = {'name__icontains': 'John'}
            clean_keys(data, remove_text='__icontains')

            {'name': 'John'}
    """

    cleaned_filters = {}

    for k, v in filters.items():
        cleaned_filters[k] = v
        cleaned_filters[k.replace(remove_text, "")] = cleaned_filters.pop(k)

    return cleaned_filters
