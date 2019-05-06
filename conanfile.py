# -*- coding: utf-8 -*-

from conanfile_base import ConanfileBase
from conans import tools
import shutil
import os


class Conanfile(ConanfileBase):
    name = "flex"
    version = ConanfileBase.version
    exports = ConanfileBase.exports + ["conanfile_base.py"]

    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)

    def package(self):
        super(Conanfile, self).package()
        bindir = os.path.join(self.package_folder, "bin")
        if os.path.isdir(bindir):
            shutil.rmtree(bindir)
