import pytest

import better_roadmap.feature as sut


class TestFeatureFromDict:
    def test_simple_feature(self):
        d = {"name": "Skynet", "estimations": {"ux": 2, "dev": 3}}
        assert sut.Feature.from_dict(d) == sut.Feature(
            name="Skynet", estimations={"ux": 2, "dev": 3}
        )

    def test_complex_feature(self):
        d = {
            "name": "Skynet",
            "estimations": {"ux": 2, "dev": 3, "conception": 2},
            "real_start": {"dev": 13},
            "real_duration": {"dev": 2},
        }
        assert sut.Feature.from_dict(d) == sut.Feature(
            name="Skynet",
            estimations={"ux": 2, "dev": 3, "conception": 2},
            real_start={"dev": 13},
            real_duration={"dev": 2},
        )

    def test_malformed_dict_raises(self):
        d = {"name": "Skynet", "hero": "Sarah Connor"}
        with pytest.raises(TypeError):
            sut.Feature.from_dict(d)
