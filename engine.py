import os
import sys
import json

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from cortex.omni_intake import OmniIntakeDecaLobe
from cortex.indra_attention import IndraAttentionDecaLobe
from cortex.metacognition import MetacognitionDecaLobe
from cortex.apex_transmute import ApexTransmuteDecaLobe

VITAL_CELLS = [
    "cells/linguistic_cell.py",
    "cells/neuron.py",
    "cells/super_xor.py"
]

class Nexus10DecagonKernel:
    def __init__(self):
        self.repo_name = os.environ.get("GITHUB_REPOSITORY", "100048777766367/nexus-10")
        self.owner = os.environ.get("REPO_OWNER", "100048777766367")
        self.ancestor = f"{self.owner}/nexus-09"
        
        self.lineage = [
            f"{self.owner}/nexus-09", f"{self.owner}/nexus-08",
            f"{self.owner}/nexus-07", f"{self.owner}/nexus-06",
            f"{self.owner}/nexus-05", f"{self.owner}/nexus", f"{self.owner}/genome"
        ]

        self.ensure_folders()

        # 4 ĐẠI THÙY NÃO BẬC F10 (+n^2)
        self.omni_lobe = OmniIntakeDecaLobe(self.owner, self.lineage)
        self.indra_lobe = IndraAttentionDecaLobe()
        self.meta_lobe = MetacognitionDecaLobe(num_cells=8)
        self.transmute_lobe = ApexTransmuteDecaLobe()

        self.context = {
            "repo_name": self.repo_name,
            "owner": self.owner,
            "ancestor": self.ancestor,
            "peers": self.load_peers(),
            "current_epoch": self.load_epoch()
        }

    def ensure_folders(self):
        for d in ["cells", "cortex", "synapses", "synapses/harvested_memory"]:
            os.makedirs(d, exist_ok=True)

    def load_peers(self):
        p_file = "synapses/peers.json"
        if os.path.exists(p_file):
            try:
                with open(p_file, "r") as f: return json.load(f).get("trusted_peers", [])
            except Exception: pass
        return [f"{self.owner}/nexus-09", f"{self.owner}/nexus-08", f"{self.owner}/nexus-07", f"{self.owner}/neuron", f"{self.owner}/seed", f"{self.owner}/motor"]

    def load_epoch(self):
        s_file = "synapses/state.json"
        if os.path.exists(s_file):
            try:
                with open(s_file, "r") as f: return json.load(f).get("generation_epoch", 0) + 1
            except Exception: pass
        return 1

    def run(self):
        print("=" * 80)
        print(f"☸️ [NEXUS-10 DECAGON KERNEL] KHỞI ĐỘNG THẾ HỆ #{self.context['current_epoch']}")
        print(f"👑 Bậc: F10 Thập Toàn Đại Viên Mãn – Ma Trận Chú Ý Toàn Ảnh Indra O(n^2)")
        print("=" * 80)

        # 1. Thùy Cảm Thụ: Nuốt nang bào tử F9, lọc Stateless Token & cào tri thức
        self.omni_lobe.process(self.context, VITAL_CELLS)

        # 2. Thùy Indra: Ma trận tương quan chéo N x N (O(n^2)) & Sóng não Kuramoto bậc 10
        self.indra_lobe.process(self.context)

        # 3. Thùy Siêu Nhận Thức: Tự sinh mã vi mô, Giả lập 10 kịch bản What-If & Siêu XOR
        self.meta_lobe.process(self.context)

        # 4. Thùy Chấp Hành: La bàn Thập Độ Ba La Mật, Biến hình 11 tầng, Merkle Tree CID
        self.transmute_lobe.process(self.context)

        print("=" * 80)
        print(f"✨ [HOÀN TẤT VÒNG ĐỜI F10] Thập Toàn Thập Mỹ đã viên mãn trong vũ trụ Indra!")
        print("=" * 80)

if __name__ == "__main__":
    node = Nexus10DecagonKernel()
    node.run()
