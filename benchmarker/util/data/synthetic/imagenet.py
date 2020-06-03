"""Generate synthetic data for ImageNet type problems"""


from .helpers import gen_classification_data


def get_data(params):
    """Generate synthetic data for ImageNet type problems. Set
    `params["size"]` appropriately. Import this function in the
    `data.py` of the problem, so it can be called by `INeuralNet`.

    """

    if isinstance(params["problem"]["size"], int):
        if params["channels_first"]:
            params["problem"]["size"] = (params["problem"]["size"], 3, 224, 224)
        else:
            params["problem"]["size"] = (params["problem"]["size"], 224, 224, 3)

    return gen_classification_data(params)