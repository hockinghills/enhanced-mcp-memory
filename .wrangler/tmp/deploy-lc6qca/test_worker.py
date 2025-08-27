"""
Test Python Worker for Cloudflare
Simplified version to test deployment
"""

import json
from datetime import datetime

async def on_fetch(request, env):
    """Main entry point for HTTP requests"""
    
    # Get request details
    url = str(request.url)
    method = request.method
    
    # Basic routing
    if '/health' in url:
        return Response.json({
            'status': 'healthy',
            'worker': 'enhanced-mcp-memory',
            'runtime': 'python',
            'timestamp': datetime.now().isoformat(),
            'services': {
                'd1_connected': bool(env.DB),
                'kv_connected': bool(env.KV_CACHE),
                'r2_connected': bool(env.R2_STORAGE),
                'ai_connected': bool(env.AI)
            }
        })
    
    elif '/test-d1' in url:
        # Test D1 database
        try:
            result = await env.DB.prepare("SELECT 1 as test").first()
            return Response.json({
                'success': True,
                'd1_test': result,
                'message': 'D1 database connection successful'
            })
        except Exception as e:
            return Response.json({
                'success': False,
                'error': str(e)
            }, status=500)
    
    elif '/test-kv' in url:
        # Test KV namespace
        try:
            # Write and read test value
            await env.KV_CACHE.put('test_key', 'test_value')
            value = await env.KV_CACHE.get('test_key')
            return Response.json({
                'success': True,
                'kv_test': value,
                'message': 'KV namespace connection successful'
            })
        except Exception as e:
            return Response.json({
                'success': False,
                'error': str(e)
            }, status=500)
    
    else:
        # Default response
        return Response.json({
            'message': 'Enhanced MCP Memory Worker (Python)',
            'endpoints': [
                '/health - Health check',
                '/test-d1 - Test D1 database',
                '/test-kv - Test KV namespace'
            ],
            'runtime': 'python-workers',
            'version': '0.1.0'
        })

class Response:
    @staticmethod
    def json(data, status=200):
        return Response(
            json.dumps(data),
            status=status,
            headers={
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            }
        )