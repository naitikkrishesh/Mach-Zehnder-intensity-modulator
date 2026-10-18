class Params:
    def __init__(self, wavelength_um=1.55, n_core=2.138, n_clad=1.444, resolution=20):
        
        self.wavelength_um = wavelength_um
        self.n_core = n_core
        self.n_clad = n_clad
        self.resolution = resolution
        
        # interferometer geometry
        self.arm_offset_um: float = 2.5   # arm centre-line offset from axis (arm spacing = 2x)
        self.bend_len_um: float = 20.0    # length of each cosine S-bend (Y-branch)
        self.ps_len_sim_um: float = 30.0  # simulated phase-shifter length (L_sim)
        self.ps_pad_um: float = 3.0       # straight padding before/after phase shifter
        self.lead_in_um: float = 6.0
        self.lead_out_um: float = 8.0
        self.monitor_gap_um: float = 5.0  # output monitor distance after combiner
        self.dpml_um: float = 1.5
        self.margin_um: float = 1.5       # cladding between arms and PML


        # --- electro-optic model (physical device) ---
        self.r33_pm_per_V: float = 30.8   # LiNbO3 r33
        self.electrode_gap_um: float = 5.0
        self.L_phys_mm: float = 5.0       # physical electrode length
        self.mode: str = "single"         # "single" (arm 1 only) or "push-pull"


        # --- numerics ---
        self.resolution: int = 20         # pixels per um
        self.ng_est: float = 2.6          # conservative group-index guess for run time
        self.tail: float = 100.0          # extra run time after pulse transit (Meep units)
        self.time_mult: float = 1.0
        self.nvolt: int = 13              # use 4k+1 so that V_pi/2 and V_pi are sampled
        self.outdir: str = "mzm_results"


    def fcen(self): 
       return 1.0 / self.wavelength_um
  
    def straight_len(self): 
        return self.ps_len_sim_um + 2 * self.ps_pad_um
  
    def sx(self): 
        return 2 * self.dpml_um + self.lead_in_um + 2 * self.bend_len_um + self.straight_len() + self.lead_out_um
   
    def sy(self):
        return 2 * (self.arm_offset_um + self.width_um / 2 + self.margin_um + self.dpml_um)
   
    def x_left(self): 
        return -self.sx / 2 + self.dpml_um
   
    def x_src(self):
        return self.x_left() + 1.0
    
    def x_refl(self): 
        return self.x_src() + 1.5

    def x_split0(self): 
        return self.x_left() + self.lead_in_um


    def x_ps0(self):
        return self.x_split0() + self.bend_len_um + self.ps_pad_um

    def x_ps1(self):
        return self.x_ps0() + self.ps_len_sim_um
  
    def x_comb1(self):
        return self.x_split0() + 2 * self.bend_len_um + self.straight_len()

    def x_mon(self): 
        return self.x_comb1() + self.monitor_gap_um
   
    def L_phys_m(self):
        return self.L_phys_mm * 1e-3
  
    def L_sim_m(self):
        return self.ps_len_sim_um * 1e-6

    def run_time(self):
        return (self.sx() * self.ng_est + self.tail) * self.time_mult


p = Params()

print(p.L_sim_m())