from .checks import stage_check, stage_tool_evidence

def artifact(ctx): return stage_check(ctx,1)
def tools(ctx): return stage_tool_evidence(ctx,1)

CHECKS=[("apt_s1_artifact",artifact,3.5),("apt_s1_tool_evidence",tools,0.5)]
