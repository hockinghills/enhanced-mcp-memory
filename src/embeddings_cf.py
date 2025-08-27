"""
Cloudflare Workers AI Embeddings
Replaces sentence-transformers with Cloudflare AI
"""

import json
from typing import List, Dict, Any, Optional

class CloudflareEmbeddings:
    """Embeddings using Cloudflare Workers AI"""
    
    def __init__(self, ai_binding):
        """Initialize with Workers AI binding"""
        self.ai = ai_binding
        self.model_name = "@cf/baai/bge-large-en-v1.5"  # Maximum quality embeddings
        
    async def generate_embedding(self, text: str) -> Optional[List[float]]:
        """Generate embedding for a single text"""
        try:
            # Use Cloudflare Workers AI to generate embedding
            result = await self.ai.run(self.model_name, {
                'text': text
            })
            
            # Extract embedding from result
            if 'data' in result and len(result['data']) > 0:
                return result['data'][0]
            else:
                console.error(f"No embedding data in result: {result}")
                return None
                
        except Exception as e:
            console.error(f"Error generating embedding: {e}")
            return None
    
    async def generate_embeddings(self, texts: List[str]) -> List[Optional[List[float]]]:
        """Generate embeddings for multiple texts"""
        embeddings = []
        for text in texts:
            embedding = await self.generate_embedding(text)
            embeddings.append(embedding)
        return embeddings
    
    def cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """Calculate cosine similarity between two vectors"""
        try:
            # Dot product
            dot_product = sum(a * b for a, b in zip(vec1, vec2))
            
            # Magnitudes
            magnitude1 = sum(a * a for a in vec1) ** 0.5
            magnitude2 = sum(b * b for b in vec2) ** 0.5
            
            if magnitude1 == 0 or magnitude2 == 0:
                return 0.0
            
            return dot_product / (magnitude1 * magnitude2)
        except Exception as e:
            console.error(f"Error calculating cosine similarity: {e}")
            return 0.0
    
    async def find_similar_texts(self, query_text: str, text_embeddings: List[Dict[str, Any]], threshold: float = 0.7) -> List[Dict[str, Any]]:
        """Find texts similar to query text"""
        try:
            # Generate embedding for query
            query_embedding = await self.generate_embedding(query_text)
            if not query_embedding:
                return []
            
            # Calculate similarities
            similarities = []
            for item in text_embeddings:
                if 'embedding' in item and item['embedding']:
                    similarity = self.cosine_similarity(query_embedding, item['embedding'])
                    if similarity >= threshold:
                        similarities.append({
                            **item,
                            'similarity': similarity
                        })
            
            # Sort by similarity (highest first)
            similarities.sort(key=lambda x: x['similarity'], reverse=True)
            return similarities
            
        except Exception as e:
            console.error(f"Error finding similar texts: {e}")
            return []