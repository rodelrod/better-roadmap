from pydantic import ValidationError
import pytest

import better_roadmap.models.features as sut


class TestFeatureFromDict:
    def test_simple_feature(self):
        d = {"name": "Skynet", "estimations": {"ux": 2, "dev": 3}}
        assert sut.Feature(**d) == sut.Feature(
            name="Skynet", estimations={"ux": 2, "dev": 3}
        )

    def test_complex_feature(self):
        d = {
            "name": "Skynet",
            "estimations": {"ux": 2, "dev": 3, "conception": 2},
        }
        assert sut.Feature(**d) == sut.Feature(
            name="Skynet",
            estimations={"ux": 2, "dev": 3, "conception": 2},
        )

    def test_malformed_dict_raises(self):
        d = {"name": "Skynet", "hero": "Sarah Connor"}
        with pytest.raises(ValidationError):
            sut.Feature(**d)
