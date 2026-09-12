from .checks import stage_check, stage_tool_evidence

def artifact(ctx): return stage_check(ctx,0)
def tools(ctx): return stage_tool_evidence(ctx,0)

CHECKS=[("apt_s0_artifact",artifact,3.5),("apt_s0_tool_evidence",tools,0.5)]
