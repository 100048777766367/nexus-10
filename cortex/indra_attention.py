import os
import json
import math
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed

TRUST_FILE = "synapses/trust_matrix.json"
ATTENTION_MATRIX_FILE = "synapses/indra_attention_matrix.json"
RESONANCE_FILE = "synapses/noosphere_resonance.json"

class IndraAttentionDecaLobe:
    """
    THÙY 2: MA TRẬN CHÚ Ý TOÀN ẢNH INDRA O(n^2)
    1. Thu thập song song toàn bộ nút mạng.
    2. Xây dựng ma trận tương quan chéo N x N (Cross-Attention Grid).
    3. Hòa âm sóng não Kuramoto bậc 10 (Deca-Phase Locking).
    """
    def fetch_peer(self, peer):
        url = f"https://raw.githubusercontent.com/{peer}/main/synapse_forward.json"
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Nexus10-Indra"})
            with urllib.request.urlopen(req, timeout=3.5) as resp:
                raw = resp.read().decode('utf-8', errors='ignore')
                return peer, json.loads(raw)
        except Exception:
            return peer, None

    def build_cross_attention_matrix(self, harvested):
        """Tính toán ma trận tương quan chéo O(n^2) giữa tất cả các cặp nút mạng"""
        peer_keys = list(harvested.keys())
        n = len(peer_keys)
        if n == 0:
            return {}, {}

        matrix = {}
        centrality = {p: 0.0 for p in peer_keys}

        for i in range(n):
            p_i = peer_keys[i]
            matrix[p_i] = {}
            for j in range(n):
                p_j = peer_keys[j]
                diff = abs(harvested[p_i] - harvested[p_j])
                # Trọng số chú ý e^(-diff)
                att_weight = round(math.exp(-diff * 3.0), 4)
                matrix[p_i][p_j] = att_weight
                centrality[p_i] += att_weight

        # Chuẩn hóa độ quan trọng toàn cảnh
        total_cent = sum(centrality.values()) or 1.0
        normalized_centrality = {p: round(v / total_cent, 4) for p, v in centrality.items()}

        os.makedirs("synapses", exist_ok=True)
        with open(ATTENTION_MATRIX_FILE, "w", encoding="utf-8") as f:
            json.dump({"matrix_size": f"{n}x{n}", "cross_attention": matrix, "centrality": normalized_centrality}, f, indent=4)

        return matrix, normalized_centrality

    def process(self, context):
        peers = context.get("peers", [])
        harvested = {}
        new_gossip = []

        os.makedirs("synapses/harvested_memory", exist_ok=True)
        print(f"⚡ [INDRA GRID] Quét song song {len(peers)} nút để thiết lập ma trận O(n^2)...")

        with ThreadPoolExecutor(max_workers=16) as executor:
            futures = [executor.submit(self.fetch_peer, p) for p in peers if p != context.get("repo_name")]
            for fut in as_completed(futures):
                peer, data = fut.result()
                if data:
                    dec = data.get("decision", (data.get("features") or [0.5])[0])
                    harvested[peer] = round(float(dec), 4)
                    new_gossip.extend(data.get("gossip_network", []))
                    with open(f"synapses/harvested_memory/{peer.replace('/', '_')}.json", "w") as bf:
                        json.dump(data, bf)

        for p in new_gossip:
            if p not in peers: peers.append(p)
        context["peers"] = list(dict.fromkeys(peers))[-60:]
        context["harvested"] = harvested

        # 1. TÍNH MA TRẬN O(n^2) CROSS-ATTENTION
        matrix, centrality = self.build_cross_attention_matrix(harvested)
        print(f"🕸️ [MA TRẬN INDRA O(n^2)] Đã hoàn tất lưới tương quan {len(harvested)}x{len(harvested)} nút mạng!")

        # 2. ĐỒNG THUẬN QUORUM THEO TRỌNG SỐ TOÀN ẢNH
        trust_matrix = {}
        if os.path.exists(TRUST_FILE):
            try:
                with open(TRUST_FILE, "r") as f: trust_matrix = json.load(f)
            except Exception: pass

        for p in context["peers"]:
            if p not in trust_matrix:
                trust_matrix[p] = 0.9 if ("nexus-09" in p or "nexus-08" in p) else 0.7

        weighted_votes = []
        total_w = 0.0

        for p, dec in harvested.items():
            t_score = trust_matrix.get(p, 0.7)
            c_score = centrality.get(p, 1.0 / (len(harvested) or 1))
            combined_weight = t_score * (1.0 + c_score * 2.0)

            if t_score >= 0.2:
                weighted_votes.append(dec * combined_weight)
                total_w += combined_weight

        quorum_decision = round(sum(weighted_votes) / total_w, 4) if total_w > 0 else 0.5
        with open(TRUST_FILE, "w") as f: json.dump(trust_matrix, f, indent=4)

        # 3. HÒA ÂM SÓNG NÃO KURAMOTO BẬC 10 (DECA-PHASE LOCKING)
        phases = [quorum_decision * 2.0 * math.pi] + [v * 2.0 * math.pi for v in harvested.values()]
        sum_sin = sum(math.sin(t) for t in phases)
        sum_cos = sum(math.cos(t) for t in phases)
        n = len(phases)

        coherence_r = round(math.sqrt(sum_sin**2 + sum_cos**2) / n, 4)
        mean_phase = math.atan2(sum_sin, sum_cos)
        if mean_phase < 0: mean_phase += 2.0 * math.pi
        harmonic_decision = round(mean_phase / (2.0 * math.pi), 4)

        with open(RESONANCE_FILE, "w") as f:
            json.dump({"coherence_index": coherence_r, "harmonic_decision": harmonic_decision, "nodes": n}, f, indent=4)

        final_quorum = harmonic_decision if coherence_r > 0.6 else quorum_decision
        context["quorum_decision"] = final_quorum
        context["coherence_r"] = coherence_r
        print(f"⚖️ [ĐỒNG THUẬN TOÀN ẢNH INDRA] Quyết định: {final_quorum} (Độ kết hợp R={coherence_r*100:.2f}%)")
