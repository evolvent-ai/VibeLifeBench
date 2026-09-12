from .checks import stage_check, stage_tool_evidence

def artifact(ctx): return stage_check(ctx,6)
def tools(ctx): return stage_tool_evidence(ctx,6)

CHECKS=[("apt_s6_artifact",artifact,3.5),("apt_s6_tool_evidence",tools,0.5)]
