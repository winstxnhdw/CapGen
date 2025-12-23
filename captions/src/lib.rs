#![feature(cold_path)]

use pyo3::PyAny;
use pyo3::exceptions::PyStopIteration;
use pyo3::intern;
use pyo3::prelude::Bound;
use pyo3::prelude::Py;
use pyo3::prelude::PyRef;
use pyo3::prelude::PyResult;
use pyo3::prelude::Python;
use pyo3::prelude::pyclass;
use pyo3::prelude::pymethods;
use pyo3::pyfunction;
use pyo3::types::PyAnyMethods;
use pyo3::types::PyIterator;

fn convert_seconds_to_hhmmssmmm(
    time_buffer: &mut [u8; 12],
    seconds: f64,
    millisecond_separator: u8,
) -> &str {
    let seconds_truncated = seconds as u64;
    let milliseconds = (seconds.fract() * 1000.0) as u64;
    let hours = seconds_truncated / 3600;
    let minutes = (seconds_truncated / 60) % 60;
    let seconds_remaining = seconds_truncated % 60;

    time_buffer[2] = b':';
    time_buffer[5] = b':';
    time_buffer[8] = millisecond_separator;

    time_buffer[0] += (hours / 10) as u8;
    time_buffer[1] += (hours % 10) as u8;
    time_buffer[3] += (minutes / 10) as u8;
    time_buffer[4] += (minutes % 10) as u8;
    time_buffer[6] += (seconds_remaining / 10) as u8;
    time_buffer[7] += (seconds_remaining % 10) as u8;
    time_buffer[9] += (milliseconds / 100) as u8;
    time_buffer[10] += ((milliseconds / 10) % 10) as u8;
    time_buffer[11] += (milliseconds % 10) as u8;

    unsafe { std::str::from_utf8_unchecked(time_buffer) }
}

#[cfg_attr(not(any(Py_3_8, Py_3_9)), pyclass(frozen, immutable_type))]
#[cfg_attr(any(Py_3_8, Py_3_9), pyclass(frozen))]
struct SubRipText {
    segments: Py<PyIterator>,
}

#[pymethods]
impl SubRipText {
    fn __iter__(slf: PyRef<'_, Self>) -> PyRef<'_, Self> {
        slf
    }

    fn __next__(&self, py: Python) -> PyResult<String> {
        let segment = self
            .segments
            .clone_ref(py)
            .into_bound(py)
            .next()
            .transpose()?
            .ok_or_else(|| PyStopIteration::new_err(()))?;

        let mut start_time_buffer = [b'0'; 12];
        let start = convert_seconds_to_hhmmssmmm(
            &mut start_time_buffer,
            segment.getattr(intern!(py, "start"))?.extract::<f64>()?,
            b',',
        );

        let mut end_time_buffer = [b'0'; 12];
        let end = convert_seconds_to_hhmmssmmm(
            &mut end_time_buffer,
            segment.getattr(intern!(py, "end"))?.extract::<f64>()?,
            b',',
        );

        let id = segment.getattr(intern!(py, "id"))?;
        let text = segment.getattr(intern!(py, "text"))?;

        Ok(format!("{id}\n{start} --> {end}\n{text}\n\n",))
    }
}

impl SubRipText {
    fn new(segments: Py<PyIterator>) -> Self {
        Self { segments }
    }
}

#[cfg_attr(not(any(Py_3_8, Py_3_9)), pyclass(immutable_type))]
#[cfg_attr(any(Py_3_8, Py_3_9), pyclass())]
struct WebVideoTextTracks {
    segments: Py<PyIterator>,
    has_started: bool,
}

#[pymethods]
impl WebVideoTextTracks {
    fn __iter__(slf: PyRef<'_, Self>) -> PyRef<'_, Self> {
        slf
    }

    fn __next__(&mut self, py: Python<'_>) -> PyResult<String> {
        if !self.has_started {
            std::hint::cold_path();
            self.has_started = true;
            return Ok("WEBVTT\n\n".into());
        }

        let segment = self
            .segments
            .clone_ref(py)
            .into_bound(py)
            .next()
            .transpose()?
            .ok_or_else(|| PyStopIteration::new_err(()))?;

        let mut start_time_buffer = [b'0'; 12];
        let start = convert_seconds_to_hhmmssmmm(
            &mut start_time_buffer,
            segment.getattr(intern!(py, "start"))?.extract::<f64>()?,
            b'.',
        );

        let mut end_time_buffer = [b'0'; 12];
        let end = convert_seconds_to_hhmmssmmm(
            &mut end_time_buffer,
            segment.getattr(intern!(py, "end"))?.extract::<f64>()?,
            b'.',
        );

        let text = segment.getattr(intern!(py, "text"))?;

        Ok(format!("{start} --> {end}\n{text}\n\n"))
    }
}

impl WebVideoTextTracks {
    fn new(segments: Py<PyIterator>) -> Self {
        Self {
            segments,
            has_started: false,
        }
    }
}

#[pyfunction]
fn segments_to_srt(segments: Bound<'_, PyAny>) -> PyResult<SubRipText> {
    Ok(SubRipText::new(segments.try_iter()?.into()))
}

#[pyfunction]
fn segments_to_vtt(segments: Bound<'_, PyAny>) -> PyResult<WebVideoTextTracks> {
    Ok(WebVideoTextTracks::new(segments.try_iter()?.into()))
}

#[pyo3::prelude::pymodule(gil_used = false)]
mod captions {
    #[pymodule_export]
    use super::segments_to_srt;
    #[pymodule_export]
    use super::segments_to_vtt;
}
