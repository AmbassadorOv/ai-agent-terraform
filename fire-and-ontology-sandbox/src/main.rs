use blake3;
use serde::{Serialize, Deserialize};
use chrono::Utc;
use thiserror::Error;

#[derive(Error, Debug)]
pub enum EngineError {
    #[error("HARD_NULL TRIGGERED: Required 3/5")]
    HardNullTriggered,
}

#[derive(Serialize, Deserialize, Debug)]
pub struct BlockHeader {
    pub version: u32,
    pub prev_hash: [u8; 32],
    pub merkle_root: [u8; 32],
    pub timestamp: i64,
    pub threshold: (u8, u8),
}

pub fn hash_header(h: &BlockHeader) -> [u8; 32] {
    *blake3::hash(&serde_json::to_vec(h).unwrap()).as_bytes()
}

pub fn verify_threshold(sigs: usize, t: u8) -> Result<(), EngineError> {
    if sigs < t as usize {
        Err(EngineError::HardNullTriggered)
    } else {
        Ok(())
    }
}

fn main() {
    println!("KERNEL_INIT_SONS_OF_ISRAEL");
    println!("HARD_NULL: 3/5 Active. System hermetically sealed.");
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_verify_threshold_success() {
        assert!(verify_threshold(3, 3).is_ok());
        assert!(verify_threshold(4, 3).is_ok());
    }

    #[test]
    fn test_verify_threshold_failure() {
        assert!(verify_threshold(2, 3).is_err());
    }

    #[test]
    fn test_hash_header() {
        let header = BlockHeader {
            version: 1,
            prev_hash: [0u8; 32],
            merkle_root: [1u8; 32],
            timestamp: Utc::now().timestamp(),
            threshold: (3, 5),
        };
        let h1 = hash_header(&header);
        let h2 = hash_header(&header);
        assert_eq!(h1, h2);
        assert_ne!(h1, [0u8; 32]);
    }
}
