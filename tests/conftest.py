import pytest, os
from datetime import datetime
from selenium import webdriver
from pytest_metadata.plugin import metadata_key


@pytest.fixture()
def setup(browser):
    if browser=='edge':
        driver = webdriver.Edge()
        print("Launching Edge browser.........")
    elif browser=='firefox':
        driver = webdriver.Firefox()
        print("Launching firefox browser.........")
    else:
        driver = webdriver.Chrome()
        print("Launching chrome browser.........")
    return driver

def pytest_addoption(parser):    # This will get the value from CLI /hooks
    parser.addoption("--browser")

@pytest.fixture()
def browser(request):  # This will return the Browser value to setup method
    return request.config.getoption("--browser")

########### pytest HTML Report ################
# It is hook for Add/update/delete Environment info to HTML Report
#Specifying report folder location and save report with timestamp
def pytest_configure(config):
    config.stash[metadata_key]['Project Name'] = "Test Project"
    config.stash[metadata_key]['Environment Name'] = "QA"
    config.stash[metadata_key]['Test Name'] = "Pushkar Namaya"
    config.stash[metadata_key].pop("Python")
    config.stash[metadata_key].pop("Packages")
    config.stash[metadata_key].pop("Plugins")

    if not getattr(config.option, "htmlpath", None):
        # example: generate a path like "reports/report-YYYYMMDD-HHMMSS.html"
        from datetime import datetime
        now = datetime.now().strftime("%Y%m%d-%H%M%S")
        report_dir = os.path.join(os.getcwd(), "reports")
        os.makedirs(report_dir, exist_ok=True)
        config.option.htmlpath = os.path.join(report_dir, f"report-{now}.html")

def pytest_html_report_title(report):
    report.title = "Test Automation Report"