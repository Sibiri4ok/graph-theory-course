import drivers.driver as driver
import config

from lib.dataset import Dataset
from lib.algorithm import AlgorithmName
from lib.tool import ToolName
from lib.dataset import DatasetValueType
from lib.util import check_output
from lib.opencl_pick import pick_spla_opencl_platform_device


class DriverSpla(driver.Driver):
    def __init__(self):
        self._opencl_pd = pick_spla_opencl_platform_device()
        super().__init__()

    def can_run_bfs(self, dataset: Dataset) -> bool:
        return dataset.get_element_type() == DatasetValueType.void

    def can_run_sssp(self, dataset: Dataset) -> bool:
        t = dataset.get_element_type()
        return t in (DatasetValueType.float, DatasetValueType.int)

    def can_run_tc(self, dataset: Dataset) -> bool:
        return True

    def can_run_pr(self, dataset: Dataset) -> bool:
        # Как в pr.cpp: строится float-матрица из структуры (степени по pattern).
        return dataset.get_element_type() == DatasetValueType.void

    def _spla_cmd(self, algo: AlgorithmName, dataset: Dataset,
                  num_iterations: int, extra: list) -> list:
        plat, dev = self._opencl_pd
        return [
            str(self.exec_path(algo)),
            f"--mtxpath={dataset.path}",
            f"--niters={num_iterations}",
            f"--platform={plat}",
            f"--device={dev}",
            "--run-cpu=false",
            "--run-ref=false",
            "--run-gpu=true",
        ] + extra

    def run_bfs(self,
                dataset: Dataset,
                source_vertex: int,
                num_iterations: int) -> driver.ExecutionResult:

        output = check_output(self._spla_cmd(
            AlgorithmName.bfs, dataset, num_iterations,
            [f"--source={source_vertex}"],
        ))

        return DriverSpla._parse_output(output)

    def run_sssp(self,
                 dataset: Dataset,
                 source_vertex: int,
                 num_iterations: int) -> driver.ExecutionResult:

        output = check_output(self._spla_cmd(
            AlgorithmName.sssp, dataset, num_iterations,
            [f"--source={source_vertex}"],
        ))

        return DriverSpla._parse_output(output)

    def run_tc(self,
               dataset: Dataset,
               num_iterations: int) -> driver.ExecutionResult:

        output = check_output(self._spla_cmd(
            AlgorithmName.tc, dataset, num_iterations, [],
        ))
        return DriverSpla._parse_output(output)

    def run_pr(self,
               dataset: Dataset,
               _num_iterations: int) -> driver.ExecutionResult:

        niters = config.PR_TRIALS_LAGRAPH_GAPPAGERANK
        output = check_output(self._spla_cmd(
            AlgorithmName.pr, dataset, niters, [],
        ))
        return DriverSpla._parse_output(output)

    def tool_name(self) -> ToolName:
        return ToolName.spla

    @staticmethod
    def _parse_output(output: bytes) -> driver.ExecutionResult:
        text = output.decode("utf-8", errors="replace").replace("\r", "")
        lines = text.split("\n")
        warmup = 0.0
        runs: list = []

        for line in lines:
            if line.startswith("warm-up(ms):"):
                parts = line.split()
                if len(parts) >= 2:
                    warmup = float(parts[1])
            if line.startswith("iters(ms):"):
                runs = [float(v) for v in line.split()[1:] if v]

        if not runs:
            for line in lines:
                if line.startswith("gpu(ms):"):
                    body = line.split(":", 1)[1]
                    runs = [
                        float(x.strip())
                        for x in body.split(",")
                        if x.strip()
                    ]
                    break

        if not runs:
            raise ValueError(
                "Не удалось разобрать вывод Spla (ожидались iters(ms): или gpu(ms):)"
            )

        return driver.ExecutionResult(warmup, runs)
