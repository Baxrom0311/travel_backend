from rest_framework.exceptions import ValidationError


COMMON_QUERY_PARAMS = {'format', 'lang', 'page', 'page_size'}


def reject_unknown_query_params(query_params, allowed_params):
    allowed = set(allowed_params) | COMMON_QUERY_PARAMS
    unknown = sorted(set(query_params.keys()) - allowed)
    if unknown:
        raise ValidationError({
            param: ["Noma'lum query param."]
            for param in unknown
        })
