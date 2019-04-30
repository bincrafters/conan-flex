import os
import glob
import platform
from conans import ConanFile, AutoToolsBuildEnvironment, tools


class ConanfileBase(ConanFile):
    _base_name = "flex"
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

    _source_subfolder = "source_subfolder"

    def source(self):
        sha256 = "e87aae032bf07c26f85ac0ed3250998c37621d95f8bd748b31f15b33c45ee995"
        tools.get("{0}/releases/download/v{1}/{2}-{3}.tar.gz".format(self.homepage, self.version, self._base_name, self.version), sha256=sha256)
        extracted_dir = self._base_name + "-" + self.version
        os.rename(extracted_dir, self._source_subfolder)

    def configure(self):
        del self.settings.compiler.libcxx

    def requirements(self):
        if tools.os_info.is_windows:
            self.requires("pcre2/10.32@bincrafters/stable")

    def _apply_patches(self):
        for filename in sorted(glob.glob("patches/*.patch")):
            self.output.info('applying patch "%s"' % filename)
            tools.patch(base_path=self._source_subfolder, patch_file=filename)

    @staticmethod
    def detected_os():
        if tools.os_info.is_macos:
            return "Macos"
        if tools.OSInfo().is_windows:
            return "Windows"
        return platform.system()

    @property
    def _the_os(self):
        return self.settings.get_safe("os") or self.settings.get_safe("os_build")

    @property
    def _the_arch(self):
        return self.settings.get_safe("arch") or self.settings.get_safe("arch_build")

    @property
    def cross_building(self):
        if tools.cross_building(self.settings):
            if self._the_os == self.detected_os():
                if self._the_arch == "x86" and tools.detected_architecture() == "x86_64":
                    return False
            return True
        return False

    def build(self):
        if tools.os_info.is_windows:
            self._apply_patches()
        env_build = AutoToolsBuildEnvironment(self, win_bash=tools.os_info.is_windows)
        configure_args = ["--disable-nls"]
        if "shared" in self.options and self.options.shared:
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
            if self.cross_building:
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
