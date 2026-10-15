import os
import json
import re
import random
from cells.neuron import AtomNeuron, sigmoid_derivative
from cells.super_xor import SuperXorMatrix

GRAPH_FILE = "synapses/knowledge_graph.json"
META_LOG_FILE = "synapses/metacognitive_synthesis.json"

class MetacognitionDecaLobe:
    """
    THÙY 3: SIÊU NHẬN THỨC & TỰ BIÊN DỊCH MÃ
    1. Giả lập 10 kịch bản tương lai What-If (Decagon Sandbox).
    2. Tự động sinh hàm vi mô (Dynamic Lambda Synthesis) khi mất mát cao.
    3. REM Sleep Giấc mơ sâu tái hiện quá khứ.
    4. Huấn luyện AtomNeuron 1+N Siêu XOR.
    """
    def __init__(self, num_cells=8):
        self.num_cells = num_cells
        self.swarm = [AtomNeuron(f"n10_h_{i}", n_inputs=4, n_super_xor=4) for i in range(num_cells)]
        self.out_cell = AtomNeuron("n10_out", n_inputs=num_cells, n_super_xor=4)

    def extract_knowledge_graph(self, text):
        triplets = []
        for s in re.split(r'[.\n]', text):
            words = [w.strip() for w in s.split() if len(w.strip()) > 2]
            if len(words) >= 3:
                triplets.append({"subject": words[0].capitalize(), "predicate": words[1].lower(), "object": " ".join(words[2:4])})

        graph = {"nodes": [], "edges": []}
        if os.path.exists(GRAPH_FILE):
            try:
                with open(GRAPH_FILE, "r") as f: graph = json.load(f)
            except Exception: pass

        for t in triplets[:8]:
            if t["subject"] not in graph["nodes"]: graph["nodes"].append(t["subject"])
            if t["object"] not in graph["nodes"]: graph["nodes"].append(t["object"])
            edge = f"{t['subject']} ===[{t['predicate']}]===> {t['object']}"
            if edge not in graph["edges"]: graph["edges"].append(edge)

        graph["nodes"] = graph["nodes"][-100:]
        graph["edges"] = graph["edges"][-150:]
        os.makedirs("synapses", exist_ok=True)
        with open(GRAPH_FILE, "w", encoding="utf-8") as f:
            json.dump(graph, f, indent=4, ensure_ascii=False)

    def simulate_10_futures(self, raw_decision):
        variations = [0.65, 0.75, 0.82, 0.90, 0.96, 1.0, 1.04, 1.10, 1.20, 1.35]
        sims = []
        for factor in variations:
            cand = max(0.01, min(0.99, round(raw_decision * factor, 4)))
            risk = abs(cand - 0.5) * factor
            stability = 1.0 - abs(cand - 0.5)
            loss = round((risk * 0.5) + ((1.0 - stability) * 0.5), 4)
            sims.append((loss, cand))
        sims.sort(key=lambda x: x[0])
        best_loss, best_cand = sims[0]
        print(f"🔮 [GIẢ LẬP 10 TƯƠNG LAI] Kịch bản tối ưu nhất: {best_cand} (Loss={best_loss})")
        return best_cand, best_loss

    def synthesize_dynamic_logic(self, decision, loss):
        """SIÊU NHẬN THỨC: Tự sinh mã vi mô nếu hàm mất mát vượt ngưỡng 0.08"""
        if loss > 0.08:
            print("💡 [SIÊU NHẬN THỨC TỰ SINH MÃ] Phát hiện hàm mất mát cao! Đang tự tạo hàm điều biến động...")
            delta_tuning = round((0.5 - decision) * 0.12, 4)
            adjusted_decision = round(decision + delta_tuning, 4)

            log = {
                "synthesized_rule": f"lambda d: d + {delta_tuning}",
                "original_decision": decision,
                "adjusted_decision": adjusted_decision,
                "reason": "Metacognitive_Loss_Mitigation"
            }
            with open(META_LOG_FILE, "w", encoding="utf-8") as f:
                json.dump(log, f, indent=4)
            return adjusted_decision
        return decision

    def rem_sleep(self, decision):
        mem_dir = "synapses/harvested_memory"
        if not os.path.exists(mem_dir): return decision
        files = [f for f in os.listdir(mem_dir) if f.endswith(".json")]
        if not files: return decision
        try:
            with open(os.path.join(mem_dir, random.choice(files)), "r") as f:
                past = float(json.load(f).get("decision", 0.5))
            recalled = round((decision * 0.88) + (past * 0.12), 4)
            print(f"🌙 [GIẤC MƠ REM] Chiêm nghiệm ký ức: {past} ──► Điều biến: {recalled}")
            return recalled
        except Exception:
            return decision

    def process(self, context):
        self.extract_knowledge_graph(context.get("wisdom_text", ""))
        v_wisdom = context.get("wisdom_vector", [0.5, 0.5, 0.5, 0.5])
        q_dec = context.get("quorum_decision", 0.5)

        super_vec = [v_wisdom[0], v_wisdom[1], q_dec, round(1.0 - q_dec, 4)]
        entangled, masks = SuperXorMatrix.refract(super_vec, "nexus10_deca_xor")

        h_outs = [cell.forward(entangled) for cell in self.swarm]
        internal_pred = self.out_cell.forward(h_outs)
        raw_decision = round((internal_pred + q_dec) / 2.0, 4)

        opt_decision, loss = self.simulate_10_futures(raw_decision)
        meta_decision = self.synthesize_dynamic_logic(opt_decision, loss)

        if len(context.get("harvested", {})) <= 1:
            meta_decision = self.rem_sleep(meta_decision)

        target = 1.0 if super_vec[0] > super_vec[1] else 0.0
        delta_out = (target - meta_decision) * sigmoid_derivative(meta_decision)
        deltas_h = [delta_out * self.out_cell.weights[j] * sigmoid_derivative(h_outs[j]) for j in range(self.num_cells)]

        self.out_cell.backward(delta_out)
        for j, cell in enumerate(self.swarm): cell.backward(deltas_h[j])

        grad_backward = [
            round(sum(deltas_h[j] * self.swarm[j].weights[0] for j in range(self.num_cells)), 4),
            round(sum(deltas_h[j] * self.swarm[j].weights[1] for j in range(self.num_cells)), 4)
        ]

        context["final_decision"] = meta_decision
        context["grad_backward"] = grad_backward
        context["super_xor_masks"] = masks
        context["swarm_weights"] = [c.weights for c in self.swarm]
