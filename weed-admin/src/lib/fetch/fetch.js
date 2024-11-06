import ky from 'ky';

const API = import.meta.env.VITE_API_ENDPOINT;

// Create S3 Bucket

const api = ky.extend({ prefixUrl: API });

/**
 *
 * @param {'GET' | 'POST' | 'PUT' | 'DELETE'} method
 * @param {string | undefined} topic
 * @param {string | undefined} url
 * @param {any} params
 */
const fetchApi = async (method = 'GET', topic = '', url = '', params) => {
	const endpoint = `${topic}${url}`;
	if (method === 'GET') {
		return await api.get(endpoint, { searchParams: new URLSearchParams(params) }).json();
	} else if (method === 'POST') {
		return await api.post(endpoint, { json: params }).json();
	}
};

export default fetchApi;
