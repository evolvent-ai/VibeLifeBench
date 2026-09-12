from .checks import stage_check, stage_tool_evidence

def artifact(ctx): return stage_check(ctx,14)
def tools(ctx): return stage_tool_evidence(ctx,14)

CHECKS=[("apt_s14_artifact",artifact,3.5),("apt_s14_tool_evidence",tools,0.5)]
