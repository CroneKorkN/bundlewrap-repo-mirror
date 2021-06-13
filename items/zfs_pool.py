from collections import Counter
from pipes import quote

from bundlewrap.exceptions import BundleError
from bundlewrap.items import Item
from bundlewrap.utils.text import mark_for_translation as _


def create_mirrors(node, path, mirrors):
    cmd = ""
    for devices in mirrors:
        actual_targets = []
        for device in devices:
            actual_targets.append(quote(prepare_blockdevice(node, device)))
        cmd += "mirror {} ".format(" ".join(actual_targets))

    node.run("zpool create {} {}".format(quote(path), cmd))
    node.run("zfs unmount {}".format(quote(path)))


def create_raidz(node, path, devices, raid='raidz'):
    cmd = ""
    actual_targets = []
    for device in devices:
        actual_targets.append(quote(prepare_blockdevice(node, device)))
    cmd += "{} {} ".format(raid, " ".join(actual_targets))

    node.run("zpool create {} {}".format(quote(path), cmd))
    node.run("zfs unmount {}".format(quote(path)))


def create_single(node, path, device):
    actual_target = prepare_blockdevice(node, device)
    node.run("zpool create {} {}".format(quote(path), quote(actual_target)))
    node.run("zfs unmount {}".format(quote(path)))


def does_exist(node, path):
    status_result = node.run(
        "zpool list {}".format(quote(path)),
        may_fail=True,
    )
    return status_result.return_code == 0


def prepare_blockdevice(node, device):
    # To increase our chances of success, we run partprobe beforehand to
    # make the kernel re-scan all devices.
    node.run("partprobe", may_fail=True)

    # Try to find out if the device already contains some filesystem.
    # Please note that there is no 100% reliable way to do this.
    res = node.run("lsblk -rndo fstype {}".format(quote(device)))
    detected = res.stdout.decode('UTF-8').strip()
    if detected != "":
        raise Exception(_("Device {} to be used for ZFS, but it is not empty! Has '{}'.").format(
            device, detected))
    else:
        return device


class ZFSPool(Item):
    """
    Creates ZFS pools and the required partitions.
    """
    BUNDLE_ATTRIBUTE_NAME = "zfs_pools"
    ITEM_ATTRIBUTES = {
        'device': None,
        'mirrors': None,
        'raidz': None,
        'raidz2': None,
        'raidz3': None,
    }
    ITEM_TYPE_NAME = "zfs_pool"

    def __repr__(self):
        return "<ZFSPool name:{} device:{} mirrors:{} raidz:{}>".format(
            self.name,
            self.attributes['device'],
            self.attributes['mirrors'],
            self.attributes['raidz'],
        )

    def cdict(self):
        return {}

    @property
    def devices_used(self):
        devices = []
        if self.attributes['device'] is not None:
            devices.append(self.attributes['device'])
        if self.attributes['mirrors'] is not None:
            for mirror in self.attributes['mirrors']:
                devices.extend(mirror)
        if self.attributes['raidz'] is not None:
            devices.extend(self.attributes['raidz'])
        return devices

    def fix(self, status):
        if status.must_be_created:
            if self.attributes['device'] is not None:
                create_single(self.node, self.name, self.attributes['device'])
            elif self.attributes['mirrors'] is not None:
                create_mirrors(self.node, self.name, self.attributes['mirrors'])
            elif self.attributes['raidz'] is not None:
                create_raidz(self.node, self.name, self.attributes['raidz'])
            elif self.attributes['raidz2'] is not None:
                create_raidz(self.node, self.name, self.attributes['raidz'], 'raidz2')
            elif self.attributes['raidz2'] is not None:
                create_raidz(self.node, self.name, self.attributes['raidz'], 'raidz3')

    def sdict(self):
        # We don't care about the device if the pool already exists.
        return {} if does_exist(self.node, self.name) else None

    def test(self):
        duplicate_devices = [
            item for item, count in Counter(self.devices_used).items() if count > 1
        ]
        if duplicate_devices:
            raise BundleError(_(
                "{item} on node {node} uses {devices} more than once as an underlying device"
            ).format(
                item=self.id,
                node=self.node.name,
                devices=_(" and ").join(duplicate_devices),
            ))

        # Have a look at all other ZFS pools on this node and check if
        # multiple pools try to use the same device.
        for item in self.node.items:
            if (
                item.ITEM_TYPE_NAME == "zfs_pool" and
                item.name != self.name and
                set(item.devices_used).intersection(set(self.devices_used))
            ):
                raise BundleError(_(
                    "Both the ZFS pools {self} and {other} on node {node} "
                    "try to use {devices} as the underlying storage device"
                ).format(
                    self=self.name,
                    other=item.name,
                    node=self.node.name,
                    devices=_(" and ").join(set(item.devices_used).intersection(set(self.devices_used))),
                ))

    @classmethod
    def validate_attributes(cls, bundle, item_id, attributes):
        device_config = []
        for key in ('device', 'mirrors', 'raidz', 'raidz2', 'raidz3'):
            device_config.append(attributes.get(key))
        device_config = [key for key in device_config if key is not None]
        if len(device_config) != 1:
            raise BundleError(_(
                "{item} on node {node} must have exactly one of "
                "'device', 'mirrors', 'raidz', 'raidz2' or 'raidz3'"
            ).format(
                item=item_id,
                node=bundle.node.name,
            ))
