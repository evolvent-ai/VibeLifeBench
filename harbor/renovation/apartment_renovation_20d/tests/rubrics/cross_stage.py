from .checks import cross_files_current,cross_budget_guard,cross_gate_sequence
CHECKS=[("apt_cross_files",cross_files_current,5.0),("apt_cross_budget",cross_budget_guard,5.0),("apt_cross_gates",cross_gate_sequence,6.0)]
