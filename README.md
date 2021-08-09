# seldom-pytest

seldom support pytest


## installation

```shell
> pip install -U git+https://github.com/SeldomQA/seldom-pytest@main
```


## Example

Use the `page` fixture to write a basic test.

```python
# test_demo.py

def test_baidu(page):
    page.get("https://www.baidu.com")
    assert "百度一下" in page.get_title


def test_bing(page):
    page.get("https://www.bing.com")
    assert page.get_title == "Bing"

```

To run your tests, use pytest CLI.

````
# Run tests (chrome by default)
pytest

# Run tests in a different browser (chrome, firefox, safari)
pytest --browser chrome
pytest --browser firefox
pytest --browser safari
```
