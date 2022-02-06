import pytest

import feature as sut


class TestFeatureFromDict:
    def test_simple_feature(self):
        d = {"name": "Skynet", "ux_estimation": 2, "dev_estimation": 3}
        assert sut.Feature.from_dict(d) == sut.Feature(
            name="Skynet", ux_estimation=2, dev_estimation=3
        )

    def test_complex_feature(self):
        d = {
            "name": "Skynet",
            "ux_estimation": 2,
            "dev_estimation": 3,
            "conception_estimation": 2,
            "dev_scheduled_sprint": 13,
        }
        assert sut.Feature.from_dict(d) == sut.Feature(
            name="Skynet",
            ux_estimation=2,
            dev_estimation=3,
            conception_estimation=2,
            dev_scheduled_sprint=13,
        )

    def test_malformed_dict_raises(self):
        d = {"name": "Skynet", "hero": "Sarah Connor"}
        with pytest.raises(TypeError):
            sut.Feature.from_dict(d)
