// audio_processor.rs
use std::fs::File;
use std::io::BufReader;
use hound;
use pyo3::prelude::*;

pub struct AudioProcessor {
    samples: Vec<f32>,
    sample_rate: u32,
}

impl AudioProcessor {
    pub fn new(file_path: &str) -> Result<Self, Box<dyn std::error::Error>> {
        let file = File::open(file_path)?;
        let reader = BufReader::new(file);
        let mut wav_reader = hound::WavReader::new(reader)?;
        
        // Convert samples to f32 and normalize
        let samples: Vec<f32> = wav_reader.samples::<i16>()
            .map(|s| s.unwrap() as f32 / i16::MAX as f32)
            .collect();
        
        let spec = wav_reader.spec();
        
        Ok(AudioProcessor {
            samples,
            sample_rate: spec.sample_rate,
        })
    }

    pub fn get_frequency_bands(&self, num_bands: usize) -> Vec<f32> {
        let chunk_size = self.samples.len() / num_bands;
        let mut bands = Vec::with_capacity(num_bands);
        
        for i in 0..num_bands {
            let start = i * chunk_size;
            let end = start + chunk_size;
            let chunk = &self.samples[start..end.min(self.samples.len())];
            
            // Calculate RMS for each band
            let rms = (chunk.iter()
                .map(|x| x * x)
                .sum::<f32>() / chunk.len() as f32)
                .sqrt();
            bands.push(rms);
        }
        
        bands
    }
}

// PyO3 bindings for Python integration
#[cfg(feature = "python_bindings")]
#[pymodule]
fn audio_processor(_py: Python, m: &PyModule) -> PyResult<()> {
    #[pyclass]
    struct PyAudioProcessor {
        inner: AudioProcessor,
    }

    #[pymethods]
    impl PyAudioProcessor {
        #[new]
        fn new(file_path: &str) -> PyResult<Self> {
            match AudioProcessor::new(file_path) {
                Ok(processor) => Ok(PyAudioProcessor { inner: processor }),
                Err(e) => Err(pyo3::exceptions::PyRuntimeError::new_err(e.to_string())),
            }
        }

        fn get_frequency_bands(&self, num_bands: usize) -> Vec<f32> {
            self.inner.get_frequency_bands(num_bands)
        }
    }

    m.add_class::<PyAudioProcessor>()?;

    #[pyfunction]
    unsafe fn get_frequency_bands(num_bars: usize) -> PyResult<Vec<f64>> {
        // Example implementation
        Ok(vec![1.0; num_bars])
    }

    m.add_function(wrap_pyfunction!(get_frequency_bands, m)?)?;

    Ok(())
}