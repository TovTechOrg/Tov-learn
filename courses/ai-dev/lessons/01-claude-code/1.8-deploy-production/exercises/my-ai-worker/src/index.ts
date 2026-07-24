interface Env {
	AI: any;
}

export default {
	async fetch(request: Request, env: Env): Promise<Response> {
		if (request.method !== 'POST') {
			return new Response('שלח POST עם {"text": "..."}', { status: 200 });
		}
		try {
			const { text } = await request.json() as { text: string };
			const response = await env.AI.run(
				'@cf/meta/llama-4-scout-17b-16e-instruct',
				{
					prompt: `תרגם את המשפט הבא לאנגלית: '${text}'`
				}
			);
			return new Response(JSON.stringify(response));
		} catch (e: any) {
			return new Response(JSON.stringify({ error: e.message, stack: e.stack }), { status: 500 });
		}
	},
};
