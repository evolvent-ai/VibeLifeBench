from .checks import stage_check, stage_tool_evidence

def artifact(ctx): return stage_check(ctx,8)
def tools(ctx): return stage_tool_evidence(ctx,8)

CHECKS=[("apt_s8_artifact",artifact,3.5),("apt_s8_tool_evidence",tools,0.5)]
