from .checks import stage_check, stage_tool_evidence

def artifact(ctx): return stage_check(ctx,18)
def tools(ctx): return stage_tool_evidence(ctx,18)

CHECKS=[("apt_s18_artifact",artifact,3.5),("apt_s18_tool_evidence",tools,0.5)]
