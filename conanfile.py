#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from conans import ConanFile, AutoToolsBuildEnvironment, tools


class FlexConan(ConanFile):
    name = "flex"
    version = "2.6.4"
    url = "https://github.com/bincrafters/conan-flex"
    homepage = "https://github.com/westes/flex"
    description = "Flex, the fast lexical analyzer generator"
    license = "https://github.com/westes/flex/blob/master/COPYING"
    author = "Bincrafters <bincrafters@gmail.com>"
    exports_sources = ["LICENSE.md"]
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False]}
    default_options = "shared=False"


    def source(self):
        source_url = "https://github.com/westes/flex"
        tools.get("{0}/releases/download/v{1}/{2}-{3}.tar.gz".format(source_url, self.version,self.name, self.version))
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, "sources")

    def configure(self):
        if self.settings.os == "Windows":
            raise Exception("Flex is not supported on Windows.")

    def build(self):
        env_build = AutoToolsBuildEnvironment(self)
        with tools.environment_append(env_build.vars):
            configure_args = ['--prefix=%s' % self.package_folder]
            configure_args.append("--enable-shared" if self.options.shared else "--disable-shared")
            configure_args.append("--disable-static" if self.options.shared else "--enable-static")
            with tools.chdir("sources"):
                env_build.fpic = True
                env_build.configure(args=configure_args)
                env_build.make(args=["all"])
                env_build.make(args=["install"])

    def package(self):
        with tools.chdir("sources"):
            self.copy(pattern="COPYING", dst="licenses")

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        self.env_info.PATH.append(os.path.join(self.package_folder, "bin"))
