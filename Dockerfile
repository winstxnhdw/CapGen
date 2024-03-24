FROM ghcr.io/winstxnhdw/capgen:main

ENV APP_PORT 7860
ENV OMP_NUM_THREADS 2
ENV CT2_USE_EXPERIMENTAL_PACKED_GEMM 1
ENV CT2_FORCE_CPU_ISA AVX512
ENV EVENTS_PER_WINDOW 5

EXPOSE $APP_PORT
