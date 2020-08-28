import pytest

from avionix import ChartBuilder, ObjectMeta
from avionix.kube.storage import (
    CSINode,
    CSINodeSpec,
    CSIDriver,
    CSIDriverSpec,
    CSINodeDriver,
    StorageClass,
    VolumeAttachment,
    VolumeNodeResources,
)
from avionix.kube.core import TopologySelectorTerm, TopologySelectorLabelRequirement
from avionix.testing import kubectl_get
from avionix.testing.installation_context import ChartInstallationContext
from pandas import DataFrame


@pytest.mark.parametrize(
    "driver",
    [
        CSIDriver(
            ObjectMeta(name="test-driver-lifecycle"),
            CSIDriverSpec(volume_lifecycle_modes=["Ephemeral"]),
        ),
        CSIDriver(ObjectMeta(name="test-driver-attach"), CSIDriverSpec(False),),
    ],
)
def test_csi_driver(chart_info, driver: CSIDriver):
    builder = ChartBuilder(chart_info, [driver])
    with ChartInstallationContext(builder):
        driver_info = kubectl_get("csidriver")
        assert driver_info["NAME"][0] == driver.metadata.name
        assert (
            driver_info["ATTACHREQUIRED"][0]
            == str(bool(driver.spec.attachRequired)).lower()
            if driver.spec.attachRequired is not None
            else "true"
        )
        assert driver_info["MODES"][0] == (
            driver.spec.volumeLifecycleModes[0]
            if driver.spec.volumeLifecycleModes
            else "Persistent"
        )


@pytest.mark.parametrize(
    "csi_node",
    [
        CSINode(
            ObjectMeta(name="test-node"),
            CSINodeSpec([CSINodeDriver("test", "test-id")]),
        ),
        CSINode(
            ObjectMeta(name="test-node"),
            CSINodeSpec([CSINodeDriver("test", "test-id", VolumeNodeResources(2))]),
        ),
    ],
)
def test_csi_node(chart_info, csi_node: CSINode):
    builder = ChartBuilder(chart_info, [csi_node],)
    with ChartInstallationContext(builder):
        csi_node_info = kubectl_get("csinode")
        csi_frame = DataFrame(csi_node_info)
        csi_frame = csi_frame[csi_frame["NAME"] != "minikube"].reset_index(drop=True)
        assert csi_frame["NAME"][0] == csi_node.metadata.name
        assert csi_frame["DRIVERS"][0] == str(len(csi_node.spec.drivers))


@pytest.mark.parametrize(
    "storage_class",
    [
        StorageClass(ObjectMeta(name="test-storage-class"), "provisioner"),
        StorageClass(
            ObjectMeta(name="test-storage-class"),
            "provisioner",
            allowed_topologies=[
                TopologySelectorTerm(
                    [TopologySelectorLabelRequirement("test-key", ["value1", "value2"])]
                )
            ],
        ),
    ],
)
def test_storage_class(chart_info, storage_class: StorageClass):
    builder = ChartBuilder(chart_info, [storage_class],)
    with ChartInstallationContext(builder):
        storage_class_info_dict = DataFrame(kubectl_get("storageclass"))
        filtered = storage_class_info_dict[
            storage_class_info_dict["NAME"] == storage_class.metadata.name
        ].reset_index()
        assert filtered["NAME"][0] == storage_class.metadata.name
        assert filtered["PROVISIONER"][0] == storage_class.provisioner