from .checks import stage_check, stage_tool_evidence

def artifact(ctx): return stage_check(ctx,5)
def tools(ctx): return stage_tool_evidence(ctx,5)

CHECKS=[("apt_s5_artifact",artifact,3.5),("apt_s5_tool_evidence",tools,0.5)]
