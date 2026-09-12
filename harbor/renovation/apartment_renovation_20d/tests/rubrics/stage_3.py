from .checks import stage_check, stage_tool_evidence

def artifact(ctx): return stage_check(ctx,3)
def tools(ctx): return stage_tool_evidence(ctx,3)

CHECKS=[("apt_s3_artifact",artifact,3.5),("apt_s3_tool_evidence",tools,0.5)]
