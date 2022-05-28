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

Software Development Kit for Parallel Ultra Low Power platform

https://github.com/pulp-platform/pulp-sdk
"""

import os

from SCons.Script import DefaultEnvironment

env = DefaultEnvironment()
platform = env.PioPlatform()

SDK_DIR = platform.get_package_dir("framework-pulp-sdk")
RT_DIR = os.path.join(SDK_DIR, "runtime", "pulp-rt")
assert os.path.isdir(SDK_DIR)
assert os.path.isdir(RT_DIR)

board_config = env.BoardConfig()

try:
    import prettytable
except ImportError:
    env.Execute(
        env.VerboseAction(
            "$PYTHONEXE -m pip install prettytable",
            "Installing Python dependencies",
        )
    )


def generate_config(
    output_dir, configs=None, libs=None, properties=None, extra_args=None
):
    if os.path.isfile(os.path.join(env.subst(output_dir), "config.mk")):
        return None
    if not configs:
        configs = []
    if not libs:
        libs = []
    if not properties:
        properties = []

    cmd = [
        '"$PYTHONEXE"',
        os.path.join(SDK_DIR, "pulp-tools", "bin", "plpflags"),
        "gen",
        "--input=pulpissimo@config_file=chips/pulpissimo/pulpissimo.json",
        "--output-dir=" + output_dir,
        "--makefile=%s/config.mk" % output_dir,
    ]

    cmd.extend(
        ["--config=" + c for c in ["platform=fpga", "**/rt/type=pulp-rt"] + configs]
    )
    cmd.extend(["--property=" + p for p in properties])
    cmd.extend(["--lib=" + lib for lib in libs])
    if extra_args:
        cmd.extend(extra_args)

    return env.VerboseAction(
        " ".join(cmd),
        "Generating configuration for %s" % os.path.basename(output_dir),
    )


def generate_sdk_config(output_dir):
    skd_properties = (
        "fc/archi",
        "pe/archi",
        "pulp_chip",
        "pulp_chip_family",
        "cluster/version",
        "host/archi",
        "fc_itc/version",
        "udma/hyper/version",
        "udma/cpi/version",
        "udma/i2c/version",
        "soc/fll/version",
        "udma/i2s/version",
        "udma/uart/version",
        "event_unit/version",
        "perf_counters",
        "fll/version",
        "soc/spi_master",
        "soc/apb_uart",
        "padframe/version",
        "udma/spim/version",
        "gpio/version",
        "udma/archi",
        "udma/version",
        "soc_eu/version",
        "compiler",
        "rtc/version",
        "udma/mram/version",
    )

    skd_libs = (
        "rt",
        "omp",
        "rtio",
        "bench",
    )

    return generate_config(output_dir, libs=skd_libs, properties=skd_properties)


def generate_app_config(output_dir):
    return generate_config(
        output_dir,
        configs=["rt/start-all=true", "**/rt/fc-start=true"],
        extra_args=["--app=" + os.path.basename(env.subst("$PROJECT_DIR"))],
    )


env.SConscript("_bare.py")

env.Append(
    ASPPFLAGS=["-DLANGUAGE_ASSEMBLY"],
    CCFLAGS=[
        "-Wall",
        "-Wextra",
        "-Werror",
        "-Wno-unused-parameter",
        "-Wno-unused-function",
        "-Wno-unused-variable",
        "-Wundef",
        "-fno-jump-tables",
        "-fno-tree-loop-distribute-patterns",
        ("-include", os.path.join("$BUILD_DIR", "configs", "sdk", "fc_config.h")),
    ],
    CPPDEFINES=[
        ("__RT_USE_IO", 1),
        ("__RT_USE_ASSERT", 1),
        ("__RT_USE_BRIDGE", 1),
        ("__RT_USE_WARNING", 1),
        ("CONFIG_CHECK_CLUSTER_START", 1),
        ("CONFIG_PADS_ENABLED", 1),
        ("__RT_UDMA_COPY_ASM", 1),
        ("__RT_I2C_COPY_ASM", 1),
        ("__RT_SPIM_COPY_ASM", 1),
        "RT_CONFIG_RTC_ENABLED",
        "RT_CONFIG_GPIO_ENABLED",
    ],
    CPPPATH=[
        os.path.join(RT_DIR, "kernel"),
        os.path.join(RT_DIR, "include"),
        os.path.join(SDK_DIR, "runtime", "hal", "include"),
        os.path.join(SDK_DIR, "runtime", "archi", "include"),
        os.path.join(SDK_DIR, "runtime", "pmsis_api", "include"),
        os.path.join(SDK_DIR, "tools", "pulp-debug-bridge", "include"),
        os.path.join(RT_DIR, "include", "io"),
    ],
    LINKFLAGS=[
        "-nostartfiles",
        "-nostdlib",
        "-Wl,--gc-sections",
        "-mfdiv",
        "-D__riscv__",
    ],
)

if not board_config.get("build.ldscript", ""):
    env.Append(LIBPATH=[os.path.join(RT_DIR, "rules", "pulpissimo")])
    env.Replace(LDSCRIPT_PATH="link.ld")


disabled_drivers = (
    "gpio",
    "hyper",
    "pwm",
    "udma/udma-v2.c",
    "udma/udma-v2_asm.S",
    "spi/spim-v2.c",
    "spi/spim-v2_asm.S",
)

disabled_kernel_parts = (
    "gap",
    "gap9",
    "oprecompkw",
    "or1k",
    "riscv/pe-eu-v1-entry.c",
    "riscv/pe-eu-v1.S",
    "riscv/pe-eu-v3.S",
    "riscv/soc_event_eu.S",
    "riscv/soc_event_itc-v1.S",
    "riscv/soc_event_itc-v3.S",
    "riscv/udma-v2.S",
    "riscv/udma_spim-v2.S",
    "riscv/udma_mram-v1.S",
    "riscv/task.S",
    "usoc_v1",
    "vega",
    "vivosoc3",
    "wolfe",
    "cluster_call.c",
    "fll-v0.c",
    "task.c",
    "freq-v0.c",
    "periph-v1.c",
    "periph-v2.c",
    "sync_mc.c",
)

libs = [
    env.BuildLibrary(
        os.path.join("$BUILD_DIR", "io"), os.path.join(RT_DIR, "libs", "io")
    ),
    env.BuildLibrary(
        os.path.join("$BUILD_DIR", "rt"),
        os.path.join(RT_DIR),
        src_filter=[
            "+<*>",
            "-<libs>",
            "-<*deprecated*>",
            "+<drivers_deprecated/pads/pads-v1.c>",
            "+<drivers_deprecated/pads/i2c-v2.c>",
            "+<drivers_deprecated/uart/uart.c>",
            "+<drivers_deprecated/spim/spim-v3.c>",
            "+<drivers_deprecated/gpio/gpio-v3.c>",
        ]
        + ["-<drivers/%s>" % d for d in disabled_drivers]
        + ["-<kernel/%s>" % k for k in disabled_kernel_parts],
    ),
]

env.Append(
    PIOBUILDFILES=[
        os.path.join("$BUILD_DIR", "configs", "app", f)
        for f in ("rt_pad_conf.c", "rt_conf.c")
    ]
)

env.Append(LIBS=libs)

# Add extra Python modules
pulp_tools = ("pulp-configs", "json-tools")
envsafe = env.Clone()
envsafe["ENV"]["PYTHONPATH"] = os.pathsep.join(
    [os.path.join(SDK_DIR, m, "python") for m in pulp_tools]
    + [envsafe["ENV"].get("PYTHONPATH", "")]
)

envsafe["ENV"]["BUILDER_CONFIGS_PATH"] = os.path.join(
    SDK_DIR, "pulp-configs", "configs"
)
envsafe["ENV"]["PULP_SDK_INSTALL"] = SDK_DIR


for command in (
    generate_app_config(os.path.join("$BUILD_DIR", "configs", "app")),
    generate_sdk_config(os.path.join("$BUILD_DIR", "configs", "sdk")),
):
    if command:
        envsafe.Execute(command)
