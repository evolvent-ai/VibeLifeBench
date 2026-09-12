from .checks import stage_check, stage_tool_evidence

def artifact(ctx): return stage_check(ctx,4)
def tools(ctx): return stage_tool_evidence(ctx,4)

CHECKS=[("apt_s4_artifact",artifact,3.5),("apt_s4_tool_evidence",tools,0.5)]
