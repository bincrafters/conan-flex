# -*- coding: utf-8 -*-

import os
from conanfile_base import ConanfileBase


class ConanfileInstaller(ConanfileBase):
    name = "flex_installer"
    version = ConanfileBase.version
    exports = ConanfileBase.exports + ["conanfile_base.py"]

    settings = "os_build", "arch_build", "compiler"


    def package_id(self):
        del self.info.settings.compiler

    def package_info(self):
        bindir = os.path.join(self.package_folder, "bin")
        self.output.info('Appending PATH environment variable: {}'.format(bindir))
        self.env_info.PATH.append(bindir)
