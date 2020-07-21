import os
import re
import shutil

from avionix import ChartBuilder, ChartInfo
from avionix.kubernetes_objects.deployment import Deployment
from avionix.tests.utils import (
    ChartInstallationContext,
    get_helm_installations,
    kubectl_get,
)


def test_chart_folder_building(test_deployment1: Deployment, test_folder):
    os.makedirs(test_folder, exist_ok=True)
    builder = ChartBuilder(
        ChartInfo(api_version="3.2.4", name="test", version="0.1.0"),
        [test_deployment1, test_deployment1],
        test_folder,
    )
    builder.generate_chart()
    templates_folder = test_folder / builder.chart_info.name / "templates"

    for file in os.listdir(templates_folder):
        with open(templates_folder / Path(file)) as kube_file:
            assert kube_file.read() == str(test_deployment1)

        assert re.match(rf"{test_deployment1.kind}-[0-9]+\.yaml", file)
    shutil.rmtree(test_folder)


def test_chart_installation(test_deployment1: Deployment, test_folder):
    builder = ChartBuilder(
        ChartInfo(api_version="3.2.4", name="test", version="0.1.0", app_version="v1"),
        [test_deployment1],
        test_folder,
    )
    with ChartInstallationContext(builder):
        # Check helm release
        helm_installation = get_helm_installations()
        assert helm_installation["NAME"][0] == "test"
        assert helm_installation["REVISION"][0] == "1"
        assert helm_installation["STATUS"][0] == "deployed"

        deployments = kubectl_get("deployments")
        assert deployments["NAME"][0] == "test-deployment-1"
        assert deployments["READY"][0] == "1/1"

        pods = kubectl_get("pods")
        assert pods["READY"][0] == "1/1"
        assert pods["STATUS"][0] == "Running"


def test_intalling_two_components(
    test_folder,
    test_deployment1: Deployment,
    test_deployment2: Deployment,
    chart_info: ChartInfo,
):
    builder = ChartBuilder(
        chart_info, [test_deployment1, test_deployment2], test_folder,
    )
    with ChartInstallationContext(builder):
        # Check helm release
        helm_installation = get_helm_installations()
        assert helm_installation["NAME"][0] == "test"
        assert helm_installation["REVISION"][0] == "1"
        assert helm_installation["STATUS"][0] == "deployed"

        # Check kubernetes components
        deployments = kubectl_get("deployments")
        pods = kubectl_get("pods")
        for i in range(2):
            assert pods["READY"][i] == "1/1"
            assert pods["STATUS"][i] == "Running"
            assert deployments["NAME"][i] == f"test-deployment-{i + 1}"
            assert deployments["READY"][i] == "1/1"
