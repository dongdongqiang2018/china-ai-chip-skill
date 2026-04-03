#!/usr/bin/env python3
"""
Performance benchmarking script for vLLM-Ascend.
Measures latency and throughput metrics.
"""

import argparse
import time
from typing import List
from vllm import LLM, SamplingParams


def parse_args():
    parser = argparse.ArgumentParser(description="Benchmark vLLM-Ascend performance")
    parser.add_argument("--model", type=str, required=True, help="Path to model")
    parser.add_argument(
        "--tensor-parallel-size",
        type=int,
        default=1,
        help="Tensor parallelism size (default: 1)",
    )
    parser.add_argument(
        "--prompt-tokens",
        type=int,
        default=100,
        help="Number of prompt tokens per request (default: 100)",
    )
    parser.add_argument(
        "--output-tokens",
        type=int,
        default=100,
        help="Number of output tokens per request (default: 100)",
    )
    parser.add_argument(
        "--num-prompts",
        type=int,
        default=10,
        help="Number of prompts to process (default: 10)",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    print(f"Model: {args.model}")
    print(f"Tensor parallel size: {args.tensor_parallel_size}")
    print(f"Prompt tokens: {args.prompt_tokens}")
    print(f"Output tokens: {args.output_tokens}")
    print(f"Number of prompts: {args.num_prompts}")

    # Load model
    print("\nLoading model...")
    llm = LLM(
        model=args.model,
        tensor_parallel_size=args.tensor_parallel_size,
        trust_remote_code=True,
    )

    # Generate test prompts
    print("\nGenerating test prompts...")
    prompts = [
        "This is a test prompt for benchmarking." for _ in range(args.num_prompts)
    ]

    # Configure sampling
    sampling_params = SamplingParams(
        temperature=0.6,
        top_p=0.9,
        max_tokens=args.output_tokens,
    )

    # Benchmark
    print("\nRunning benchmark...")
    latencies = []

    for i, prompt in enumerate(prompts):
        start_time = time.time()

        outputs = llm.generate([prompt], sampling_params)

        end_time = time.time()
        latency = end_time - start_time
        latencies.append(latency)

        output_text = outputs[0].outputs[0].text
        print(
            f"  Request {i + 1}/{args.num_prompts}: latency={latency:.3f}s, tokens={len(output_text)}"
        )

    # Calculate metrics
    avg_latency = sum(latencies) / len(latencies)
    min_latency = min(latencies)
    max_latency = max(latencies)
    total_time = sum(latencies)
    throughput = (
        args.num_prompts * (args.prompt_tokens + args.output_tokens)
    ) / total_time

    print("\n=== Benchmark Results ===")
    print(f"Average latency: {avg_latency:.3f}s")
    print(f"Min latency: {min_latency:.3f}s")
    print(f"Max latency: {max_latency:.3f}s")
    print(f"Total time: {total_time:.3f}s")
    print(f"Throughput: {throughput:.2f} tokens/s")


if __name__ == "__main__":
    main()
