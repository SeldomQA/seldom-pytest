import pytest

pytest.main([
    "--browser=firefox",
    "--html=./report.html",
    "--base-url=https://www.baidu.com"
])
