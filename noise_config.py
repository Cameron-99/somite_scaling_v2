import os
vrest_noise = [-44, -42, -40, -38, -36]
gjunc_noise = [0.73, 0.82, 0.91, 1.00, 1.09]

os.makedirs('noise_models', exist_ok=True)
configs = []

for i, vrest in enumerate(vrest_noise):
    for j, gjunc in enumerate(gjunc_noise):
        outdir = f"noise_models/vrest{vrest}_gj{gjunc:.2f}"
        config_path = f"{outdir}/sim_config.yaml"
        
        # Generate base config
        os.system(f"betse config {config_path}")
        
        # Inject noise parameters
        with open(config_path, 'r') as f:
            config = f.read()
        
        config = config.replace('pHCN2: 0.0', 'pHCN2: 1.2')      # Fixed optimum
        config = config.replace('pCx43: 0.0', f'pCx43: {gjunc}') # Gap junction noise
        config = config.replace('vrest: -40.0', f'vrest: {vrest}') # Rest potential noise
        
        with open(config_path, 'w') as f:
            f.write(config)
            
        configs.append({'vrest': vrest, 'gjunc': gjunc, 'path': config_path})
        print(f"Generated: {config_path}")

print(f"\n✅ 25 noise configs ready!")
with open('noise_configs.pkl', 'wb') as f:
    import pickle
    pickle.dump(configs, f)
