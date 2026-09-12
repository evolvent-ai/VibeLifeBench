from .checks import stage_check, stage_tool_evidence

def artifact(ctx): return stage_check(ctx,7)
def tools(ctx): return stage_tool_evidence(ctx,7)

CHECKS=[("apt_s7_artifact",artifact,3.5),("apt_s7_tool_evidence",tools,0.5)]
