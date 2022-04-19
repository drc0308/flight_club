// This prevents code from attempting to server-side which cuases problems with firebase hosting
export async function handle({ request, resolve }) {
    const response = await resolve(request, {
        ssr: false
    });
    return response;
}