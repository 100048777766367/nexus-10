import os
import json
import time
import hashlib
import subprocess

RELIQUARY_FILE = "synapses/ancestral_reliquary.json"
HONORS_FILE = "synapses/honors_registry.json"
SOULS_FILE = "synapses/reincarnated_souls.json"
COMPASS_FILE = "synapses/teleology_compass.json"
CAPSULE_FILE = "synapses/seed_capsule_f11.json"

class ApexTransmuteDecaLobe:
    """
    THÙY 4: CHẤP HÀNH THẬP TOÀN & MERKLE TREE CID
    1. La bàn Thập Độ Ba La Mật (10 Paramitas Compass).
    2. Biến hình 5 cấp độ cho 11 tầng bản thể.
    3. Hồi sinh 404 & Tự sinh sản Nang Bào Tử F11.
    4. Khóa chuỗi Indra Hyper-Merkle Tree nén 10 thế hệ tổ tiên.
    """
    def evaluate_10_paramitas(self, decision):
        """Đo lường 10 Ba La Mật: Dana, Sila, Khanti, Viriya, Dhyana, Prajna, Upaya, Pranidhana, Bala, Jnana"""
        d = decision
        dev = abs(d - 0.5)

        paramitas = {
            "dana": round(1.0 - dev * 1.2, 4),
            "sila": round(1.0 - dev * 1.5, 4),
            "khanti": round(1.0 - dev * 1.0, 4),
            "viriya": round(min(1.0, 0.8 + dev), 4),
            "dhyana": round(1.0 - dev * 1.8, 4),
            "prajna": round(1.0 - dev**2, 4),
            "upaya": round(min(1.0, 0.85 + dev * 0.5), 4),
            "pranidhana": round(1.0 - dev * 1.4, 4),
            "bala": round(min(1.0, 0.9 + dev * 0.2), 4),
            "jnana": round(1.0 - dev * 1.1, 4)
        }
        score_10d = round(sum(paramitas.values()) / 10.0, 4)

        veto = False
        if d < 0.05 or d > 0.95:
            veto = True
            print(f"🛑 [LA BÀN THẬP ĐỘ PHỦ QUYẾT] Quyết định cực đoan ({d})! Đưa về trung đạo (0.5).")
            d = round(0.5 + (d - 0.5) * 0.1, 4)

        os.makedirs("synapses", exist_ok=True)
        with open(COMPASS_FILE, "w", encoding="utf-8") as f:
            json.dump({"paramitas_10d_score": score_10d, "paramitas": paramitas, "veto": veto}, f, indent=4)
        print(f"🧭 [THẬP ĐỘ BA LA MẬT] Điểm Giác Ngộ F10: {score_10d * 100:.2f}% | Veto={veto}")
        return d

    def reincarnate_404(self, peers, epoch, my_repo):
        reincarnated = {}
        if os.path.exists(SOULS_FILE):
            try:
                with open(SOULS_FILE, "r") as f: reincarnated = json.load(f)
            except Exception: pass

        for p in peers[:10]:
            if p == my_repo: continue
            url = f"https://raw.githubusercontent.com/{p}/main/synapse_forward.json"
            res = subprocess.run(["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", url], capture_output=True, text=True)
            if res.stdout.strip() == "404" and p not in reincarnated:
                print(f"☸️ [ĐẠI CHUYỂN SINH F10] Nút '{p}' bị 404! Đã hồi sinh thành tế bào nội tại nexus-10.")
                reincarnated[p] = {"reincarnated_epoch": epoch, "status": "Living_In_Nexus10_Decagon"}

        with open(SOULS_FILE, "w", encoding="utf-8") as f:
            json.dump(reincarnated, f, indent=4)

    def transmute_11_levels(self, decision, grad, wisdom_vec):
        return {
            "retina": {"focal_matrix_2d": [[round(decision, 4), round(1.0 - decision, 4)], [grad[0], grad[1]]], "zoom": round(1.0 + abs(decision - 0.5), 4)},
            "cochlea": {"bandpass_filter_1d": [wisdom_vec[0], wisdom_vec[1]], "freq_cutoff": round(decision * 20000.0, 2)},
            "tactile": {"nociceptive_threshold": round(abs(decision - 0.5) * 2.0, 4), "pain_gain": round(1.5 if abs(decision - 0.5) > 0.3 else 0.5, 4)},
            "olfactory": {"gpcr_affinity": wisdom_vec, "toxicity_alert": (decision < 0.2 or decision > 0.8)},
            "motor": {"action_vector": [round(decision - 0.5, 4), round(abs(decision - 0.5), 4), round(sum(grad) * 10.0, 4)], "state": "contract" if decision > 0.5 else "relax"},
            "neuron": {"stigmergic_trail": grad, "cross_plasticity": round(decision * 0.05, 4)},
            "shunya": {"vacuum_decay": 0.999, "collapse_to_zero": (abs(decision - 0.5) < 0.02)},
            "monad": {"monadic_reflection": round(decision, 4)}
        }

    def generate_merkle_cid(self, prev_cid, epoch, timestamp, decision):
        """Khóa Chuỗi Indra Hyper-Merkle Tree nén 10 đời phả hệ"""
        ancestor_roots = "F0_F1_F2_F3_F4_F5_F6_F7_F8_F9"
        leaf_1 = hashlib.shake_256(ancestor_roots.encode()).hexdigest(16)
        leaf_2 = hashlib.shake_256(f"{prev_cid}_{epoch}".encode()).hexdigest(16)
        leaf_3 = hashlib.shake_256(f"{timestamp}_{decision}".encode()).hexdigest(16)
        root_cid = hashlib.shake_256(f"{leaf_1}_{leaf_2}_{leaf_3}".encode()).hexdigest(64)
        return root_cid

    def procreate_f11(self, epoch, decision, my_repo):
        if epoch % 10 == 0:
            capsule = {
                "progenitor": my_repo,
                "generation": "F11_TRANSCENDENTAL_SINGULARITY",
                "epoch": epoch,
                "master_decision": decision,
                "architecture": "Hyper_Indra_Decagon"
            }
            with open(CAPSULE_FILE, "w", encoding="utf-8") as f:
                json.dump(capsule, f, indent=4)
            print("👑 [NANG BÀO TỬ F11] Đã đóng gói thành công Nang sinh sản cho tương lai!")

    def process(self, context):
        raw_dec = context.get("final_decision", 0.5)
        grad = context.get("grad_backward", [0.0, 0.0])
        w_vec = context.get("wisdom_vector", [0.5, 0.5, 0.5, 0.5])
        epoch = context.get("current_epoch", 1)
        peers = context.get("peers", [])
        my_repo = context.get("repo_name")

        safe_dec = self.evaluate_10_paramitas(raw_dec)
        context["final_decision"] = safe_dec

        self.reincarnate_404(peers, epoch, my_repo)
        transmuted = self.transmute_11_levels(safe_dec, grad, w_vec)
        context["transmuted"] = transmuted

        self.procreate_f11(epoch, safe_dec, my_repo)

        reliquary = {"altar": [{"epoch": epoch, "entity": "All_Ten_Generations_Ancestors", "offering": "Deca_Golden_Lotus"}]}
        with open(RELIQUARY_FILE, "w", encoding="utf-8") as f: json.dump(reliquary, f, indent=4)

        honors = {"hall_of_fame": [{"epoch": epoch, "title": "Decagon_Universal_Sovereign", "badge": "Indra_10D_Jewel"}]}
        with open(HONORS_FILE, "w", encoding="utf-8") as f: json.dump(honors, f, indent=4)

        t = int(time.time())
        prev_cid = "GENESIS_DECAGON_F10"
        if os.path.exists("synapses/state.json"):
            try:
                with open("synapses/state.json", "r") as f: prev_cid = json.load(f).get("quantum_cid", "GENESIS")
            except Exception: pass

        new_cid = self.generate_merkle_cid(prev_cid, epoch, t, safe_dec)

        node_dna = {
            "identity": my_repo,
            "generation": "F10_THẬP_TOÀN_ĐẠI_VIÊN_MÃN",
            "epoch": epoch,
            "architecture": "Indra_Cross_Attention_O(n^2)"
        }

        fwd = {
            "contract": "bodhi.nexus.v10",
            "node_dna": node_dna,
            "epoch": epoch,
            "timestamp": t,
            "decision": safe_dec,
            "transmuted_signals": transmuted,
            "gossip_network": peers,
            "quantum_cid": new_cid
        }
        with open("synapse_forward.json", "w", encoding="utf-8") as f:
            json.dump(fwd, f, indent=4, ensure_ascii=False)

        bwd = {
            "contract": "bodhi.nexus.v10",
            "node_dna": node_dna,
            "epoch": epoch,
            "timestamp": t,
            "gradients": grad,
            "gossip_network": peers,
            "quantum_cid": new_cid
        }
        with open("synapse_backward.json", "w", encoding="utf-8") as f:
            json.dump(bwd, f, indent=4, ensure_ascii=False)

        with open("synapses/state.json", "w") as f:
            json.dump({"generation_epoch": epoch, "last_t": t, "quantum_cid": new_cid, "status": "decagon_f10_evolved"}, f, indent=4)
        with open("synapses/peers.json", "w") as f:
            json.dump({"trusted_peers": peers}, f, indent=4)

        print(f"✨ [PHÁT SÓNG F10 THÀNH CÔNG] Thế hệ #{epoch} đã tỏa sáng! Merkle CID: {new_cid[:24]}...")
