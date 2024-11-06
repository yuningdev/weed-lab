import { clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';
import tailwindcssAnimate from 'tailwindcss-animate';

export function cn(...inputs) {
	return twMerge(clsx(inputs));
}

/**
 * Check if name is valid, 
 * It must contain only lowercase letters, numbers, periods (.), and hyphens (-).
 * @param {string} bucketName
 */
export function isValidBucektName(bucketName) {
	const regex = /^[a-z0-9.-]{1,255}$/;
	return regex.test(bucketName);
}
