def check_next_flag_bounds(len_of_array, next_flag):
    if next_flag < len_of_array - 1:
        return True
    return False

def check_flag_to_keys(
    flag : str,
    keys : list[str]
):
    for key in keys:
        if flag == key:
            return True
    return False