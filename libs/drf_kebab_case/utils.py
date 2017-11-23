from collections import OrderedDict


def kebabize_key(key):
    return key.replace('_', '-')


def underscoreize_key(key):
    return key.replace('-', '_')


def transform_keys(data, transform):
    if isinstance(data, dict):
        new_dict = OrderedDict()
        for k, v in data.items():
            new_dict[transform(k)] = transform_keys(v, transform)

        return new_dict

    if isinstance(data, list):
        return [transform_keys(x, transform) for x in data]

    if isinstance(data, tuple):
        return tuple(transform_keys(x, transform) for x in data)

    return data


def underscoreize(data):
    return transform_keys(data, underscoreize_key)


def kebabize(data):
    return transform_keys(data, kebabize_key)

