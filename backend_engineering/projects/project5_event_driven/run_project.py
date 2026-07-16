#!/usr/bin/env python3
"""
Project 5: Event-Driven AI Workflow Platform (Decoupled EDA Pipeline)
Skills Focus: Event Stream Topics, Producers & Consumers, Kafka Partition Offsets.

This script implements a simulated Apache Kafka message broker. It demonstrates
how a Producer publishes raw file upload events, and independent Consumer groups
process text extractions and vector indexing asynchronously.
"""

import json
import time

class MockKafkaBroker:
    def __init__(self):
        # Dictionary of topics containing messages: { topic_name: [ messages ] }
        self.topics = {
            "document_uploaded": [],
            "text_extracted": [],
            "embeddings_generated": []
        }
        # Offset pointers tracking consumer reads: { group_id: { topic_name: offset_index } }
        self.consumer_offsets = {}

    def publish(self, topic, message):
        """Simulates producing an event payload to a topic."""
        self.topics[topic].append(message)
        offset = len(self.topics[topic]) - 1
        print(f"[KAFKA BROKER] Produced event to Topic '{topic}' | Offset: {offset}")

    def consume(self, topic, group_id):
        """Simulates a consumer fetching new messages based on partition offset indexes."""
        if group_id not in self.consumer_offsets:
            self.consumer_offsets[group_id] = {}
            
        if topic not in self.consumer_offsets[group_id]:
            self.consumer_offsets[group_id][topic] = 0
            
        current_offset = self.consumer_offsets[group_id][topic]
        topic_messages = self.topics[topic]
        
        if current_offset < len(topic_messages):
            message = topic_messages[current_offset]
            self.consumer_offsets[group_id][topic] += 1
            print(f"[KAFKA BROKER] Consumer '{group_id}' read from Topic '{topic}' | Offset: {current_offset}")
            return message
        else:
            return None

class DocumentIngestionProducer:
    def upload_file(self, broker, file_name, raw_content):
        print(f"\n[PRODUCER] Uploading file: '{file_name}'...")
        event = {
            "file_name": file_name,
            "raw_content": raw_content,
            "timestamp": time.time()
        }
        # Publish event
        broker.publish("document_uploaded", event)

class TextExtractorConsumer:
    def run_step(self, broker):
        # Fetch event
        event = broker.consume("document_uploaded", group_id="text_extractor_group")
        if not event:
            return False
            
        print(f"[CONSUMER: TextExtractor] Processing document: '{event['file_name']}'")
        # Extract text content
        extracted_text = event["raw_content"].upper() # Simple extraction simulation
        
        # Publish output event
        output_event = {
            "file_name": event["file_name"],
            "extracted_text": extracted_text,
            "timestamp": time.time()
        }
        broker.publish("text_extracted", output_event)
        return True

class VectorIndexerConsumer:
    def run_step(self, broker):
        # Fetch event
        event = broker.consume("text_extracted", group_id="vector_indexer_group")
        if not event:
            return False
            
        print(f"[CONSUMER: VectorIndexer] Ingesting and indexing text: '{event['extracted_text']}'")
        # Simulating vector indexing
        print(f"[CONSUMER: VectorIndexer] Successfully indexed '{event['file_name']}' in ChromaDB.")
        return True

def main():
    print("Project 5: Event-Driven AI Ingestion Platform (Kafka Simulator)")
    print("="*60)
    
    broker = MockKafkaBroker()
    producer = DocumentIngestionProducer()
    extractor = TextExtractorConsumer()
    indexer = VectorIndexerConsumer()
    
    # 1. Producer publishes file uploads
    producer.upload_file(broker, "policy_guideline.pdf", "All staff can work remotely up to 2 days per week.")
    
    # 2. Text Extractor consumes upload event and publishes extracted text
    extractor.run_step(broker)
    
    # 3. Vector Indexer consumes extracted text event and indexes data
    indexer.run_step(broker)

if __name__ == "__main__":
    main()
