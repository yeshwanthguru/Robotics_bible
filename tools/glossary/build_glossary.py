"""Build the A-Z dictionary pages from tools/glossary/src/*.txt

Each source line:   Term | Domain | Definition | ref1,ref2     (the last field is optional)
Run:  python tools/glossary/build_glossary.py        -> writes docs/glossary/*.md
"""
import glob, json, os, re, sys, collections

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SRC = os.path.join(ROOT, "tools", "glossary", "src")
OUT = os.path.join(ROOT, "docs", "glossary")

# ref key -> (doc path relative to docs/, label)
REFS = {
    "start": ("00-start-here/index", "Start here"),
    "math": ("01-foundations/linear-algebra-probability", "Math foundations"),
    "cs": ("01-foundations/cs-dsa-complexity", "CS & algorithms"),
    "ml": ("02-machine-learning/ml-fundamentals", "ML fundamentals"),
    "dl": ("03-deep-learning/dl-fundamentals", "DL fundamentals"),
    "arch": ("03-deep-learning/architectures", "DL architectures"),
    "rl": ("04-reinforcement-learning/rl-foundations", "RL foundations"),
    "llm": ("05-foundation-models/llm", "LLMs"),
    "vla": ("05-foundation-models/vlm-vla", "VLM & VLA"),
    "qbasics": ("06-quantum/quantum-basics", "Quantum basics"),
    "qalgo": ("06-quantum/quantum-algorithms", "Quantum algorithms"),
    "qsoft": ("06-quantum/quantum-software", "Quantum software"),
    "pai": ("07-physical-ai/physical-ai-overview", "Physical AI"),
    "il": ("07-physical-ai/imitation-robot-learning", "Imitation learning"),
    "kin": ("08-robotics/kinematics", "Kinematics"),
    "dyn": ("08-robotics/dynamics", "Dynamics"),
    "sens": ("08-robotics/sensors-actuators", "Sensors & actuators"),
    "est": ("09-perception-localization/state-estimation", "State estimation"),
    "slam": ("09-perception-localization/slam-localization", "SLAM & localization"),
    "cv": ("09-perception-localization/computer-vision-3d", "Robot perception"),
    "ctrl": ("10-planning-control/control", "Control"),
    "plan": ("10-planning-control/motion-planning", "Motion planning"),
    "pddl": ("10-planning-control/task-planning-pddl", "Task planning & PDDL"),
    "nav": ("11-mobility-dexterity/mobile-navigation", "Mobile navigation"),
    "leg": ("11-mobility-dexterity/legged-locomotion", "Legged locomotion"),
    "manip": ("11-mobility-dexterity/manipulation-dexterity", "Manipulation & dexterity"),
    "space": ("11-mobility-dexterity/space-humanoid-other", "Space & other robots"),
    "ros2": ("12-software/ros2", "ROS 2"),
    "ros1": ("12-software/ros1", "ROS 1"),
    "cpp": ("12-software/cpp-for-robotics", "C++"),
    "py": ("12-software/python-for-robotics", "Python"),
    "matlab": ("12-software/matlab-simulink", "MATLAB"),
    "r": ("12-software/r-for-robotics-stats", "R"),
    "devtools": ("12-software/devtools-deployment", "Dev tools"),
    "sim": ("13-simulation/simulation-landscape", "Simulation landscape"),
    "isaacsim": ("13-simulation/isaac-sim", "Isaac Sim"),
    "isaaclab": ("13-simulation/isaac-lab", "Isaac Lab"),
    "isaacgym": ("13-simulation/isaac-gym", "Isaac Gym"),
    "othersim": ("13-simulation/other-simulators", "Other simulators"),
    "sim2real": ("13-simulation/sim2real", "Sim-to-real"),
    "buildai": ("build-your-own/01-build-an-ai-model", "Build an AI model"),
    "buildvlm": ("build-your-own/02-build-a-vlm", "Build a VLM"),
    "buildvla": ("build-your-own/03-build-a-vla", "Build a VLA"),
    "evaldeploy": ("build-your-own/04-evaluate-deploy-debug", "Evaluate, deploy, debug"),
}
# extra reference keys are registered by tools/glossary/extra_refs.json (added as new chapters are written)
extra = os.path.join(SRC, "extra_refs.json")
if os.path.exists(extra):
    REFS.update({k: tuple(v) for k, v in json.load(open(extra)).items()})


def parse():
    terms, seen = [], {}
    for f in sorted(glob.glob(os.path.join(SRC, "*.txt"))):
        for n, line in enumerate(open(f, encoding="utf-8"), 1):
            line = line.strip()
            if not line or line.startswith("#"): continue
            parts = [p.strip() for p in line.split(" | ")]
            if len(parts) < 3:
                print(f"BAD LINE {os.path.basename(f)}:{n}: {line[:60]}", file=sys.stderr); continue
            term, dom, d = parts[0], parts[1], parts[2]
            refs = [r.strip() for r in parts[3].split(",")] if len(parts) > 3 and parts[3] else []
            for r in refs:
                if r not in REFS: print(f"UNKNOWN REF {r} in {os.path.basename(f)}:{n}", file=sys.stderr)
            key = term.casefold()
            if key in seen:
                print(f"DUPLICATE: {term} ({os.path.basename(f)}:{n})", file=sys.stderr); continue
            seen[key] = True
            terms.append((term, dom, d, [r for r in refs if r in REFS]))
    return terms


def letter(term):
    for ch in term:
        if ch.isalpha(): return ch.upper()
        if ch.isdigit(): return "0-9"
    return "0-9"


def main():
    terms = parse()
    groups = collections.defaultdict(list)
    for t in terms: groups[letter(t[0])].append(t)
    os.makedirs(OUT, exist_ok=True)
    for f in glob.glob(os.path.join(OUT, "*.md")): os.remove(f)
    letters = sorted(groups, key=lambda x: ("~" if x == "0-9" else x))
    nav = " · ".join(f"[{l}](./{l.lower()}.md)" for l in letters)
    for i, l in enumerate(letters, 1):
        items = sorted(groups[l], key=lambda t: re.sub(r"[^a-z0-9]", "", t[0].casefold()))
        lines = ["---", f"title: \"Dictionary: {l}\"", f"sidebar_position: {i}", f"sidebar_label: \"{l}  ({len(items)})\"", "---", "",
                 f"# Dictionary: {l}", "", f"{nav}", "", ":::tip[Tip]\nUse the search box (Ctrl+K). Every term below is its own searchable heading.\n:::", ""]
        for term, dom, d, refs in items:
            lines += [f"### {term}", "", f"**{dom}** · {d}", ""]
            if refs:
                lines += ["*Read more:* " + " · ".join(f"[{REFS[r][1]}](../{REFS[r][0]}.md)" for r in refs), ""]
        open(os.path.join(OUT, f"{l.lower()}.md"), "w", encoding="utf-8").write("\n".join(lines))
    dom_count = collections.Counter(t[1] for t in terms)
    idx = ["---", "title: Dictionary (A–Z)", "sidebar_position: 0", "slug: /glossary", "---", "", "# Dictionary (A–Z)", "",
           f":::tip[How to use this dictionary]\n**{len(terms)} terms** across robotics, AI, machine learning, deep learning, reinforcement learning, LLM/VLM/VLA, quantum computing, control, planning, perception, software and simulation. Press **Ctrl+K** and type any word: each term is a separate search result with a one-line definition and a link to the full chapter.\n:::", "",
           "## Jump to a letter", "", nav, "", "## Terms by domain", "", "| Domain | Terms |", "|---|---|"]
    idx += [f"| {d} | {c} |" for d, c in sorted(dom_count.items(), key=lambda x: -x[1])]
    open(os.path.join(OUT, "index.md"), "w", encoding="utf-8").write("\n".join(idx) + "\n")
    json.dump({"label": "Dictionary (A–Z)", "position": 0.6, "collapsed": True}, open(os.path.join(OUT, "_category_.json"), "w"))
    print(f"{len(terms)} terms -> {len(letters)} letter pages")


if __name__ == "__main__":
    main()
