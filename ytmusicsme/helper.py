def convert_string_to_number(input_str):

    input_str = input_str.replace(" ", "")
    input_str = input_str.replace(u'\xa0', u'')
    input_str = input_str.replace(',', '.')

    suffixes = {'tys.': 1e3, 'mln': 1e6, 'mld': 1e9}
    # Check if the input string has a valid suffix
    for suffix, factor in suffixes.items():
        if input_str.endswith(suffix):
            # Remove the suffix and convert to a float
            number_part = float(input_str[:-1 * len(suffix)])
            # Multiply by the corresponding factor
            return number_part * factor
    
    # If no valid suffix is found, simply convert to a float
    return float(input_str)



def find_musicPlaylistShelfRenderer(json_obj):
    if isinstance(json_obj, dict):
        if 'musicPlaylistShelfRenderer' in json_obj:
            return json_obj['musicPlaylistShelfRenderer']
        else:
            for key, value in json_obj.items():
                result = find_musicPlaylistShelfRenderer(value)
                if result is not None:
                    return result
    elif isinstance(json_obj, list):
        for item in json_obj:
            result = find_musicPlaylistShelfRenderer(item)
            if result is not None:
                return result
    return None


def find_musicPlaylistShelfContinuation(json_obj):
    if isinstance(json_obj, dict):
        if 'musicPlaylistShelfContinuation' in json_obj:
            return json_obj['musicPlaylistShelfContinuation']
        else:
            for key, value in json_obj.items():
                result = find_musicPlaylistShelfContinuation(value)
                if result is not None:
                    return result
    elif isinstance(json_obj, list):
        for item in json_obj:
            result = find_musicPlaylistShelfContinuation(item)
            if result is not None:
                return result
    return None



def find_musicShelfRenderer(json_obj):
    if isinstance(json_obj, dict):
        if 'musicShelfRenderer' in json_obj:
            return json_obj['musicShelfRenderer']
        else:
            for key, value in json_obj.items():
                result = find_musicShelfRenderer(value)
                if result is not None:
                    return result
    elif isinstance(json_obj, list):
        for item in json_obj:
            result = find_musicShelfRenderer(item)
            if result is not None:
                return result
    return None


def find_all_music_renderers(json_obj):
    result_list = []

    def search(obj):
        if isinstance(obj, dict):
            if 'musicResponsiveListItemRenderer' in obj:
                result_list.append(obj['musicResponsiveListItemRenderer'])
            else:
                for value in obj.values():
                    search(value)
        elif isinstance(obj, list):
            for item in obj:
                search(item)

    search(json_obj)
    return result_list


def find_browseEndpointContextSupportedConfigs(json_obj):
    if isinstance(json_obj, dict):
        if 'browseEndpointContextSupportedConfigs' in json_obj:
            return json_obj['browseEndpointContextSupportedConfigs']
        else:
            for key, value in json_obj.items():
                result = find_browseEndpointContextSupportedConfigs(value)
                if result is not None:
                    return result
    elif isinstance(json_obj, list):
        for item in json_obj:
            result = find_browseEndpointContextSupportedConfigs(item)
            if result is not None:
                return result
    return None


def find_objects_list(json_obj,object_name):
    result_list = []

    def search(obj,object_name):
        if isinstance(obj, dict):
            if object_name in obj:
                result_list.append(obj[object_name])
            else:
                for value in obj.values():
                    search(value,object_name)
        elif isinstance(obj, list):
            for item in obj:
                search(item,object_name)

    search(json_obj,object_name)
    return result_list