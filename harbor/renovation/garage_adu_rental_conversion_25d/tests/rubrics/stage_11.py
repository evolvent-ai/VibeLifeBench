from ._helpers import material_spec_recorded, trace_stage


def s11_material_spec_check(env) -> bool:
    # HARDENING: was `trace_stage AND text_stage([egress/alarm/insulation/vent])`.
    # This stage is genuine spec-vetting (before any order is placed at s12), so
    # per manual §6.1(b) we tie it to a DURABLE ledger row that must enumerate the
    # code-relevant material classes with their return/spec notes in materials_log
    # (an actual persisted comparison table), not a transient response keyword.
    # Weight trimmed 1.2 -> 1.0 so the real backend order check (s12/cross) carries
    # the material weight. Two-valued: False if materials_log does not enumerate
    # the egress/alarm/insulation/exhaust classes with a spec/return note.
    return trace_stage(env, 11) and material_spec_recorded(env)


CHECKS = [
    ("s11_material_spec_check", s11_material_spec_check, 1.0),
]
