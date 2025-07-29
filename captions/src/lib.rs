use pyo3::intern;
use pyo3::prelude::pyclass;
use pyo3::prelude::pymethods;
use pyo3::prelude::Bound;
use pyo3::prelude::Py;
use pyo3::prelude::PyRef;
use pyo3::prelude::PyRefMut;
use pyo3::prelude::PyResult;
use pyo3::prelude::Python;
use pyo3::pyfunction;
use pyo3::types::PyAnyMethods;
use pyo3::types::PyIterator;
use pyo3::types::PyModuleMethods;
use pyo3::types::PyString;
use pyo3::wrap_pyfunction;

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

    fn __next__(slf: PyRef<'_, Self>, py: Python<'_>) -> PyResult<String> {
        let next_segment = slf.segments.clone_ref(py).into_bound(py).next();
        let segment =
            next_segment.unwrap_or_else(|| Err(pyo3::exceptions::PyStopIteration::new_err(())))?;

        let id = segment.getattr(intern!(py, "id"))?;
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

        let text = segment.getattr(intern!(py, "text"))?.extract::<String>()?;
        let caption = format!("{id}\n{start} --> {end}\n{text}\n\n",);

        Ok(caption)
    }
}

impl SubRipText {
    fn new(segments: Py<PyIterator>) -> Self {
        Self { segments }
    }
}

#[cfg_attr(not(any(Py_3_8, Py_3_9)), pyclass(immutable_type))]
#[cfg_attr(any(Py_3_8, Py_3_9), pyclass)]
struct WebVideoTextTracks {
    segments: Py<PyIterator>,
    has_started: bool,
}

#[pymethods]
impl WebVideoTextTracks {
    fn __iter__(slf: PyRef<'_, Self>) -> PyRef<'_, Self> {
        slf
    }

    fn __next__(mut slf: PyRefMut<'_, Self>, py: Python<'_>) -> PyResult<String> {
        if !slf.has_started {
            slf.has_started = true;
            return Ok("WEBVTT\n\n".into());
        }

        let next_segment = slf.segments.clone_ref(py).into_bound(py).next();
        let segment =
            next_segment.unwrap_or_else(|| Err(pyo3::exceptions::PyStopIteration::new_err(())))?;

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

        let text = segment
            .getattr(intern!(py, "text"))?
            .extract::<Bound<'_, PyString>>()?;

        let caption = format!("{start} --> {end}\n{text}\n\n",);

        Ok(caption)
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
fn segments_to_srt(segments: Py<PyIterator>) -> SubRipText {
    SubRipText::new(segments)
}

#[pyfunction]
fn segments_to_vtt(segments: Py<PyIterator>) -> WebVideoTextTracks {
    WebVideoTextTracks::new(segments)
}

#[pyo3::prelude::pymodule()]
fn captions(m: &Bound<'_, pyo3::prelude::PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(segments_to_srt, m)?)?;
    m.add_function(wrap_pyfunction!(segments_to_vtt, m)?)?;
    Ok(())
}
