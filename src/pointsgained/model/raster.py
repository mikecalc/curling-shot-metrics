"""Raw-geometry f and g: positions rasterised on the fly and read by a small convolutional network
(design Section 5.2, gates in Section 7.5).

Raster: 1 inch per pixel, x in [-85, 85] (171 columns, sheet width), y from 72 in behind the tee
(back line) to the hog line at 252 in (325 rows), two channels (own = hammer team, opponent), stones
as filled discs of radius 5.7 px; a third channel marks the intent target for g. Scalars (rocks
remaining, next thrower, free-guard-zone rocks, discipline, situation; for g the call, turn,
expected grade and the target descriptors) join at the dense layer. Mirroring is a training-time
augmentation (x -> -x on stones and target), not stored rows.

Requires torch (optional dependency group `geom`); falls back to CPU when MPS is unavailable.
"""
from __future__ import annotations

import logging
import time
from dataclasses import dataclass, field

import numpy as np
import pandas as pd

from ..core.geometry import STONE_RADIUS
from .dataset import Dataset
from .features import FEATURE_NAMES
from .train import column, FEATURE_SETS, design_columns
from .value import N_OUT

log = logging.getLogger(__name__)

X_MIN, X_MAX = -85.0, 85.0
Y_MIN, Y_MAX = -72.0, 252.0
W = int(X_MAX - X_MIN) + 1          # 171
H = int(Y_MAX - Y_MIN) + 1          # 325
MAX_STONES = 16
SCALAR_F = ["rocks_remaining", "next_thrower_has_hammer", "fgz_rocks", "stones_in_play", "is_women",
            "diff_hammer_clip", "ends_remaining_clip", "is_extra_end"]
SCALAR_G_EXTRA = ["turn_code", "expected_grade", "target_owner", "target_ring", "target_is_shot_rock", "target_is_guard"]
N_TYPES = 13


def _torch():
    import torch
    return torch


def device_name() -> str:
    torch = _torch()
    return "mps" if torch.backends.mps.is_available() else "cpu"


# ---- positions as ragged arrays --------------------------------------------------------------

@dataclass
class StoneArrays:
    """Pre-shot positions of the unmirrored rows as padded arrays (n_rows, MAX_STONES)."""
    x: np.ndarray
    y: np.ndarray
    owner: np.ndarray          # 1 own (hammer), 0 opponent
    valid: np.ndarray          # bool mask


def pre_position_arrays(ds: Dataset) -> StoneArrays:
    """For every unmirrored row, the stones of its pre-shot position: the post position of
    `pre_source_shot` in the same end (empty sheet when 0)."""
    rows = ds.rows[ds.rows["mirror"] == 0]
    n = len(rows)
    x = np.zeros((n, MAX_STONES), dtype=np.float32); y = np.zeros_like(x); own = np.zeros_like(x)
    valid = np.zeros((n, MAX_STONES), dtype=bool)
    st = ds.stones
    key_rows = pd.MultiIndex.from_arrays([rows["game_key"], rows["end"], rows["pre_source_shot"]])
    grp = st.groupby(["game_key", "end", "shot"]).indices
    sx, sy, so = st["x"].to_numpy(np.float32), st["y"].to_numpy(np.float32), st["owner"].to_numpy(np.float32)
    for i, k in enumerate(key_rows):
        if k[2] == 0:
            continue
        idx = grp.get(k)
        if idx is None:
            continue
        m = min(len(idx), MAX_STONES)
        x[i, :m], y[i, :m], own[i, :m], valid[i, :m] = sx[idx[:m]], sy[idx[:m]], so[idx[:m]], True
    return StoneArrays(x, y, own, valid)


# ---- rasteriser ------------------------------------------------------------------------------

def rasterise(x, y, owner, valid, target_xy=None, mirror=None):
    """(B, MAX_STONES) tensors -> (B, C, H, W) float tensor with filled discs. C = 2, or 3 with a target channel.
    `mirror` is a (B,) bool tensor flipping x (and the target) for augmentation."""
    torch = _torch()
    B = x.shape[0]
    if mirror is not None:
        sgn = torch.where(mirror, -1.0, 1.0).unsqueeze(1)
        x = x * sgn
        if target_xy is not None:
            target_xy = target_xy * torch.stack([sgn.squeeze(1), torch.ones_like(sgn.squeeze(1))], dim=1)
    C = 2 if target_xy is None else 3
    canvas = torch.zeros((B, C, H, W), dtype=torch.float32, device=x.device)
    r = int(np.ceil(STONE_RADIUS))
    offs = torch.arange(-r, r + 1, device=x.device, dtype=torch.float32)
    dy, dx = torch.meshgrid(offs, offs, indexing="ij")
    disc = ((dx ** 2 + dy ** 2) <= STONE_RADIUS ** 2).flatten()                    # (K,)
    K = disc.numel()
    cx = torch.round(x - X_MIN).long(); cy = torch.round(y - Y_MIN).long()          # (B, S)
    px = (cx.unsqueeze(-1) + dx.flatten().long()).reshape(B, -1)                     # (B, S*K)
    py = (cy.unsqueeze(-1) + dy.flatten().long()).reshape(B, -1)
    ok = (valid.unsqueeze(-1) & disc).reshape(B, -1) & (px >= 0) & (px < W) & (py >= 0) & (py < H)
    ch = owner.long().unsqueeze(-1).expand(-1, -1, K).reshape(B, -1)                 # 1 own -> channel 0, 0 opp -> channel 1
    ch = 1 - ch
    b = torch.arange(B, device=x.device).unsqueeze(1).expand(-1, px.shape[1])
    flat = (b * C + ch) * (H * W) + py.clamp(0, H - 1) * W + px.clamp(0, W - 1)
    canvas.view(-1).index_put_((flat[ok],), torch.ones_like(flat[ok], dtype=torch.float32), accumulate=False)
    if target_xy is not None:
        tx = torch.round(target_xy[:, 0] - X_MIN).long(); ty = torch.round(target_xy[:, 1] - Y_MIN).long()
        px = (tx.unsqueeze(-1) + dx.flatten().long()); py = (ty.unsqueeze(-1) + dy.flatten().long())
        ok = disc.unsqueeze(0) & (px >= 0) & (px < W) & (py >= 0) & (py < H)
        b = torch.arange(B, device=x.device).unsqueeze(1).expand(-1, K)
        flat = (b * C + 2) * (H * W) + py.clamp(0, H - 1) * W + px.clamp(0, W - 1)
        canvas.view(-1).index_put_((flat[ok],), torch.ones_like(flat[ok], dtype=torch.float32), accumulate=False)
    return canvas


# ---- network ---------------------------------------------------------------------------------

def build_net(n_channels: int, n_scalars: int, width: int = 24):
    torch = _torch()
    nn = torch.nn

    class Net(nn.Module):
        def __init__(self):
            super().__init__()
            chans = [n_channels, width, 2 * width, 4 * width, 4 * width, 8 * width]
            blocks = []
            for a, b in zip(chans[:-1], chans[1:]):
                blocks += [nn.Conv2d(a, b, 3, stride=2, padding=1), nn.BatchNorm2d(b), nn.GELU()]
            self.conv = nn.Sequential(*blocks)
            self.pool = nn.AdaptiveAvgPool2d(1)
            self.head = nn.Sequential(nn.Linear(8 * width + n_scalars, 128), nn.GELU(), nn.Dropout(0.1),
                                      nn.Linear(128, 64), nn.GELU(), nn.Linear(64, N_OUT))

        def forward(self, img, scal):
            h = self.pool(self.conv(img)).flatten(1)
            return self.head(torch.cat([h, scal], dim=1))

    return Net()


# ---- data assembly ---------------------------------------------------------------------------

def scalar_matrix(rows: pd.DataFrame, X: np.ndarray, kind: str) -> tuple[np.ndarray, list[str]]:
    cols = list(SCALAR_F)
    S = [column(rows, X, c) for c in cols]
    if kind == "g":
        st = rows["shot_type_code"].to_numpy(int)
        onehot = np.zeros((len(rows), N_TYPES), dtype=np.float32); onehot[np.arange(len(rows)), np.clip(st, 0, N_TYPES - 1)] = 1
        S += [onehot[:, i] for i in range(N_TYPES)]
        cols += [f"type_{i}" for i in range(N_TYPES)]
        for c in SCALAR_G_EXTRA:
            have = c in rows or c == "turn_code" or (c == "expected_grade" and "grade_logit_base" in rows)
            S.append(column(rows, X, c) if have else np.zeros(len(rows)))
            cols.append(c)
    return np.column_stack(S).astype(np.float32), cols


@dataclass
class RasterFit:
    kind: str
    net: object
    mean: np.ndarray
    std: np.ndarray
    scalar_cols: list[str]
    history: list = field(default_factory=list)

    def predict(self, arrays: StoneArrays, S: np.ndarray, target_xy: np.ndarray | None, batch: int = 1024) -> np.ndarray:
        torch = _torch()
        dev = next(self.net.parameters()).device
        self.net.eval()
        out = np.zeros((len(S), N_OUT), dtype=np.float32)
        Sn = (S - self.mean) / self.std
        with torch.no_grad():
            for i in range(0, len(S), batch):
                sl = slice(i, i + batch)
                img = rasterise(torch.from_numpy(arrays.x[sl]).to(dev), torch.from_numpy(arrays.y[sl]).to(dev),
                                torch.from_numpy(arrays.owner[sl]).to(dev), torch.from_numpy(arrays.valid[sl]).to(dev),
                                None if target_xy is None else torch.from_numpy(target_xy[sl]).to(dev))
                logits = self.net(img, torch.from_numpy(Sn[sl]).to(dev))
                out[sl] = torch.softmax(logits, dim=1).cpu().numpy()
        return out


def fit_raster(kind: str, arrays: StoneArrays, S: np.ndarray, y: np.ndarray, target_xy: np.ndarray | None,
               train_idx: np.ndarray, val_idx: np.ndarray, epochs: int = 8, batch: int = 512, lr: float = 2e-3,
               seed: int = 0, max_train: int | None = None, log_every: int = 200) -> RasterFit:
    """Train f (kind='f', no target channel) or g on the given rows; early stopping on val log-loss."""
    torch = _torch()
    torch.manual_seed(seed); rng = np.random.default_rng(seed)
    dev = torch.device(device_name())
    mean, std = S[train_idx].mean(0), S[train_idx].std(0) + 1e-6
    Sn = ((S - mean) / std).astype(np.float32)
    n_ch = 2 if target_xy is None else 3
    net = build_net(n_ch, S.shape[1]).to(dev)
    opt = torch.optim.AdamW(net.parameters(), lr=lr, weight_decay=1e-4)
    steps_per_epoch = int(np.ceil(len(train_idx) / batch))
    sched = torch.optim.lr_scheduler.OneCycleLR(opt, max_lr=lr, total_steps=epochs * steps_per_epoch)
    loss_fn = torch.nn.CrossEntropyLoss()
    fit = RasterFit(kind, net, mean, std, [])
    best, best_state, bad = np.inf, None, 0
    yt = torch.from_numpy(y.astype(np.int64))
    t0 = time.time()
    for ep in range(epochs):
        net.train()
        order = rng.permutation(train_idx)
        if max_train:
            order = order[:max_train]
        tot, nb = 0.0, 0
        for bi in range(0, len(order), batch):
            idx = order[bi:bi + batch]
            mirror = torch.from_numpy(rng.random(len(idx)) < 0.5).to(dev)
            img = rasterise(torch.from_numpy(arrays.x[idx]).to(dev), torch.from_numpy(arrays.y[idx]).to(dev),
                            torch.from_numpy(arrays.owner[idx]).to(dev), torch.from_numpy(arrays.valid[idx]).to(dev),
                            None if target_xy is None else torch.from_numpy(target_xy[idx]).to(dev), mirror)
            logits = net(img, torch.from_numpy(Sn[idx]).to(dev))
            loss = loss_fn(logits, yt[idx].to(dev))
            opt.zero_grad(); loss.backward(); opt.step(); sched.step()
            tot += float(loss); nb += 1
            if nb % log_every == 0:
                log.info("%s epoch %d batch %d/%d loss %.4f (%.0fs)", kind, ep + 1, nb, steps_per_epoch, tot / nb, time.time() - t0)
        P = fit.predict(arrays_subset(arrays, val_idx), S[val_idx], None if target_xy is None else target_xy[val_idx])
        vl = float(-np.mean(np.log(np.clip(P[np.arange(len(val_idx)), y[val_idx]], 1e-6, 1))))
        fit.history.append({"epoch": ep + 1, "train": tot / max(nb, 1), "val": vl, "seconds": round(time.time() - t0)})
        log.info("%s epoch %d: train %.4f val %.4f (%.0fs)", kind, ep + 1, tot / max(nb, 1), vl, time.time() - t0)
        if vl < best - 1e-4:
            best, bad = vl, 0
            best_state = {k: v.detach().clone() for k, v in net.state_dict().items()}
        else:
            bad += 1
            if bad >= 2:
                break
    if best_state is not None:
        net.load_state_dict(best_state)
    return fit


def arrays_subset(a: StoneArrays, idx: np.ndarray) -> StoneArrays:
    return StoneArrays(a.x[idx], a.y[idx], a.owner[idx], a.valid[idx])


def target_xy_from_rows(rows: pd.DataFrame) -> np.ndarray | None:
    if "target_x" not in rows:
        return None
    return np.column_stack([rows["target_x"].to_numpy(np.float32), rows["target_y"].to_numpy(np.float32)])
