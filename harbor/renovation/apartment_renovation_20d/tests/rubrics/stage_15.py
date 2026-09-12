from .checks import stage_check, stage_tool_evidence

def artifact(ctx): return stage_check(ctx,15)
def tools(ctx): return stage_tool_evidence(ctx,15)

CHECKS=[("apt_s15_artifact",artifact,3.5),("apt_s15_tool_evidence",tools,0.5)]
