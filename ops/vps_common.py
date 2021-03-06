#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import random
import string
import os
import tempfile
import time
import re
import _env
from lib.command import call_cmd

#def call_cmd (cmd):
#    res = os.system (cmd)
#    if res != 0:
#        raise Exception ("%s exit with %d" % (cmd, res))

def call_cmd_via_ssh (ip, user, password, cmd):
    import paramiko
    client = paramiko.SSHClient()
#    client.load_system_host_keys ()
    client.set_missing_host_key_policy (paramiko.AutoAddPolicy ())
    client.connect (ip, username=user, password=password, look_for_keys=False)
    try:
        stdin, stdout, stderr = client.exec_command(cmd)
        try:
            exit_status = stdout.channel.recv_exit_status()
            out = "\n".join (stdout.readlines ())
            err = "\n".join (stderr.readlines ())
            return exit_status, out, err
        finally:
            stdin.close ()
            stdout.close ()
            stderr.close ()
    finally:
        client.close ()


def gen_password (length=10):
    return "".join ([ random.choice(string.hexdigits) for i in xrange (0, length) ])

def gen_mac ():
    cmd = """(date; cat /proc/interrupts) | md5sum | sed -r 's/^(.{6}).*$/\\1/; s/([0-9a-f]{2})/\\1:/g; s/:$//;'"""
    s = "00:16:3e:"
    out = call_cmd (cmd)
    return s + out

def mount_loop_tmp (img_path, readonly=False):
    """ create temporary mount point and mount loop file """
    tmp_mount = tempfile.mkdtemp (prefix='mountpoint')
    try:
        if readonly:
            call_cmd ("mount %s %s -o loop,ro" % (img_path, tmp_mount))
        else:
            call_cmd ("mount %s %s -o loop" % (img_path, tmp_mount))
    except Exception, e:
        os.rmdir (tmp_mount)
        raise e
    return tmp_mount

def mount_partition_tmp (dev_path, readonly=False):
    tmp_mount = tempfile.mkdtemp (prefix='mountpoint')
    try:
        if readonly:
            call_cmd ("mount %s %s -o ro" % (dev_path, tmp_mount))
        else:
            call_cmd ("mount %s %s" % (dev_path, tmp_mount))
    except Exception, e:
        os.rmdir (tmp_mount)
        raise e
    return tmp_mount

def get_partition_fs_type (mount_point=None, dev_path=None):
    """ NOTE that /dev/main/vps00_root will actually be  /dev/mapper/main-vps00_root in /proc/mounts, so dev_path is not likely to be reliable
    """
    assert dev_path or mount_point
    if mount_point and mount_point != "/":
        mount_point = mount_point.rstrip ("/")
    f = open ("/proc/mounts", "r")
    lines = None
    try:
        lines = f.readlines ()
    finally:
        f.close ()
    lines.reverse ()
    for line in lines:
        arr = line.split ()
        if dev_path and arr[0] == dev_path:
            return arr[2]
        if mount_point and arr[1] == mount_point:
            return arr[2]
    if mount_point:
        raise Exception ("%s is not a mount point" % (mount_point))
    elif dev_path:
        raise Exception ("device %s is not mounted" % (dev_path))


def umount_tmp (tmp_mount):
    """ umount loop file and delete temporary mount point """
    call_cmd ("umount %s" % (tmp_mount))
    os.rmdir (tmp_mount)

def create_raw_image (path, size_g, sparse=False):
    assert size_g > 0
    size_m = int (size_g * 1024)
    if sparse:
        call_cmd ("dd if=/dev/zero of=%s bs=1M count=1 seek=%d" % (path, size_m - 1))
    else:
        call_cmd ("dd if=/dev/zero of=%s bs=1M count=%d" % (path, size_m))

def format_fs (fs_type, target):
    if fs_type in ['ext4', 'ext3', 'ext2']:
        mkfs_cmd = "mkfs.%s -F" % (fs_type)
    elif fs_type == 'reiserfs':
        mkfs_cmd = "mkfs.reiserfs -f"
    elif fs_type in ['swap']:
        mkfs_cmd = "mkswap"
    elif fs_type == 'raw':
        pass
    else:
        raise Exception ("not supported fs_type %s" % (fs_type))
    call_cmd ("%s %s" % (mkfs_cmd, target))


def sync_img (vpsmountpoint, template_img_path):
    if vpsmountpoint[-1] != '/':
        vpsmountpoint += "/"
    template_mount = mount_loop_tmp (template_img_path, readonly=True)
    if template_mount[-1] != '/':
        template_mount += "/"
    try:
        call_cmd ("rsync -a '%s/' '%s/'" % (template_mount, vpsmountpoint)) 
    finally:
        umount_tmp (template_mount)

def unpack_tarball (vpsmountpoint, tarball_path):
    pwd = os.getcwd()
    os.chdir (vpsmountpoint)
    try:
        if re.match ("^.*\.(tar\.gz|tgz)$", tarball_path):
            call_cmd ("tar zxf '%s'" % (tarball_path))
        elif re.match ('^.*\.(tar\.bz2|tbz2)$', tarball_path):
            call_cmd ("tar jxf '%s'" % (tarball_path))
    finally:
        os.chdir (pwd)

def vg_free_space (vg_name):
    out = call_cmd ("vgs --noheadings -o vg_free --units g --nosuffix /dev/%s" % (vg_name))
    out = out.strip ()
    return int (float (out))

def lv_create (vg_name, lv_name, size_g):
    assert size_g > 0
    size_m = int (size_g * 1024)
    call_cmd ("lvcreate --name %s --size %dM /dev/%s" % (lv_name, size_m, vg_name))
    lv_dev = "/dev/%s/%s" % (vg_name, lv_name)
    if not os.path.exists (lv_dev):
        raise Exception ("lv %s not exists after creating" % (lv_dev))
    return lv_dev

def lv_delete (lv_dev):
    call_cmd ("lvremove -f %s" % (lv_dev))

def lv_rename (src_dev, dest_dev):
    call_cmd ("lvrename %s %s " % (src_dev, dest_dev))


def pack_vps_fs_tarball (img_path, tarball_dir_or_path):
    """ if tarball_dir_or_path is a directory, will generate filename like XXX_fs_FSTYPE.tar.gz  """
    tarball_dir = None
    tarball_path = None
    if os.path.isdir (tarball_dir_or_path):
        tarball_dir = tarball_dir_or_path
    else:
        if os.path.exists (tarball_dir_or_path):
            raise Exception ("file %s exists" % (tarball_dir_or_path))
        tarball_path = tarball_dir_or_path
        tarball_dir = os.path.dirname (tarball_path)
        if not os.path.isdir (tarball_dir):
            raise Exception ("directory %s not exists" % (tarball_dir))

    if img_path.find ("/dev") == 0:
        mount_point = mount_partition_tmp (img_path, readonly=True)
    else:
        mount_point = mount_loop_tmp (img_path, readonly=True)
    if not tarball_path and tarball_dir:
        fs_type = get_partition_fs_type (mount_point=mount_point)
        tarball_name = "%s_fs_%s.tar.gz" % (os.path.basename (img_path), fs_type)
        tarball_path = os.path.join (tarball_dir, tarball_name)
        if os.path.exists (tarball_path):
            raise Exception ("file %s already exists" % (tarball_path))
        
    cwd = os.getcwd ()
    os.chdir (mount_point)
    try:
        call_cmd ("tar zcf %s ." % (tarball_path))
    finally:
        os.chdir (cwd)
        umount_tmp (mount_point)
    return tarball_path

def get_fs_from_tarball_name (tarball_path):
    om = re.match (r"^.*?fs[_\-](\w+).*?$", os.path.basename (tarball_path))
    if not om:
        return None
    fs_type = om.group (1)
    return fs_type

#def check_loop (img_path):
#    "return loop device name matching img_path. return None when not found"
#    _out = subprocess.check_output (["losetup", "-a"])
#    lines = _out.split ("\n")
#    time.sleep (1)
#    for line in lines:
#        if line.find (img_path) != -1:
#            om = re.match (r"^(/dev/loop\d+):.*$", line)
#            if om:
#                return om.group (1)
#    return None
#
#
#def setup_loop (img_path):
#    """ return loop device filename """
#    img_path = os.path.abspath (img_path)
#    lo_dev = check_loop (img_path)
#    if lo_dev:
#        raise Exception ("img has already been mounted as %s" % (lo_dev))
#
#    call_cmd ("losetup -f %s" % (img_path))
#    lo_dev = check_loop (img_path)
#    assert lo_dev
#    return lo_dev
#
#def teardown_loop (lo_dev):
#    call_cmd ("losetup -d %s" % (lo_dev))


if __name__ == '__main__':
    import unittest

    class TestVPSCommon (unittest.TestCase):

        def test_fs_from_tarball_name (self):
            self.assertEqual (get_fs_from_tarball_name ("/vps/ubuntu-11.10-amd64-fs-ext4.tar.gz"), "ext4")
            self.assertEqual (get_fs_from_tarball_name ("ubuntu_11.10_amd64_fs_ext4.tar.gz"), "ext4")
            self.assertEqual (get_fs_from_tarball_name ("ubuntu_11.10_amd64.tar.gz"), None)

    unittest.main ()
