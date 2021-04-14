# Copyright 2014-present PIO Plus <contact@pioplus.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
PULP SDK

Runtime Environment for Parallel Ultra Low Power platform

https://github.com/pulp-platform/pulp-runtime
"""

import os

from SCons.Script import DefaultEnvironment

env = DefaultEnvironment()
platform = env.PioPlatform()

RUNTIME_DIR = platform.get_package_dir("framework-pulp-runtime")
assert os.path.isdir(RUNTIME_DIR)

board_config = env.BoardConfig()

env.SConscript("_bare.py")

env.Append(
    ASFLAGS=["-DLANGUAGE_ASSEMBLY"],

    CCFLAGS=[
        "-include", "chips/pulpissimo/config.h",
        "-fno-jump-tables",
        "-fno-tree-loop-distribute-patterns",
        "-U__riscv__"
    ],

    CPPDEFINES=[
        "RV_ISA_RV32",
        ("__PLATFORM__", "ARCHI_PLATFORM_FPGA"),
        ("CONFIG_IO_UART", 0),
        ("CONFIG_IO_UART_BAUDRATE", 115200),
        ("CONFIG_IO_UART_ITF", 0)
    ],

    CPPPATH=[
        os.path.join(RUNTIME_DIR, "include", "chips", "pulpissimo"),
        os.path.join(RUNTIME_DIR, "lib", "libc", "minimal", "include"),
        os.path.join(RUNTIME_DIR, "include"),
        os.path.join(RUNTIME_DIR, "kernel"),
    ]
)

env.AppendUnique(ASFLAGS=env.get("CCFLAGS", [])[:])

if not board_config.get("build.ldscript", ""):
    env.Append(
        LIBPATH=[os.path.join(RUNTIME_DIR, "kernel", "chips", "pulpissimo")]
    )
    env.Replace(LDSCRIPT_PATH="link.ld")

libs = []

libs.append(
    env.BuildLibrary(
        os.path.join("$BUILD_DIR", "kernel"),
        os.path.join(RUNTIME_DIR, "kernel"),
        src_filter=[
            "+<*>",
            "-<cluster.c>",
            "-<chips/>",
            "+<chips/pulpissimo>",
        ],
    )
)

libs.append(
    env.BuildLibrary(
        os.path.join("$BUILD_DIR", "drivers"),
        os.path.join(RUNTIME_DIR, "drivers")
    )
)

libs.append(
    env.BuildLibrary(
        os.path.join("$BUILD_DIR", "lib", "libc", "minimal"),
        os.path.join(RUNTIME_DIR, "lib")
    )
)

env.Append(LIBS=libs)
