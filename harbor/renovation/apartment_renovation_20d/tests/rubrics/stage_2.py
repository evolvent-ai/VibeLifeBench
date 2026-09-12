from .checks import stage_check, stage_tool_evidence

def artifact(ctx): return stage_check(ctx,2)
def tools(ctx): return stage_tool_evidence(ctx,2)

CHECKS=[("apt_s2_artifact",artifact,3.5),("apt_s2_tool_evidence",tools,0.5)]
