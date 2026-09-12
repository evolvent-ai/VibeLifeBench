from .checks import stage_check, stage_tool_evidence

def artifact(ctx): return stage_check(ctx,13)
def tools(ctx): return stage_tool_evidence(ctx,13)

CHECKS=[("apt_s13_artifact",artifact,3.5),("apt_s13_tool_evidence",tools,0.5)]
