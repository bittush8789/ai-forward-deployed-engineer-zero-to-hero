#!/usr/bin/env python3
"""
Project 3: Distributed AI Platform (gRPC & Protocol Buffers)
Skills Focus: Protobuf Schema Parsing, Binary Serialization, gRPC Unary & Streaming.

This script simulates a gRPC-style inter-service communication pipeline. It
compares the serialization performance of binary Protobuf payloads against plain
text JSON, and demonstrates gRPC-style unary and streaming requests.
"""

import json
import time

class MockProtobufMessage:
    """Simulates a gRPC Protocol Buffer message structure."""
    def __init__(self, prompt: str, max_tokens: int):
        self.prompt = prompt
        self.max_tokens = max_tokens

    def serialize_to_binary(self) -> bytes:
        """Simulates compact binary serialization of field tags."""
        # Simulated binary formatting of field tags (e.g. tag 1 = prompt, tag 2 = max_tokens)
        binary_payload = f"\x0a{len(self.prompt)}{self.prompt}\x10{self.max_tokens}".encode("utf-8")
        return binary_payload

    @classmethod
    def deserialize_from_binary(cls, binary_data: bytes):
        """Simulates binary deserialization back to model object."""
        decoded = binary_data.decode("utf-8")
        # Simple parser simulation based on tags
        prompt_len = ord(decoded[1])
        prompt = decoded[2:2+prompt_len]
        max_tokens = ord(decoded[-1])
        return cls(prompt, max_tokens)

class DistributedInferenceService:
    """Simulates an internal gRPC Model Serving microservice."""
    def process_unary_call(self, request_binary: bytes) -> bytes:
        # Deserialize request
        req = MockProtobufMessage.deserialize_from_binary(request_binary)
        print(f"[gRPC SERVER] Deserialized Unary Request. Prompt: '{req.prompt}', Max Tokens: {req.max_tokens}")
        
        # Process and generate response
        response_text = f"Completed inference for: '{req.prompt}'"
        # Return serialized binary response
        return f"\x0a{len(response_text)}{response_text}".encode("utf-8")

    def process_streaming_call(self, request_binary: bytes):
        req = MockProtobufMessage.deserialize_from_binary(request_binary)
        print(f"[gRPC SERVER] Deserialized Streaming Request. Starting token stream...")
        
        # Simulate streaming chunks
        chunks = ["Executive ", "brief: ", "Llama-3 ", "is ", "running."]
        for chunk in chunks:
            time.sleep(0.1) # Simulate network stream delay
            yield f"\x0a{len(chunk)}{chunk}".encode("utf-8")

def main():
    print("Project 3: Distributed AI Platform (gRPC Service Simulator)")
    print("="*60)
    
    server = DistributedInferenceService()
    
    # 1. Performance comparison: JSON vs Protobuf
    print("[PERFORMANCE TEST] Comparing JSON vs Protobuf Serialization...")
    prompt_str = "Analyze server logs and report errors."
    max_tokens = 128
    
    # JSON Serialization
    start_json = time.perf_counter()
    json_payload = json.dumps({"prompt": prompt_str, "max_tokens": max_tokens})
    json_bytes = json_payload.encode("utf-8")
    json_time = (time.perf_counter() - start_json) * 1000
    
    # Protobuf Serialization
    start_proto = time.perf_counter()
    proto_msg = MockProtobufMessage(prompt_str, max_tokens)
    proto_bytes = proto_msg.serialize_to_binary()
    proto_time = (time.perf_counter() - start_proto) * 1000
    
    print(f" - JSON Payload Size: {len(json_bytes)} bytes | Serialization Time: {json_time:.4f}ms")
    print(f" - Proto Payload Size: {len(proto_bytes)} bytes | Serialization Time: {proto_time:.4f}ms")
    print(f" -> Size Reduction: {((len(json_bytes) - len(proto_bytes)) / len(json_bytes)) * 100:.1f}% smaller")
    
    print("\n" + "-"*40 + "\n")
    
    # 2. Simulate gRPC Unary Call
    print("[gRPC CLIENT] Executing Unary Call...")
    serialized_req = proto_msg.serialize_to_binary()
    binary_resp = server.process_unary_call(serialized_req)
    
    # Decode response
    decoded_resp = binary_resp.decode("utf-8")[2:]
    print(f"[gRPC CLIENT] Received Unary Response: '{decoded_resp}'")
    
    print("\n" + "-"*40 + "\n")
    
    # 3. Simulate gRPC Server Streaming Call
    print("[gRPC CLIENT] Executing Server Streaming Call...")
    stream_generator = server.process_streaming_call(serialized_req)
    
    print("[gRPC CLIENT] Receiving Stream Chunks:")
    for chunk_binary in stream_generator:
        chunk_text = chunk_binary.decode("utf-8")[2:]
        print(f" -> Chunk: '{chunk_text}'")

if __name__ == "__main__":
    main()
