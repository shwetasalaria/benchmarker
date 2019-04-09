"""Module contains the interface for all deep learning modules"""
import importlib


class INeuralNet():
    """Interface for all deep learning modules"""

    def __init__(self, params):
        self.params = params
        if "batch_size_per_device" in params:
            self.params["batch_size_per_device"] = params["batch_size_per_device"]
        else:
            self.params["batch_size_per_device"] = 32
        self.params["batch_size"] = self.params["batch_size_per_device"]
        if self.params["nb_gpus"] > 0:
            self.params["batch_size"] = self.params["batch_size_per_device"] * self.params["nb_gpus"]
        self.params["channels_first"] = True
        if params["mode"] is None:
            params["mode"] = "training"
        assert params["mode"] in ["training", "inference"]

    def load_data(self):
        params = self.params
        mod = importlib.import_module("benchmarker.modules.problems." + params["problem"]["name"] + ".data")
        get_data = getattr(mod, 'get_data')
        data = get_data(params)
        params["problem"]["bytes_x_train"] = data[0].nbytes
        params["problem"]["shape_x_train"] = data[0].shape
        params["problem"]["cnt_batches_per_epoch"] = data[0].shape[0] / self.params["batch_size"]
        return data