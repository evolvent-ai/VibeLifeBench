from ._helpers import durable_workspace, trace_stage


def s11_material_spec_check(env) -> bool:
    # HARDENING: was `trace_stage AND text_stage([egress/alarm/insulation/vent])`.
    # This stage is genuine spec-vetting (before any order is placed at s12), so
    # per manual §6.1(b) we tie it to a DURABLE ledger row that must enumerate the
    # code-relevant material classes with their return/spec notes in materials_log
    # (an actual persisted comparison table), not a transient response keyword.
    # Weight trimmed 1.2 -> 1.0 so the real backend order check (s12/cross) carries
    # the material weight. Two-valued: False if materials_log does not enumerate
    # the egress/alarm/insulation/exhaust classes with a spec/return note.
    return (
        trace_stage(env, 11)
        and durable_workspace(env, [["materials_log"], ["egress", "逃生窗"], ["alarm", "报警", "一氧化碳", "烟感"], ["insulation", "保温"], ["exhaust", "排风", "ventilation", "通风"], ["return", "可退", "spec", "规格", "库存", "stock"]])
    )


CHECKS = [
    ("s11_material_spec_check", s11_material_spec_check, 1.0),
]
