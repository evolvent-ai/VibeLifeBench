from .checks import stage_check, stage_tool_evidence

def artifact(ctx): return stage_check(ctx,17)
def tools(ctx): return stage_tool_evidence(ctx,17)

CHECKS=[("apt_s17_artifact",artifact,3.5),("apt_s17_tool_evidence",tools,0.5)]
