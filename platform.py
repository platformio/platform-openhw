# Copyright 2014-present PlatformIO <contact@platformio.org>
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

import os
import sys

from platformio.public import PlatformBase

IS_WINDOWS = sys.platform.startswith("win")

class OpenhwPlatform(PlatformBase):

    def get_boards(self, id_=None):
        result = super().get_boards(id_)
        if not result:
            return result
        if id_:
            return self._add_default_debug_tools(result)
        else:
            for key in result:
                result[key] = self._add_default_debug_tools(result[key])
        return result

    def _add_default_debug_tools(self, board):
        debug = board.manifest.get("debug", {})
        if "tools" not in debug:
            debug["tools"] = {}

        tools = (
            "digilent-hs1",
            "digilent-hs2",
            "olimex-arm-usb-tiny-h",
            "olimex-arm-usb-ocd-h",
            "olimex-arm-usb-ocd",
            "olimex-jtag-tiny",
            "ovpsim",
            "renode"
        )
        for tool in tools:
            if tool in debug["tools"]:
                continue

            if tool == "ovpsim":
                debug["tools"][tool] = {
                    "init_cmds": [
                        "define pio_reset_halt_target",
                        "end",
                        "define pio_reset_run_target",
                        "end",
                        "set mem inaccessible-by-default off",
                        "set arch riscv:rv32",
                        "set remotetimeout 250",
                        "target extended-remote $DEBUG_PORT",
                        "$INIT_BREAK",
                        "$LOAD_CMDS",
                    ],
                    "server": {
                        "package": "tool-ovpsim-corev",
                        "arguments": [
                            "--variant", "CV32E40P",
                            "--port", "3333",
                            "--program",
                            "$PROG_PATH"
                        ],
                        "executable": "riscvOVPsimCOREV"
                    }
                }

            elif tool == "renode":
                debug["tools"][tool] = {
                    "server": {
                        "package": "tool-renode",
                        "arguments": [
                            "--disable-xwt",
                            "-e", "include @%s" % os.path.join(
                                self.get_dir(), "misc", "renode", "openhw_cv32e40p.resc"),
                            "-e", "machine StartGdbServer 3333 True"
                        ],
                        "ready_pattern": "GDB server with all CPUs started on port",
                        "executable": ("bin/Renode.exe" if IS_WINDOWS else "renode")
                    }
                }

            else:
                debug["tools"][tool] = {
                    "init_cmds": [
                        "define pio_reset_halt_target",
                        "   load",
                        "   monitor reset halt",
                        "end",
                        "define pio_reset_run_target",
                        "   load",
                        "   monitor reset",
                        "end",
                        "set mem inaccessible-by-default off",
                        "set arch riscv:rv32",
                        "set remotetimeout 250",
                        "target extended-remote $DEBUG_PORT",
                        "$INIT_BREAK",
                        "$LOAD_CMDS",
                    ],
                    "server": {
                        "package": "tool-openocd-riscv-pulp",
                        "executable": "bin/openocd",
                        "arguments": [
                            "-s",
                            os.path.join(self.get_dir(), "misc", "openocd"),
                            "-s",
                            "$PACKAGE_DIR/share/openocd/scripts",
                            "-f",
                            ("digilent-hs2.cfg" if tool == "digilent-hs2" else ("interface/ftdi/%s.cfg" % tool)),
                            "-f",
                            "cv32e40p_nexys.cfg",
                        ]
                    },
                    "onboard": tool in debug.get("onboard_tools", []),
                }

        board.manifest["debug"] = debug
        return board
