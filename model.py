from typing import NewType, Protocol
from enum import StrEnum

arguments = {	"SEED" 			: "-s",
				"JOBS" 			: "-j",
				"JLIST" 		: "-l",
				"MAXLEN" 		: "-m",
				"POLICY" 		: "-p",
				"QUANTUM"		: "-q",
				"MAXTICKET"		: "-T",
				"NUMQUEUES"		: "-n",
				"ALLOTMENT"		: "-a",
				"QUANTUMLIST" 	: "-Q",
				"ALLOTMENTLIST"	: "-A",
				"MAXIO" 		: "-M",
				"BOOST" 		: "-B",
				"IOTIME" 		: "-i",
				"STAY" 			: "-S",
				"IOBUMP"		: "-I",
				}

class Scheduler(Protocol):
	@property
	def name(self) -> str:
		...

	@property
	def parameters(self) -> list[str]:
		...

class BasicScheduler:
	def __init__(self) -> None:
		self._name = "Basic"
		self._parameters = ["SEED",
							"JOBS",
							"JLIST",
							"MAXLEN",
							"POLICY",				# SJF, FIFO, RR
							"QUANTUM",				# length of time slice for RR policy
							]
	@property
	def name(self) -> str:
		return self._name

	@property
	def parameters(self) -> list[str]:
		return self._parameters

class LotteryScheduler:
	def __init__(self) -> None:
		self._name = "Lottery"
		self._parameters = ["SEED",
							"JOBS",
							"JLIST",
							"MAXLEN",
							"MAXTICKET",			
							"QUANTUM",				# length of time slice
							]
	@property
	def name(self) -> str:
		return self._name

	@property
	def parameters(self) -> list[str]:
		return self._parameters

class MLFQScheduler:
	def __init__(self) -> None:
		self._name = "MLFQ"
		self._parameters = ["SEED",
							"NUMQUEUES",
							"QUANTUM",	
							"ALLOTMENT",
							"QUANTUMLIST",
							"ALLOTMENTLIST",
							"JOBS",
							"MAXLEN",
							"MAXIO",
							"BOOST",
							"IOTIME",
							"STAY",
							"IOBUMP",
							"JLIST",			
							]
	@property
	def name(self) -> str:
		return self._name

	@property
	def parameters(self) -> list[str]:
		return self._parameters

class MultiCPUScheduler:
	def __init__(self) -> None:
		self._name = "temp"
		self._parameters = []
	@property
	def name(self) -> str:
		return self._name

	@property
	def parameters(self) -> list[str]:
		return self._parameters

class SchedulerModel:
	def __init__(self) -> None:
		self._current_scheduler: Scheduler
		self._scheduler_mapping = { "Basic":BasicScheduler(), 
									"Lottery":LotteryScheduler(), 
									"MLFQ":MLFQScheduler(), 
									"Multi-CPU":MultiCPUScheduler()}
		self._param_text_hints = {	"SEED" 			: "42",
									"JOBS" 			: "number of jobs in system",
									"JLIST" 		: "x1,y1,z1:x2,y2,z2:... where x=arrival,y=runtime,z=how often I/O issued",
									"MAXLEN" 		: "max run-time of a job (if randomly generating)",
									"POLICY" 		: "SJF, FIFO, RR",
									"QUANTUM"		: "length of time slice (for RR policy if Basic Scheduler)",
									"MAXTICKET"		: "maximum ticket value, if randomly assigned",
									"NUMQUEUES"		: "number of queues (if not using -QUANTUMLIST)",
									"ALLOTMENT"		: "length of allotment (if not using -ALLOTMENTLIST)",
									"QUANTUMLIST" 	: "x,y,z,... where x=quantum length for the highest priority queue, y the next highest, and so on",
									"ALLOTMENTLIST"	: "x,y,z,... where x=# of time slices for the highest priority queue, y the next highest, and so on",
									"MAXIO" 		: "max I/O frequency of a job (if randomly generating)",
									"BOOST" 		: "how often to boost the priority of all jobs back tohigh priority",
									"IOTIME" 		: "how long an I/O should last",
									"STAY" 			: "True/False: reset and stay at same priority level when issuing I/O",
									"IOBUMP"		: "True/False:  jobs that finished I/O move immediately to front of current queue",}

	@property
	def current_scheduler(self) -> str:
		return self._current_scheduler.name
	@property
	def scheduler_parameters(self) -> list[str]:
		return self._current_scheduler.parameters
	@property
	def param_text_hints(self) -> dict[str,str]:
		return self._param_text_hints

	def change_scheduler(self, new_scheduler:str):
		self._param_text_hints["QUANTUM"] = "length of time slice (for RR policy)" if new_scheduler == "Basic" \
											else "length of time slice" if new_scheduler == "Lottery" \
											else "length of time slice (if not using -QUANTUMLIST)"
		self._current_scheduler = self._scheduler_mapping[new_scheduler]

	def solve(self, cmd:str):
		pass
