# data.py

# A dictionary of assembly program templates. 
# We pair a CISC implementation and a RISC implementation for the same logical task
# so the user can see how the assembly paradigms differ side-by-side.
PRESETS = {
    "A + B  (add two numbers)": {
        "cisc": """; x86 CISC — add A=12, B=8\n; CISC can add memory operand directly\nDATA 100, 12        ; MEM[100] = 12\nDATA 104, 8         ; MEM[104] = 8\nMOV  EAX, [100]     ; EAX = A\nADD  EAX, [104]     ; EAX = EAX + B  ← memory operand!\nMOV  [200], EAX     ; store result""",
        "risc": """# MIPS RISC — add A=12, B=8\n# RISC: must LOAD before any operation\nDATA 100, 12        # MEM[100] = 12\nDATA 104, 8         # MEM[104] = 8\nLOAD R1, 100        # R1 = MEM[100]\nLOAD R2, 104        # R2 = MEM[104]\nADD  R3, R1, R2     # R3 = R1 + R2\nSTORE R3, 200       # store result"""
    },
    "A × B  (multiply)": {
        "cisc": """; x86 CISC — multiply A=6, B=7\nDATA 100, 6\nDATA 104, 7\nMOV  EAX, [100]     ; load A\nIMUL EAX, [104]     ; EAX = EAX × MEM[104]  ← one instruction!\nMOV  [200], EAX     ; store result""",
        "risc": """# MIPS RISC — multiply A=6, B=7\nDATA 100, 6\nDATA 104, 7\nLOAD R1, 100        # R1 = A\nLOAD R2, 104        # R2 = B\nMUL  R3, R1, R2     # R3 = R1 × R2\nSTORE R3, 200       # store result"""
    },
    "(A + B) × C": {
        "cisc": """; x86 CISC — (A+B)*C  values: 5, 3, 4\nDATA 100, 5\nDATA 104, 3\nDATA 108, 4\nMOV  EAX, [100]     ; EAX = A\nADD  EAX, [104]     ; EAX = A + B  (memory direct)\nIMUL EAX, [108]     ; EAX = (A+B) * C  (memory direct)\nMOV  [200], EAX     ; store result""",
        "risc": """# MIPS RISC — (A+B)*C  values: 5, 3, 4\nDATA 100, 5\nDATA 104, 3\nDATA 108, 4\nLOAD R1, 100        # R1 = A\nLOAD R2, 104        # R2 = B\nLOAD R3, 108        # R3 = C\nADD  R4, R1, R2     # R4 = A + B\nMUL  R5, R4, R3     # R5 = (A+B) * C\nSTORE R5, 200       # store result"""
    },
    "Swap two values": {
        "cisc": """; x86 CISC — swap MEM[100] and MEM[104]\nDATA 100, 42\nDATA 104, 99\nMOV  EAX, [100]     ; EAX = first\nMOV  EBX, [104]     ; EBX = second\nMOV  [100], EBX     ; first  = second\nMOV  [104], EAX     ; second = first""",
        "risc": """# MIPS RISC — swap MEM[100] and MEM[104]\nDATA 100, 42\nDATA 104, 99\nLOAD R1, 100        # R1 = first\nLOAD R2, 104        # R2 = second\nSTORE R2, 100       # first  = second\nSTORE R1, 104       # second = first"""
    },
}

PLOT_BASE = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(color='#94a3b8', family='IBM Plex Mono'),
    margin=dict(t=30, b=10, l=10, r=10),
)

SPEC_DATA = {
    "Processor": ["i9-13900K", "Ryzen 9 7950X", "Apple M3 Max", "Apple M2 Ultra", "AWS Graviton3"],
    "Score": [57.6, 62.1, 58.9, 67.4, 43.0],
    "Arch": ["CISC", "CISC", "RISC", "RISC", "RISC"],
    "TDP": [253, 170, 92, 157, 150],
}

CPI_DATA = {
    "wl_names": ["Integer ALU","Load/Store","Branch-heavy","FP Compute","SIMD/Media"],
    "cisc_cpi": [1.15, 1.35, 1.65, 1.10, 1.05],
    "risc_cpi": [1.08, 1.20, 1.45, 1.05, 1.10]
}

TRANSISTOR_DATA = {
    "name": ["8086","386","Pentium","Core 2","Skylake","Raptor Lake","ARM v1","Cortex-A8","Cortex-A15","Apple M1","Apple M3"],
    "year": [1978,1985,1993,2006,2015,2022,1985,2008,2012,2020,2023],
    "tr_m": [0.029,0.275,3.1,291,1750,19400,0.025,153,1400,16000,92000],
    "arch": ["CISC","CISC","CISC","CISC","CISC","CISC","RISC","RISC","RISC","RISC","RISC"]
}

PIPE_DATA = {
    "Processor": ["MIPS R2000","ARM Cortex-A8","ARM Cortex-A15","Apple M1","Intel Pentium","Intel P4 (Netburst)","Intel Core","Intel Skylake"],
    "Stages": [5,13,15,19,5,31,14,14],
    "Arch": ["RISC","RISC","RISC","RISC","CISC","CISC","CISC","CISC"]
}