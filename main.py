#!/usr/bin/env python3
"""
Shadow Army — Monarch Fleet Runtime
Usage: python main.py "your task here"
       python main.py --status
"""
from __future__ import annotations
import asyncio
import sys
import os

# Run from repo root
os.chdir(os.path.dirname(os.path.abspath(__file__)))

from shadow_army.fleet import Fleet
from shadow_army.monarch import Monarch


async def main() -> None:
    args = sys.argv[1:]

    fleet = Fleet(base_dir=".")
    init_events = fleet.load()

    if "--status" in args:
        print(fleet.fleet_report())
        if init_events:
            print("\nInit events:")
            for e in init_events:
                print(f"  {e}")
        return

    if not args:
        print("Usage: python main.py \"your task here\"")
        print("       python main.py --status")
        return

    task = " ".join(a for a in args if not a.startswith("--"))
    if not task:
        print("No task provided.")
        return

    if init_events:
        for e in init_events:
            print(f"  {e}")

    monarch = Monarch(fleet)
    result = await monarch.run(task)

    print("\n── Output ───────────────────────────────────────")
    print(result["output"])

    if result.get("events"):
        print("\n── Events ───────────────────────────────────────")
        for e in result["events"]:
            print(f"  {e}")

    print(fleet.fleet_report())

    fleet.save()
    print("\n  State saved.")


if __name__ == "__main__":
    asyncio.run(main())
