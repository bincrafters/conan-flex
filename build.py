#!/usr/bin/env python
# -*- coding: utf-8 -*-


from bincrafters import build_template_default, build_template_installer, build_shared
import os

if __name__ == "__main__":
    if "CONAN_CONANFILE" in os.environ and os.environ["CONAN_CONANFILE"] == "conanfile_installer.py":
        arch = os.environ["ARCH"]
        build_requires = dict()
        if "MINGW_CONFIGURATIONS" in os.environ:
            build_requires = {"*": ["mingw_installer/1.0@conan/stable"]}
        builder = build_template_installer.get_builder()
        builder.add({"os": build_shared.get_os(), "arch_build": arch, "arch": arch}, {}, {}, build_requires)
        builder.run()
    else:
        builder = build_template_default.get_builder(pure_c=True)
        builder.run()
