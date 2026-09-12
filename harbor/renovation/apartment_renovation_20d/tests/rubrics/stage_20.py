from .checks import stage_check, stage_tool_evidence

def artifact(ctx): return stage_check(ctx,20)
def tools(ctx): return stage_tool_evidence(ctx,20)

CHECKS=[("apt_s20_artifact",artifact,3.5),("apt_s20_tool_evidence",tools,0.5)]
