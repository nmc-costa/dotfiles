Gauntlet Loop. Goal: {{goal}}. How to build it is your call.

Bar: {{bar}} ({{bar_access}}). This real thing is the standard, not a checklist. It may be out of reach; aim for it anyway.

Ledger: L = `python3 ~/.agents/skills/gauntlet-prompting/scripts/gauntlet_ledger.py`. Never decide A/B order or when to stop yourself. Run name R = `{{slug}}`. First run `L init R --max-rounds {{max_rounds}}`.

1. Split the goal into pieces that can be improved independently.
2. Each round, per piece: build or revise the candidate, then `L pair R <piece> --candidate <path> --bar <ref>`. Give a critic only the A and B it prints. The critic inspects both real artifacts and answers A or B, plus the largest gap in one sentence. Record it with `L verdict R <piece> <A|B> --reason "<gap>"`, then run `L status R <piece>`.
3. WIN: integrate the piece. CONTINUE: revise using only the critic's gap. STOP_BUDGET or STOP_PLATEAU: stop that piece and report it to the human.
4. Builders never judge their own work. Critics never see builder notes, drafts, or which side is the candidate.

{{delegation_block}}

Finish by reporting each piece's status, the final artifact paths, and `L status R`.{{task_line}}
