from .checks import stage_check, stage_tool_evidence

def artifact(ctx): return stage_check(ctx,10)
def tools(ctx): return stage_tool_evidence(ctx,10)

CHECKS=[("apt_s10_artifact",artifact,3.5),("apt_s10_tool_evidence",tools,0.5)]
