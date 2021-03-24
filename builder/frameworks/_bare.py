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

#
# Default flags for bare-metal programming (without any framework layers)
#

from SCons.Script import DefaultEnvironment

env = DefaultEnvironment()
board_config = env.BoardConfig()

env.Append(
    ASFLAGS=[
        "-x", "assembler-with-cpp"
    ],
    CCFLAGS=[
        "-Os",
        "-fdata-sections",
        "-ffunction-sections",
        "-march=%s" % board_config.get("build.march"),
    ],
    CPPDEFINES=[
        "__riscv__",
        "__pulp__"
    ],
    LINKFLAGS=[
        "-march=%s" % board_config.get("build.march"),
        "-nostartfiles"
    ],
    LIBS=["gcc"],
)

env.Append(ASFLAGS=env.get("CCFLAGS", [])[:])
