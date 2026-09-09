from pointsgained.ingest.panel_text import parse_shot_line


def test_pct_with_arrow_separate():
    assert parse_shot_line(["Draw", "↺", "100%"]) == ("Draw", "ccw", "100%", 100.0, "pct")


def test_pct_with_arrow_glued():
    assert parse_shot_line(["Double", "Take-out", "↻100%"]) == ("Double Take-out", "cw", "100%", 100.0, "pct")


def test_four_scale_joined_and_split():
    assert parse_shot_line(["Front", "Out4"]) == ("Front", "out", "Out4", 100.0, "four")
    assert parse_shot_line(["Draw", "In", "0"]) == ("Draw", "in", "0", 0.0, "four")


def test_takeout_normalised():
    assert parse_shot_line(["Promotion", "Takeout", "Out0"])[0] == "Promotion Take-out"


def test_not_considered():
    st, turn, raw, pct, scale = parse_shot_line(["Through", "-", "-"])
    assert st == "Through" and pct is None


def test_end_header_conceded():
    from pointsgained.ingest.panel_text import PageHeader, _parse_end_header
    toks = "End 10 CAN - Canada 3 + X (this end) = 3 SWE - Sweden 6 + X (this end) = 6".split()
    ws = [{"text": t, "x0": 10.0 * i, "top": 150.0} for i, t in enumerate(toks)]
    h = PageHeader(); _parse_end_header(ws, h)
    assert h.end_number == 10 and [t.code for t in h.teams] == ["CAN", "SWE"]
    assert h.teams[0].score_before == 3 and h.teams[0].score_this_end is None and h.teams[0].conceded
    assert h.teams[1].score_after == 6


def test_end_header_normal():
    from pointsgained.ingest.panel_text import PageHeader, _parse_end_header
    toks = "End 3 SWE - Sweden 2 + 2 (this end) = 4 CAN - Canada 1 + 0 (this end) = 1".split()
    ws = [{"text": t, "x0": 10.0 * i, "top": 150.0} for i, t in enumerate(toks)]
    h = PageHeader(); _parse_end_header(ws, h)
    assert (h.teams[0].score_before, h.teams[0].score_this_end, h.teams[0].score_after) == (2, 2, 4)
    assert (h.teams[1].score_before, h.teams[1].score_this_end, h.teams[1].score_after) == (1, 0, 1)


def test_end_header_2014_layout():
    from pointsgained.ingest.panel_text import PageHeader, _parse_end_header
    toks = "SWE - Sweden 0 + 0 NOR - Norway 1 + 1 End 2".split()
    ws = [{"text": t, "x0": 10.0 * i, "top": 151.0} for i, t in enumerate(toks)]
    h = PageHeader(); _parse_end_header(ws, h)
    assert h.end_number == 2 and h.teams[1].code == "NOR" and h.teams[1].score_this_end == 1 and h.teams[1].score_after == 2


def test_end_header_glued_plus():
    from pointsgained.ingest.panel_text import PageHeader, _parse_end_header
    toks = "End 7 NOR - Norway 3 + 1 (this end) = 4 CAN - Canada 11+ 0 (this end) = 11".split()
    ws = [{"text": t, "x0": 10.0 * i, "top": 150.0} for i, t in enumerate(toks)]
    h = PageHeader(); _parse_end_header(ws, h)
    assert (h.teams[1].score_before, h.teams[1].score_this_end, h.teams[1].score_after) == (11, 0, 11)


def test_end_header_2017_glued():
    from pointsgained.ingest.panel_text import PageHeader, _parse_end_header
    toks = ["End1", "CAN-Canada", "0+0(this", "end)=0", "SWE-Sweden", "1+2(this", "end)=3"]
    ws = [{"text": t, "x0": 10.0 * i, "top": 150.0} for i, t in enumerate(toks)]
    h = PageHeader(); _parse_end_header(ws, h)
    assert h.end_number == 1 and [t.code for t in h.teams] == ["CAN", "SWE"]
    assert (h.teams[1].score_before, h.teams[1].score_this_end, h.teams[1].score_after) == (1, 2, 3)
    assert h.teams[0].name == "Canada"
