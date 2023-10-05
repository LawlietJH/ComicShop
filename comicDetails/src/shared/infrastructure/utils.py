import time


class Utils:

    @staticmethod
    def get_method_name(obj, func_name: str = '') -> str:
        obj_class_name = f"{obj.__class__.__module__}." \
                         f"{obj.__class__.__qualname__}"
        return f'{obj_class_name}.{func_name}' if func_name else obj_class_name

    @staticmethod
    def add_attributes(obj, data: dict) -> None:
        """ Add the extra attributes. """
        for key, value in data.items():
            setattr(obj, key, value)

    @staticmethod
    def discard_empty_attributes(obj) -> None:
        """ Removes all attributes of the object that represent a value of
        type 'False': None, False, 0, '', [], (], {}. value of type 'False':
        None, False, 0, '', [], (), {}. """
        obj_copy = obj.__dict__.copy()
        for key, value in obj_copy.items():
            if not value:
                delattr(obj, key)

    @staticmethod
    def sort_attributes(obj) -> None:
        """ Sorts the attributes of the object. """
        obj.__dict__ = dict(sorted(obj.__dict__.items()))

    @staticmethod
    def get_error_details(errors):
        return list(map(lambda error: f"{error['loc'][1]}: {error['msg']} in"
                                      f" {error['loc'][0]}", errors))

    @staticmethod
    def get_time_elapsed_ms(init_time: float, decimals: int = 2):
        current_time = time.perf_counter()
        time_elapsed = current_time - init_time
        return round(time_elapsed * 1000, decimals)
