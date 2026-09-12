from .checks import stage_check, stage_tool_evidence

def artifact(ctx): return stage_check(ctx,21)
def tools(ctx): return stage_tool_evidence(ctx,21)

CHECKS=[("apt_s21_artifact",artifact,3.5),("apt_s21_tool_evidence",tools,0.5)]
