#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import glob
from conans import ConanFile, AutoToolsBuildEnvironment, tools


class FlexConan(ConanFile):
    name = "flex"
    version = "2.6.4"
    url = "https://github.com/bincrafters/conan-flex"
    homepage = "https://github.com/westes/flex"
    description = "Flex, the fast lexical analyzer generator"
    topics = ("conan", "flex", "lex", "lexer", "lexical analyzer generator")
    license = "BSD-2-Clause"
    author = "Bincrafters <bincrafters@gmail.com>"
    exports = ["LICENSE.md"]
    exports_sources = ["patches/*.patch"]
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {'shared': False, "fPIC": True }
    _source_subfolder = "source_subfolder"

    def source(self):
        source_url = "https://github.com/westes/flex"
        tools.get("{0}/releases/download/v{1}/{2}-{3}.tar.gz".format(source_url, self.version,self.name, self.version),
                  sha256="e87aae032bf07c26f85ac0ed3250998c37621d95f8bd748b31f15b33c45ee995")
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, self._source_subfolder)

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        del self.settings.compiler.libcxx

    def requirements(self):
        if tools.os_info.is_windows:
            self.requires("pcre2/10.32@bincrafters/stable")

    def build(self):
        for filename in sorted(glob.glob("patches/*.patch")):
            self.output.info('applying patch "%s"' % filename)
            tools.patch(base_path=self._source_subfolder, patch_file=filename)

        env_build = AutoToolsBuildEnvironment(self, win_bash=tools.os_info.is_windows)
        configure_args = ["--disable-nls"]
        if self.options.shared:
            configure_args.extend(["--enable-shared", "--disable-static"])
        else:
            configure_args.extend(["--disable-shared", "--enable-shared"])

        if str(self.settings.compiler) == "gcc" and float(str(self.settings.compiler.version)) >= 6:
            configure_args.append("ac_cv_func_reallocarray=no")
        with tools.chdir(self._source_subfolder):
            if tools.os_info.is_windows:
                tools.save("regex.h", "#define PCRE2_CODE_UNIT_WIDTH 8\n#include <pcre2posix.h>")
                if not os.path.isdir("sys"):
                    os.makedirs("sys")
                tools.download("https://raw.githubusercontent.com/win32ports/sys_wait_h/master/sys/wait.h", os.path.join("sys", "wait.h"))
                env_build.include_paths.append(os.getcwd())
            if tools.cross_building(self.settings):
                # stage1flex must be built on native arch: https://github.com/westes/flex/issues/78
                self.run("./configure %s" % " ".join(configure_args))
                env_build.make(args=["-C", "src", "stage1flex"])
                self.run("mv src/stage1flex src/stage1flex.build")
                env_build.make(args=["distclean"])
                with tools.environment_append(env_build.vars):
                    env_build.configure(args=configure_args)
                    cpu_count_option = "-j%s" % tools.cpu_count()
                    self.run("make -C src %s || true" % cpu_count_option)
                    self.run("mv src/stage1flex.build src/stage1flex")
                    self.run("touch src/stage1flex")
                    env_build.make(args=["-C", "src"])
            else:
                with tools.environment_append(env_build.vars):
                    env_build.configure(args=configure_args)
                    env_build.make()
            env_build.make(args=["install"])

    def package(self):
        self.copy(pattern="COPYING", dst="licenses", src=self._source_subfolder)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        self.env_info.PATH.append(os.path.join(self.package_folder, "bin"))
