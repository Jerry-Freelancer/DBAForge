import asyncio
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Protocol


@dataclass(frozen=True, slots=True)
class PowerShellResult:
    exit_code: int
    stdout: str
    stderr: str


class PowerShellExecutor(Protocol):
    async def execute_json(self, script: Path, payload: dict[str, Any]) -> PowerShellResult: ...


class SubprocessPowerShellExecutor:
    """Executes a script through pwsh and exchanges only JSON through standard I/O."""

    def __init__(self, executable: str = "pwsh", timeout_seconds: float = 60) -> None:
        self._executable = executable
        self._timeout_seconds = timeout_seconds

    async def execute_json(self, script: Path, payload: dict[str, Any]) -> PowerShellResult:
        process = await asyncio.create_subprocess_exec(
            self._executable,
            "-NoLogo",
            "-NoProfile",
            "-NonInteractive",
            "-File",
            str(script),
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        try:
            stdout, stderr = await asyncio.wait_for(
                process.communicate(json.dumps(payload).encode()), timeout=self._timeout_seconds
            )
        except TimeoutError:
            process.kill()
            await process.wait()
            raise

        return PowerShellResult(
            exit_code=process.returncode or 0,
            stdout=stdout.decode(),
            stderr=stderr.decode(),
        )
