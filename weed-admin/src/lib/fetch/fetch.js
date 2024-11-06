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

	/**
	 * @type {{data?: any}}
	 */
	let res = {};

	if (method === 'GET') {
		res = await api.get(endpoint, { searchParams: new URLSearchParams(params) }).json();
	} else if (method === 'POST') {
		res = await api.post(endpoint, { json: params }).json();
	}

	if (res.hasOwnProperty('data')) {
		return res.data;
	} else {
		return res;
	}
};

export default fetchApi;
