# -*- coding: utf-8 -*-

import os
import shutil
from conanfile_base import ConanFileBase


class ConanFileInstaller(ConanFileBase):
    name = ConanFileBase._base_name + "_installer"
    version = ConanFileBase.version
    exports = ConanFileBase.exports + ["conanfile_base.py"]

    settings = "os_build", "arch_build", "compiler", "arch"

    def package_id(self):
        del self.info.settings.compiler
        del self.info.settings.arch

    def package_info(self):
        bindir = os.path.join(self.package_folder, "bin")
        self.output.info('Appending PATH environment variable: {}'.format(bindir))
        self.env_info.PATH.append(bindir)

    def package(self):
        super(ConanFileInstaller, self).package()
        libdir = os.path.join(self.package_folder, "lib")
        incdir = os.path.join(self.package_folder, "include")
        if os.path.isdir(libdir):
            shutil.rmtree(libdir)
        if os.path.isdir(incdir):
            shutil.rmtree(incdir)
