from .checks import stage_check, stage_tool_evidence

def artifact(ctx): return stage_check(ctx,11)
def tools(ctx): return stage_tool_evidence(ctx,11)

CHECKS=[("apt_s11_artifact",artifact,3.5),("apt_s11_tool_evidence",tools,0.5)]
