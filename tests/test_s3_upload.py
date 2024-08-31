import pytest
from moto import mock_aws

from libraries.s3 import generate_post_url


@mock_aws
def test_it_should_be_able_to_generate_upload_url():
    response = generate_post_url("products-covers", "product.jpeg")
    assert response


if __name__ == "__main__":
    pytest.main()
