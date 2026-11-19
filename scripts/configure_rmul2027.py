"""Configure RMUL 2027 3V3 field, ruleset, season entry, and robot eligibility in config/rules.json.

Preserves existing 2026 and 2027 RMUC configurations and default_season ("2027").
Coordinates are extracted from RMUL2027_3V3_1to1.blend (12.0 m x 8.0 m, z=0 floor).
"""
from __future__ import annotations

import copy
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RULES_PATH = ROOT / "config" / "rules.json"


def rect_poly(x: float, y: float, w: float, h: float) -> list[list[float]]:
    return [
        [round(x, 6), round(y, 6)],
        [round(x + w, 6), round(y, 6)],
        [round(x + w, 6), round(y + h, 6)],
        [round(x, 6), round(y + h, 6)],
    ]


def build_rmul2027_map() -> dict:
    # Exact terrain & structures measured from RMUL2027_3V3_1to1.blend,
    # augmented with smooth 0.75 m ramps (14.9 deg) so all 3V3 chassis can climb the 0.20 m highlands.
    terrain = [
        {
            "id": "red_highland",
            "x": 2.5,
            "y": 0.94,
            "w": 2.0,
            "h": 4.06,
            "polygon": [[2.5, 1.02], [2.6386, 0.94], [4.3614, 0.94], [4.5, 1.02], [4.5, 5.0], [2.5, 5.0]],
            "kind": "platform",
            "elevation": 0.20,
            "speed_multiplier": 1.0,
            "direction": 0,
            "axis": "x",
            "source_page": 0,
            "base_elevation": 0.0,
            "edge_ramp_m": 0.0,
            "bump_pitch": 0.0,
            "bump_height": 0.0,
            "slope_deg": 0.0,
        },
        {
            "id": "blue_highland",
            "x": 7.5,
            "y": 3.0,
            "w": 2.0,
            "h": 4.06,
            "polygon": [[7.5, 3.0], [9.5, 3.0], [9.5, 6.98], [9.3614, 7.06], [7.6386, 7.06], [7.5, 6.98]],
            "kind": "platform",
            "elevation": 0.20,
            "speed_multiplier": 1.0,
            "direction": 0,
            "axis": "x",
            "source_page": 0,
            "base_elevation": 0.0,
            "edge_ramp_m": 0.0,
            "bump_pitch": 0.0,
            "bump_height": 0.0,
            "slope_deg": 0.0,
        },
        {
            "id": "red_highland_ramp_west",
            "x": 1.75,
            "y": 2.0,
            "w": 0.75,
            "h": 3.0,
            "polygon": rect_poly(1.75, 2.0, 0.75, 3.0),
            "kind": "ramp",
            "elevation": 0.20,
            "base_elevation": 0.0,
            "speed_multiplier": 0.95,
            "direction": 1,
            "axis": "x",
            "source_page": 0,
            "edge_ramp_m": 0.0,
            "bump_pitch": 0.0,
            "bump_height": 0.0,
            "slope_deg": 14.9,
            "ramp_start": [1.75, 3.5],
            "ramp_end": [2.5, 3.5],
        },
        {
            "id": "red_highland_ramp_south",
            "x": 2.5,
            "y": 5.0,
            "w": 2.0,
            "h": 0.75,
            "polygon": rect_poly(2.5, 5.0, 2.0, 0.75),
            "kind": "ramp",
            "elevation": 0.20,
            "base_elevation": 0.0,
            "speed_multiplier": 0.95,
            "direction": -1,
            "axis": "y",
            "source_page": 0,
            "edge_ramp_m": 0.0,
            "bump_pitch": 0.0,
            "bump_height": 0.0,
            "slope_deg": 14.9,
            "ramp_start": [3.5, 5.75],
            "ramp_end": [3.5, 5.0],
        },
        {
            "id": "red_highland_ramp_east_north",
            "x": 4.5,
            "y": 1.02,
            "w": 0.75,
            "h": 1.28,
            "polygon": rect_poly(4.5, 1.02, 0.75, 1.28),
            "kind": "ramp",
            "elevation": 0.20,
            "base_elevation": 0.0,
            "speed_multiplier": 0.95,
            "direction": -1,
            "axis": "x",
            "source_page": 0,
            "edge_ramp_m": 0.0,
            "bump_pitch": 0.0,
            "bump_height": 0.0,
            "slope_deg": 14.9,
            "ramp_start": [5.25, 1.66],
            "ramp_end": [4.5, 1.66],
        },
        {
            "id": "blue_highland_ramp_east",
            "x": 9.5,
            "y": 3.0,
            "w": 0.75,
            "h": 3.0,
            "polygon": rect_poly(9.5, 3.0, 0.75, 3.0),
            "kind": "ramp",
            "elevation": 0.20,
            "base_elevation": 0.0,
            "speed_multiplier": 0.95,
            "direction": -1,
            "axis": "x",
            "source_page": 0,
            "edge_ramp_m": 0.0,
            "bump_pitch": 0.0,
            "bump_height": 0.0,
            "slope_deg": 14.9,
            "ramp_start": [10.25, 4.5],
            "ramp_end": [9.5, 4.5],
        },
        {
            "id": "blue_highland_ramp_north",
            "x": 7.5,
            "y": 2.25,
            "w": 2.0,
            "h": 0.75,
            "polygon": rect_poly(7.5, 2.25, 2.0, 0.75),
            "kind": "ramp",
            "elevation": 0.20,
            "base_elevation": 0.0,
            "speed_multiplier": 0.95,
            "direction": 1,
            "axis": "y",
            "source_page": 0,
            "edge_ramp_m": 0.0,
            "bump_pitch": 0.0,
            "bump_height": 0.0,
            "slope_deg": 14.9,
            "ramp_start": [8.5, 2.25],
            "ramp_end": [8.5, 3.0],
        },
        {
            "id": "blue_highland_ramp_west_south",
            "x": 6.75,
            "y": 5.7,
            "w": 0.75,
            "h": 1.28,
            "polygon": rect_poly(6.75, 5.7, 0.75, 1.28),
            "kind": "ramp",
            "elevation": 0.20,
            "base_elevation": 0.0,
            "speed_multiplier": 0.95,
            "direction": 1,
            "axis": "x",
            "source_page": 0,
            "edge_ramp_m": 0.0,
            "bump_pitch": 0.0,
            "bump_height": 0.0,
            "slope_deg": 14.9,
            "ramp_start": [6.75, 6.34],
            "ramp_end": [7.5, 6.34],
        },
    ]

    obstacles = [
        {"id": "red_highland_barrier", "x": 4.35, "y": 2.3, "w": 0.15, "h": 1.8, "bottom": 0.20, "height": 0.20, "rotation": 0.0, "kind": "barrier", "source_page": 0},
        {"id": "blue_highland_barrier", "x": 7.5, "y": 3.9, "w": 0.15, "h": 1.8, "bottom": 0.20, "height": 0.20, "rotation": 0.0, "kind": "barrier", "source_page": 0},
        {"id": "red_tunnel_support", "x": 2.5, "y": 0.0, "w": 2.0, "h": 0.14, "bottom": 0.0, "height": 0.20, "rotation": 0.0, "kind": "wall", "source_page": 0},
        {"id": "blue_tunnel_support", "x": 7.5, "y": 7.86, "w": 2.0, "h": 0.14, "bottom": 0.0, "height": 0.20, "rotation": 0.0, "kind": "wall", "source_page": 0},
        {"id": "red_tunnel_roof", "x": 3.325, "y": 0.0, "w": 0.35, "h": 1.08, "bottom": 0.20, "height": 0.07, "rotation": 0.0, "kind": "roof", "source_page": 0},
        {"id": "blue_tunnel_roof", "x": 8.325, "y": 6.92, "w": 0.35, "h": 1.08, "bottom": 0.20, "height": 0.07, "rotation": 0.0, "kind": "roof", "source_page": 0},
        {"id": "red_workbench", "x": 0.0, "y": 0.0, "w": 0.75, "h": 0.45, "bottom": 0.0, "height": 0.403, "rotation": 0.0, "kind": "fixture", "source_page": 0},
        {"id": "blue_workbench", "x": 11.25, "y": 7.55, "w": 0.75, "h": 0.45, "bottom": 0.0, "height": 0.403, "rotation": 0.0, "kind": "fixture", "source_page": 0},
    ]

    zones = [
        {
            "id": "red_supply",
            "kind": "supply",
            "owner": "red",
            "x": 1.5,
            "y": 1.15,
            "radius": 0.8,
            "source": "RMUL2027_3V3_1to1.blend",
            "polygon": [[0.0, 0.0], [2.5, 0.0], [2.5, 2.0], [0.0, 2.0]],
        },
        {
            "id": "blue_supply",
            "kind": "supply",
            "owner": "blue",
            "x": 10.5,
            "y": 6.85,
            "radius": 0.8,
            "source": "RMUL2027_3V3_1to1.blend",
            "polygon": [[9.5, 6.0], [12.0, 6.0], [12.0, 8.0], [9.5, 8.0]],
        },
        {
            "id": "red_control",
            "kind": "high_point",
            "owner": "red",
            "x": 3.5,
            "y": 3.2,
            "radius": 0.6,
            "source": "RMUL2027_3V3_1to1.blend",
            "polygon": [[2.9, 2.6], [4.1, 2.6], [4.1, 3.8], [2.9, 3.8]],
        },
        {
            "id": "blue_control",
            "kind": "high_point",
            "owner": "blue",
            "x": 8.5,
            "y": 4.8,
            "radius": 0.6,
            "source": "RMUL2027_3V3_1to1.blend",
            "polygon": [[7.9, 4.2], [9.1, 4.2], [9.1, 5.4], [7.9, 5.4]],
        },
        {
            "id": "centre_control",
            "kind": "central",
            "owner": None,
            "x": 6.0,
            "y": 4.0,
            "radius": 1.5,
            "source": "RMUL2027_3V3_1to1.blend",
            "polygon": [[4.5, 2.5], [7.5, 2.5], [7.5, 5.5], [4.5, 5.5]],
        },
        {
            "id": "red_tunnel_buff",
            "kind": "tunnel_buff",
            "owner": "red",
            "x": 4.0875,
            "y": 0.54,
            "radius": 0.4,
            "source": "RMUL2027_3V3_1to1.blend",
            "polygon": [[3.675, 0.14], [4.5, 0.14], [4.5, 0.94], [3.675, 0.94]],
        },
        {
            "id": "blue_tunnel_buff",
            "kind": "tunnel_buff",
            "owner": "blue",
            "x": 7.9125,
            "y": 7.46,
            "radius": 0.4,
            "source": "RMUL2027_3V3_1to1.blend",
            "polygon": [[7.5, 7.06], [8.325, 7.06], [8.325, 7.86], [7.5, 7.86]],
        },
        {
            "id": "red_workbench",
            "kind": "workbench",
            "owner": "red",
            "x": 1.20,
            "y": 0.85,
            "radius": 0.55,
            "source": "RMUL2027_3V3_1to1.blend",
            "polygon": [[0.75, 0.0], [1.75, 0.0], [1.75, 1.25], [0.75, 1.25]],
        },
        {
            "id": "blue_workbench",
            "kind": "workbench",
            "owner": "blue",
            "x": 10.80,
            "y": 7.15,
            "radius": 0.55,
            "source": "RMUL2027_3V3_1to1.blend",
            "polygon": [[10.25, 6.75], [11.25, 6.75], [11.25, 8.0], [10.25, 8.0]],
        },
    ]

    nav_nodes = [
        # Red side & supply / workbench
        [1.20, 0.85], [1.50, 1.15], [1.10, 1.75], [2.00, 1.45],
        # Red open lanes (west / south / north)
        [0.80, 3.50], [1.20, 2.60], [1.20, 3.50], [1.20, 4.40], [1.20, 6.50],
        # Red highland ramp approaches, tops & control
        [2.12, 3.50], [2.90, 3.50],
        [3.50, 6.30], [3.50, 5.38], [3.50, 4.60],
        [3.50, 3.20], [3.50, 1.66],
        [5.70, 1.66], [4.88, 1.66], [4.10, 1.66],
        # Red tunnel buff & north lane
        [4.09, 0.54], [5.70, 0.80],
        # Center corridors & centre control
        [6.00, 1.20], [6.00, 2.20], [6.00, 4.00], [6.00, 5.80], [6.00, 6.80],
        [4.95, 4.80], [7.05, 3.20],
        # South corridor
        [3.50, 6.80], [8.50, 1.20],
        # Blue highland ramp approaches, tops & control
        [6.30, 6.34], [7.12, 6.34], [7.90, 6.34],
        [8.50, 1.70], [8.50, 2.62], [8.50, 3.40],
        [8.50, 4.80], [8.50, 6.34],
        [9.88, 4.50], [9.10, 4.50],
        # Blue tunnel buff & south lane
        [7.91, 7.46], [6.30, 7.20],
        # Blue open lanes & supply / workbench
        [10.80, 1.50], [10.80, 3.60], [10.80, 4.50], [10.80, 5.40], [11.20, 4.50],
        [10.00, 6.55], [10.90, 6.25], [10.50, 6.85], [10.80, 7.15],
    ]

    return {
        "name": "RMUL 2027 3V3",
        "season": "rmul2027",
        "ruleset": "rmul2027",
        "layout_revision": "rmul2027-blend-v1",
        "width": 12.0,
        "height": 8.0,
        "floor_slope_deg": 0.0,
        "terrain": terrain,
        "obstacles": obstacles,
        "zones": zones,
        "forbidden": [
            {"id": "red_supply_forbidden", "kind": "supply", "owner": "red", "x": 0.0, "y": 0.0, "w": 2.5, "h": 2.0},
            {"id": "blue_supply_forbidden", "kind": "supply", "owner": "blue", "x": 9.5, "y": 6.0, "w": 2.5, "h": 2.0},
        ],
        "spawn_points": {
            "red": {"1": [1.35, 0.90], "3": [2.00, 1.45], "7": [1.05, 1.75]},
            "blue": {"1": [10.65, 7.10], "3": [10.00, 6.55], "7": [10.95, 6.25]},
        },
        "bases": {},
        "outposts": {},
        "outpost_plinth_m": 0.0,
        "pads": {},
        "hangars": None,
        "positions": {
            "red_control": {"owner": "neutral", "kind": "control", "zones": ["red_control"]},
            "centre_control": {"owner": "neutral", "kind": "control", "zones": ["centre_control"]},
            "blue_control": {"owner": "neutral", "kind": "control", "zones": ["blue_control"]},
        },
        "flight_lanes": [],
        "rune": None,
        "assembly_frames": {},
        "asset": "/assets/map-rmul2027.glb",
        "structure_assets": {},
        "field_geometry": {
            "fixtures": [
                {"kind": "workbench", "team": "red", "dock_point": [1.20, 0.85]},
                {"kind": "workbench", "team": "blue", "dock_point": [10.80, 7.15]},
            ]
        },
        "navigation": {"nodes": nav_nodes},
    }


def build_rmul2027_rulebook(base_rulebook: dict) -> dict:
    rb = copy.deepcopy(base_rulebook)
    rb["season"] = "rmul2027"
    rb["source"] = "RoboMaster 2027 RMUL 3V3 V1.0.0 (2026-10-15) + RMUL2027_3V3_1to1.blend"
    rb["match"] = {
        **rb.get("match", {}),
        "duration_s": 300,
        "field_length_m": 12.0,
        "field_width_m": 8.0,
        "fence_height_m": 1.2,
    }
    rb["control"] = {
        "mode": "rmul_drain",
        "positions": ["red_control", "centre_control", "blue_control"],
        "initial_control": 600.0,
        "capture_s": 5.0,
        "zone_drain_per_s": 1.0,
        "death_penalty": 10.0,
        "comeback": [
            {"gap": 200.0, "coins": 200, "respawn_scale": 0.67, "supply_heal_ratio": 0.33},
            {"gap": 400.0, "coins": 200, "respawn_scale": 0.50, "supply_heal_ratio": 0.50},
        ],
    }
    rb["initial_ammo"] = {"heavy": 0, "infantry": 0, "sentry": 750}
    rb["economy"] = {
        **rb["economy"],
        "initial_coins": 200,
        "initial_coin_time_s": 1,
        "periodic_schedule": [
            {"elapsed_s": 61, "coins": 200},
            {"elapsed_s": 121, "coins": 200},
            {"elapsed_s": 181, "coins": 300},
            {"elapsed_s": 241, "coins": 300},
        ],
        "ammo": {
            "17mm": {"local_batch": 10, "local_cost": 10, "remote_batch": 0, "remote_cost": 0, "team_purchase_cap": 10000},
            "42mm": {"local_batch": 1, "local_cost": 10, "remote_batch": 0, "remote_cost": 0, "team_purchase_cap": 1000},
        },
        "local_exchange_points": ["supply"],
    }
    rb["heavy"] = {
        **rb["heavy"],
        "stages": [
            {"after": "start", "hp": 100, "power_w": 50, "max_heat": 0, "cooling": 0},
            {"after": "launcher", "hp": 450, "power_w": 50, "max_heat": 250, "cooling": 66, "muzzle_limit_mps": 16.5},
        ],
        "early_defense": 0.0,
        "early_defense_until_s": 0,
        "early_defense_ends_with_launcher": True,
        "supply_invulnerable": True,
    }
    rb["profiles"] = {
        "defaults": {"infantry_chassis": "hp", "infantry_weapon": "cooling"},
        "infantry_chassis": {
            "hp": [{"level": 1, "hp": 350, "power_w": 75}],
            "power": [{"level": 1, "hp": 300, "power_w": 90}],
        },
        "infantry_weapon": {
            "cooling": [{"level": 1, "max_heat": 88, "cooling": 24}],
            "burst": [{"level": 1, "max_heat": 230, "cooling": 14}],
        },
        "locked_after_start": True,
        "level_up_adds_hp_delta": False,
    }
    rb["sentry"] = {
        **rb["sentry"],
        "automatic": {"hp": 400, "max_heat": 260, "cooling": 30, "power_w": 100},
        "initial_ammo": 750,
        "self_service_via_serial": False,
        "multi_robot_comms": False,
    }
    rb["experience"] = {
        **rb["experience"],
        "initial_cap": 1,
        "cap_after_assembly_2": 1,
        "cap_after_assembly_3": 1,
    }
    rb["heal"] = {
        **rb["heal"],
        "supply_ratio_per_s": 0.25,
        "late_start_s": 9999.0,
        "late_disengaged_supply_ratio_per_s": 0.25,
        "outpost_ratio_of_supply": 0.0,
        "remote_ratio": 0.0,
    }
    rb["respawn"] = {
        **rb["respawn"],
        "progress_per_death": 5.0,
        "normal_progress_per_s": 1.0,
        "fast_progress_per_s": 1.0,
        "normal_hp_ratio": 0.20,
        "normal_invulnerability_s": 30.0,
        "weak_clear_invulnerability_min_s": 0.0,
    }
    rb["structures"] = {**rb["structures"], "base_hp": 0, "outpost_hp": 0}
    rb["buffs"] = {
        **rb["buffs"],
        "release_delay_s": 2.0,
        "high_point_defense": 0.25,
        "central_defense": 0.0,
        "tunnel_cooling_multiplier": 1.5,
        "tunnel_window_s": 3.0,
        "tunnel_duration_s": 60.0,
    }
    rb["winner"] = {
        "order": [
            "Drain opponent control degree to zero (control_depleted)",
            "On timeout: higher remaining control degree, higher total attack damage, higher alive ground HP total",
        ]
    }
    return rb


def main() -> None:
    rules = json.loads(RULES_PATH.read_text(encoding="utf-8"))
    rules["maps"]["rmul2027"] = build_rmul2027_map()
    rules["rulebook_rmul2027"] = build_rmul2027_rulebook(rules["rulebook_2027"])

    s27 = rules["seasons"]["2027"]
    sim_overrides = copy.deepcopy(s27["simulation_overrides"])
    sim_overrides["launcher_install"]["stationary_s"] = 4.0

    rmul_specs = {
        "heavy": {**copy.deepcopy(s27["specs"]["heavy"]), "hp": 100, "power_w": 50, "max_heat": 0, "cooling": 0, "ammo": 0},
        "infantry": {**copy.deepcopy(s27["specs"]["infantry"]), "hp": 350, "power_w": 75, "max_heat": 88, "cooling": 24, "ammo": 0},
        "sentry": {**copy.deepcopy(s27["specs"]["sentry"]), "hp": 400, "power_w": 100, "max_heat": 260, "cooling": 30, "ammo": 750},
    }

    rules["seasons"]["rmul2027"] = {
        "label": "RMUL 2027 3V3",
        "rules_profile": "rmul-2027-v1.0.0-arena-v1",
        "rules_key": "rulebook_rmul2027",
        "map": "rmul2027",
        "roster": [
            {"slot": 1, "role": "heavy"},
            {"slot": 3, "role": "infantry"},
            {"slot": 7, "role": "sentry"},
        ],
        "default_lineup": {"1": 2711, "3": 2731, "7": 2771},
        "specs": rmul_specs,
        "simulation_overrides": sim_overrides,
    }

    for model_id, design in rules["robot_designs"].items():
        role = design.get("role")
        legal_2027 = bool(design.get("seasons", {}).get("2027", {}).get("legal"))
        if legal_2027 and role in ("heavy", "infantry", "sentry"):
            entry = {"legal": True, "role": role, "issues": []}
        else:
            if role not in ("heavy", "infantry", "sentry"):
                issue = {
                    "code": "role",
                    "zh": f"RMUL 2027 3V3 仅开放重装（1）、步兵（3）与哨兵（7），不支持 {role}",
                    "en": f"RMUL 2027 3V3 fields only heavy (1), infantry (3), and sentry (7), not {role}",
                }
            else:
                issue = copy.deepcopy(
                    (design.get("seasons", {}).get("2027", {}).get("issues") or [
                        {"code": "spec", "zh": f"型号 {model_id} 不符合 2027 制作规范", "en": f"Model {model_id} fails 2027 construction rules"}
                    ])[0]
                )
            entry = {"legal": False, "role": role, "issues": [issue]}
        design.setdefault("seasons", {})["rmul2027"] = entry

    RULES_PATH.write_text(json.dumps(rules, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Updated {RULES_PATH} with rmul2027 map, rulebook_rmul2027, season, and robot_designs.")


if __name__ == "__main__":
    main()
