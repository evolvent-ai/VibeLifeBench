from .checks import stage_check, stage_tool_evidence

def artifact(ctx): return stage_check(ctx,12)
def tools(ctx): return stage_tool_evidence(ctx,12)

CHECKS=[("apt_s12_artifact",artifact,3.5),("apt_s12_tool_evidence",tools,0.5)]
