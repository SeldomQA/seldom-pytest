from time import sleep


def test_baidu_search(baidu_page, base_url):
    """
    搜索
    """
    baidu_page.get(base_url)
    baidu_page.search_input.send_keys("pytest")
    baidu_page.search_button.click()
    sleep(2)
    assert baidu_page.get_title == "pytest_百度搜索"


def test_baidu_search_setting(baidu_page, base_url):
    """
    搜索设置
    """
    baidu_page.get(base_url)
    baidu_page.settings.click()
    baidu_page.search_setting.click()
    sleep(2)
    baidu_page.save_setting.click()
    alert_text = baidu_page.get_alert_text
    baidu_page.accept_alert()
    assert alert_text == "已经记录下您的使用偏好"
