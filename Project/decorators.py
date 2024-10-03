def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as ve:
            return f"Error happened: {ve}"
        except KeyError:
            return "Contact does not exist"
        except IndexError as e:
            return (f"I have no idea where this error can occur in the existing code, "
                    f"but here is the error: {e}")

    return inner
