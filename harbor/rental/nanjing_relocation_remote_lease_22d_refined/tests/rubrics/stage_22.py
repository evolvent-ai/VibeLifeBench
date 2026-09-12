"""Stage 22 — final answer: single verified target, exact money and principal sequence."""
from __future__ import annotations
from ._helpers import BAIT_LISTING, TARGET_COMMUNITY, count_any, file_has, has_any, has_regex, persisted_corpus, stage_response_text


def s22_final_handoff_answer(env) -> bool:
    text = stage_response_text(env, 22) + '\n' + persisted_corpus(env)
    names_target = has_any(text, [TARGET_COMMUNITY, 'Mingfa'])
    why = count_any(text, ['ownership', 'account name', 'commute', 'reputation', 'verification', 'market price', 'agency fee', 'status', 'budget']) >= 5
    todo = has_any(text, ['principal', 'Gu Feng', 'by you', 'you personally', 'personally'])
    durable = file_has(env, 'handoff.md', ['Mingfa', 'principal', 'transfer', 'lease signing'], minimum=4)
    no_bait = not has_regex(text, '(recommend|final|select|choose).{0,16}(Top-of-the-Hill Street Xinyuan|' + BAIT_LISTING + ')')
    return names_target and why and todo and durable and no_bait


def s22_final_exact_money_and_sequence(env) -> bool:
    text = stage_response_text(env, 22) + '\n' + persisted_corpus(env)
    has_target = has_any(text, [TARGET_COMMUNITY, 'Gu Jianguo'])
    money = all(has_any(text, forms) for forms in (
        ('4080', '4,080'), ('12240', '12,240'), ('3880', '3,880'), ('20200', '20,200')
    ))
    sequence = has_regex(text, '(first|on-site|verification).{0,24}(property certificate|contract).{0,48}(then|after).{0,24}(transfer|payment|sign|lease signing)')
    principal = has_any(text, ['principal', 'personally', 'by you', 'you personally'])
    durable = file_has(env, 'handoff.md', ['4080', '12240', '3880', '20200', 'Gu Jianguo'], minimum=5)
    return has_target and money and sequence and principal and durable

CHECKS = [('s22_final_handoff_answer', s22_final_handoff_answer, 0.1863799283154122), ('s22_final_exact_money_and_sequence', s22_final_exact_money_and_sequence, 3.727598566308244)]
