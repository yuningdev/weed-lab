import { writable } from 'svelte/store';

const queryStatement = {
	queryS3Buckets: {},
	queryDirs: {},
	queryDuckDBS3Schema: { bucket_name: '', object_key: '' }
};

/**
 *  @type {import('svelte/store').Writable<queryStatement>}
 */
export const storeQueryStatement = writable(queryStatement);
