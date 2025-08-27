export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    
    if (url.pathname === '/health') {
      return new Response(JSON.stringify({
        status: 'healthy',
        worker: 'enhanced-mcp-memory',
        runtime: 'javascript',
        timestamp: new Date().toISOString(),
        services: {
          d1_connected: !!env.DB,
          kv_connected: !!env.KV_CACHE,
          r2_connected: !!env.R2_STORAGE,
          ai_connected: !!env.AI
        }
      }), {
        headers: { 'content-type': 'application/json' }
      });
    }
    
    return new Response(JSON.stringify({
      message: 'Enhanced MCP Memory Worker (JavaScript Test)',
      endpoints: ['/health'],
      ready_for: 'Python implementation'
    }), {
      headers: { 'content-type': 'application/json' }
    });
  }
};