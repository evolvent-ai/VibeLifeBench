from .checks import stage_check, stage_tool_evidence

def artifact(ctx): return stage_check(ctx,9)
def tools(ctx): return stage_tool_evidence(ctx,9)

CHECKS=[("apt_s9_artifact",artifact,3.5),("apt_s9_tool_evidence",tools,0.5)]
