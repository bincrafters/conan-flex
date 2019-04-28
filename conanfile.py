# -*- coding: utf-8 -*-

from conanfile_base import ConanfileBase
from conans import tools


class Conanfile(ConanfileBase):
    name = ConanfileBase.name
    version = ConanfileBase.version
    exports = ConanfileBase.exports + ["conanfile_base.py"]

    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {'shared': False, "fPIC": True}

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
