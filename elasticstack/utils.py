from haystack import connections


def prepare_object(obj, using='default'):
    """
    """
    model = obj.__class__
    unified_index = connections[using].get_unified_index()
    index = unified_index.get_index(model)
    prepped_data = index.full_prepare(obj)
    final_data = {}
    for key, value in prepped_data.items():
       final_data[key] = connections[using].get_backend().conn.from_python(value)
    return final_data
