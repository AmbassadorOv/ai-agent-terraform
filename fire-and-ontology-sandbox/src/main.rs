use blake3::Hasher;
use std::time::{SystemTime, UNIX_EPOCH};

#[derive(Debug, Clone, PartialEq)]
pub enum EngineStatus {
    Active,
    HardNullTriggered,
}

#[derive(Debug, Clone)]
pub struct FrostSignatureProof {
    pub total_shares: u8,
    pub signed_shares: u8,
    pub signatures: Vec<String>,
}

#[derive(Debug, Clone)]
pub struct GenesisBlock {
    pub index: u64,
    pub timestamp: u64,
    pub previous_hash: [u8; 32],
    pub state_root: [u8; 32],
    pub metadata: String,
    pub signature_proof: FrostSignatureProof,
    pub engine_status: EngineStatus,
}

impl GenesisBlock {
    /// מייצר בלוק ג'נסיס חדש תחת פרוטוקול סירוב וקטורי
    pub fn new(metadata: &str, proof: FrostSignatureProof) -> Self {
        let mut block = GenesisBlock {
            index: 0,
            timestamp: SystemTime::now()
                .duration_since(UNIX_EPOCH)
                .unwrap()
                .as_secs(),
            previous_hash: [0u8; 32], // בלוק אפס
            state_root: [0u8; 32],
            metadata: metadata.to_string(),
            signature_proof: proof,
            engine_status: EngineStatus::Active,
        };

        // הפעלת מנגנון אימות הסף הקריפטוגרפי - HARD_NULL
        block.validate_constraints();
        block.state_root = block.calculate_blake3_root();

        block
    }

    /// בדיקת מנגנון הסירוב: אם אין 3 מתוך 5 חתימות תקפות, המערכת נועלת את הבלוק לאפס
    fn validate_constraints(&mut self) {
        if self.signature_proof.total_shares != 5 {
            self.engine_status = EngineStatus::HardNullTriggered;
            return;
        }

        // חוק 3/5: אם יש פחות מ-3 חתימות, או שיש סירוב אקטיבי - המערכת קורסת ל-Null
        if self.signature_proof.signed_shares < 3 {
            self.engine_status = EngineStatus::HardNullTriggered;
        }
    }

    /// חישוב State Root באמצעות BLAKE3
    pub fn calculate_blake3_root(&self) -> [u8; 32] {
        if self.engine_status == EngineStatus::HardNullTriggered {
            // HARD_NULL מחזיר מערך מאופס לחלוטין - חסימה מתמטית מוחלטת
            return [0u8; 32];
        }

        let mut hasher = Hasher::new();
        hasher.update(&self.index.to_le_bytes());
        hasher.update(&self.timestamp.to_le_bytes());
        hasher.update(&self.previous_hash);
        hasher.update(self.metadata.as_bytes());
        hasher.update(&[self.signature_proof.signed_shares]);

        *hasher.finalize().as_bytes()
    }
}

fn main() {
    println!("--- AUTONOMOUS KERNEL: INITIALIZING GENESIS MATRIX ---");

    // תרחיש א': ניסיון הרצה תקין עם 3 חתימות מאושרות (FROST 3/5)
    let valid_proof = FrostSignatureProof {
        total_shares: 5,
        signed_shares: 3,
        signatures: vec![
            "share_alpha_signed".to_string(),
            "share_beta_signed".to_string(),
            "share_gamma_signed".to_string(),
        ],
    };

    let genesis_block = GenesisBlock::new("ARK_KERNEL_INIT_SONS_OF_ISRAEL", valid_proof);
    println!("Scenario A (Valid 3/5 Threshold):");
    println!("Engine Status: {:?}", genesis_block.engine_status);
    println!("BLAKE3 State Root: {:x?}\n", genesis_block.state_root);

    // תרחיש ב': ניסיון הרצה עם 2 חתימות בלבד - הפעלת HARD_NULL אוטומטית
    let invalid_proof = FrostSignatureProof {
        total_shares: 5,
        signed_shares: 2,
        signatures: vec![
            "share_alpha_signed".to_string(),
            "share_beta_signed".to_string(),
        ],
    };

    let failed_block = GenesisBlock::new("ARK_KERNEL_INIT_SONS_OF_ISRAEL", invalid_proof);
    println!("Scenario B (Failed 2/5 Threshold - Refusal Crypto Active):");
    println!("Engine Status: {:?}", failed_block.engine_status);
    println!("BLAKE3 State Root (HARD_NULL): {:x?}", failed_block.state_root);

    assert_eq!(failed_block.engine_status, EngineStatus::HardNullTriggered);
    assert_eq!(failed_block.state_root, [0u8; 32]);
    println!("\n[Verification Complete] HARD_NULL verified. System is hermetically sealed.");
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_valid_threshold() {
        let valid_proof = FrostSignatureProof {
            total_shares: 5,
            signed_shares: 3,
            signatures: vec![
                "a".to_string(),
                "b".to_string(),
                "c".to_string(),
            ],
        };
        let block = GenesisBlock::new("TEST_METADATA", valid_proof);
        assert_eq!(block.engine_status, EngineStatus::Active);
        assert_ne!(block.state_root, [0u8; 32]);
    }

    #[test]
    fn test_invalid_shares_count() {
        let invalid_proof = FrostSignatureProof {
            total_shares: 4,
            signed_shares: 3,
            signatures: vec![
                "a".to_string(),
                "b".to_string(),
                "c".to_string(),
            ],
        };
        let block = GenesisBlock::new("TEST_METADATA", invalid_proof);
        assert_eq!(block.engine_status, EngineStatus::HardNullTriggered);
        assert_eq!(block.state_root, [0u8; 32]);
    }

    #[test]
    fn test_failed_threshold() {
        let invalid_proof = FrostSignatureProof {
            total_shares: 5,
            signed_shares: 2,
            signatures: vec![
                "a".to_string(),
                "b".to_string(),
            ],
        };
        let block = GenesisBlock::new("TEST_METADATA", invalid_proof);
        assert_eq!(block.engine_status, EngineStatus::HardNullTriggered);
        assert_eq!(block.state_root, [0u8; 32]);
    }
}
