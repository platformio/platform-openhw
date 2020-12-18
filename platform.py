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

from os.path import join

from platformio.managers.platform import PlatformBase


class OpenhwPlatform(PlatformBase):

    def get_boards(self, id_=None):
        result = PlatformBase.get_boards(self, id_)
        if not result:
            return result
        if id_:
            return self._add_default_debug_tools(result)
        else:
            for key, value in result.items():
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
            "olimex-jtag-tiny"
        )
        for tool in tools:
            if tool in debug["tools"]:
                continue
            server_executable = "bin/openocd"
            server_package = "tool-openocd-riscv-pulp"
            server_args = [
                "-s",
                join(self.get_dir(), "misc", "openocd"),
                "-s",
                "$PACKAGE_DIR/share/openocd/scripts"
            ]
            reset_cmds = [
                "define pio_reset_halt_target",
                "   load",
                "   monitor reset halt",
                "end",
                "define pio_reset_run_target",
                "   load",
                "   monitor reset",
                "end",
            ]

            if tool == "digilent-hs2":
                server_args.extend(["-f", "digilent-hs2.cfg"])
            else:
                # All tools are FTDI based
                server_args.extend(
                    [
                        "-f",
                        "interface/ftdi/%s.cfg" % tool,
                        "-f",
                        "cv32e40p_nexys.cfg",
                    ]
                )

            debug["tools"][tool] = {
                "init_cmds": reset_cmds + [
                    "set mem inaccessible-by-default off",
                    "set arch riscv:rv32",
                    "set remotetimeout 250",
                    "target extended-remote $DEBUG_PORT",
                    "$INIT_BREAK",
                    "$LOAD_CMDS",
                ],
                "server": {
                    "package": server_package,
                    "executable": server_executable,
                    "arguments": server_args,
                },
                "onboard": tool in debug.get("onboard_tools", [])
            }

        board.manifest["debug"] = debug
        return board
