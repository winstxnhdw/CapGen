FROM ghcr.io/winstxnhdw/capgen:main

ENV SERVER_PORT=7860
ENV OMP_NUM_THREADS=2
ENV CT2_FORCE_CPU_ISA=AVX512

EXPOSE $SERVER_PORT
